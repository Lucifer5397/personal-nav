"""并发检测所有书签URL可访问性，清理死链"""
import mysql.connector
import requests
import concurrent.futures
import time
from urllib.parse import urlparse

DB = {'host': 'localhost', 'user': 'root', 'password': '123456', 'database': 'pj1', 'buffered': True}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
}

def check_url(bid, url, title):
    """检测单个URL，返回 (bid, url, title, ok)"""
    try:
        # 先用 HEAD，失败了再用 GET
        for method in ['HEAD', 'GET']:
            try:
                r = requests.request(method, url, headers=HEADERS, timeout=10, allow_redirects=True, verify=True)
                if r.status_code < 500:
                    return (bid, url, title, True, r.status_code)
            except requests.exceptions.SSLError:
                # SSL错误，尝试跳过验证
                try:
                    r = requests.request(method, url, headers=HEADERS, timeout=10, allow_redirects=True, verify=False)
                    if r.status_code < 500:
                        return (bid, url, title, True, r.status_code)
                except:
                    pass
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                continue
        return (bid, url, title, False, 0)
    except Exception as e:
        return (bid, url, title, False, str(e)[:50])

def main():
    conn = mysql.connector.connect(**DB)
    c = conn.cursor()
    c.execute('SELECT id, title, url FROM bookmarks')
    all_rows = c.fetchall()
    conn.close()
    print(f'共 {len(all_rows)} 个书签，开始检测...\n')

    dead = []
    alive = 0
    checked = 0

    # 并发50
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as pool:
        futures = {pool.submit(check_url, bid, url, title): (bid, url, title) for bid, title, url in all_rows}
        for f in concurrent.futures.as_completed(futures):
            bid, url, title, ok, status = f.result()
            checked += 1
            if ok:
                alive += 1
            else:
                dead.append((bid, url, title))
                print(f'  DEAD [{checked}] {title[:30]:30s} | {url[:70]}')
            if checked % 100 == 0:
                print(f'  进度: {checked}/{len(all_rows)} (存活:{alive} 死链:{len(dead)})')

    print(f'\n=== 检测完成 ===')
    print(f'存活: {alive}')
    print(f'死链: {len(dead)}')

    # 清理死链
    if dead:
        conn = mysql.connector.connect(**DB)
        c = conn.cursor()
        for bid, url, title in dead:
            c.execute('DELETE FROM bookmarks WHERE id=%s', (bid,))
        conn.commit()
        conn.close()
        print(f'已从数据库删除 {len(dead)} 条死链')

        # 最终统计
        conn = mysql.connector.connect(**DB)
        c = conn.cursor()
        c.execute("SELECT category, COUNT(*) FROM bookmarks GROUP BY category ORDER BY count(*) DESC")
        names = {'dev':'开发技术','study':'学习百科','media':'影音娱乐','social':'社交社区','office':'办公效率','tools':'网络工具','ai':'人工智能','commerce':'购物交易','life':'生活服务','news':'新闻资讯','adult':'成人内容','service':'便民服务','design':'设计资源','game':'游戏电竞'}
        total = 0
        for cat, cnt in c.fetchall():
            print(f'  {names.get(cat,cat)}: {cnt}')
            total += cnt
        print(f'  最终总计: {total}')
        conn.close()

if __name__ == '__main__':
    start = time.time()
    main()
    print(f'\n耗时: {time.time()-start:.0f}s')

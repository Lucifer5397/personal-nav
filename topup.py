"""补足：成人50 游戏40 其他扩充"""
import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', password='123456', database='pj1', buffered=True)
c = conn.cursor()

ADD = [
    # ===== 成人 24个 → 总计50 =====
    ('adult','视频','JavGuru','https://jav.guru','日本影片信息库','🔞'),
    ('adult','视频','R18','https://www.r18.com','日本正版成人平台','🔞'),
    ('adult','视频','Fanza','https://www.dmm.co.jp','DMM成人内容','🔞'),
    ('adult','视频','Beeg','https://beeg.com','成人视频播放','🔞'),
    ('adult','视频','Txxx','https://txxx.com','成人视频社区','🔞'),
    ('adult','视频','Porntrex','https://www.porntrex.com','高清成人视频','🔞'),
    ('adult','图片','ImageFap','https://www.imagefap.com','成人图片社区','🔞'),
    ('adult','图片','PornPics','https://www.pornpics.com','成人图片画廊','🔞'),
    ('adult','图片','Sex.com','https://www.sex.com','成人图片搜索引擎','🔞'),
    ('adult','论坛','Sex8','https://www.sex8.zone','中文成人综合社区','🔞'),
    ('adult','论坛','98堂','https://98t.la','中文成人交流社区','🔞'),
    ('adult','论坛','Avgle','https://avgle.com','成人视频聚合','🔞'),
    ('adult','漫画','Tsumino','https://www.tsumino.com','成人同人漫画','🔞'),
    ('adult','漫画','Hentaifox','https://hentaifox.com','成人动漫漫画','🔞'),
    ('adult','漫画','Simply Hentai','https://www.simply-hentai.com','成人漫画合集','🔞'),
    ('adult','直播','BongaCams','https://www.bongacams.com','成人直播社区','🔞'),
    ('adult','直播','MyFreeCams','https://www.myfreecams.com','免费成人直播','🔞'),
    ('adult','小说','第一版主','https://www.diyibanzhu.buzz','成人文学社区','🔞'),
    ('adult','小说','色中色','https://www.sexinsex.xyz','成人综合论坛','🔞'),
    ('adult','视频','YouJizz','https://www.youjizz.com','成人视频平台','🔞'),
    ('adult','视频','DrTuber','https://www.drtuber.com','成人视频分享','🔞'),
    ('adult','社区','Tube8','https://www.tube8.com','成人视频社区','🔞'),
    ('adult','图片','XArt','https://www.x-art.com','唯美成人写真','🔞'),
    ('adult','视频','Eporner','https://www.eporner.com','高清成人视频','🔞'),

    # ===== 游戏 6个 → 总计40 =====
    ('game','游戏资讯','VGtime','https://www.vgtime.com','主机游戏资讯评测','🎮'),
    ('game','游戏资讯','二柄','https://www.diershoubing.com','主机游戏App社区','🎮'),
    ('game','电竞社区','Max+','https://www.maxjia.com','DOTA2/CSGO数据','📊'),
    ('game','数字平台','WeGame','https://www.wegame.com.cn','腾讯游戏平台','🎮'),
    ('game','游戏Wiki','POE流亡编年史','https://poedb.tw','流放之路中文资料库','📖'),
    ('game','游戏Wiki','灰机Wiki','https://www.huijiwiki.com','中文游戏Wiki农场','📚'),

    # ===== 开发技术 补 =====
    ('dev','开发工具','Laravel News','https://laravel-news.com','Laravel生态资讯','📰'),
    ('dev','开发工具','React','https://react.dev','React官方文档','⚛️'),
    ('dev','开发工具','Vue.js','https://vuejs.org','Vue官方文档','💚'),
    ('dev','开发工具','Angular','https://angular.dev','Angular官方文档','🅰️'),
    ('dev','技术社区','CSDN','https://www.csdn.net','中国IT技术社区','🇨🇳'),

    # ===== 工具 补 =====
    ('tools','实用工具','Listary','https://www.listary.com','Windows快速搜索','🔍'),
    ('tools','实用工具','PowerToys','https://learn.microsoft.com/en-us/windows/powertoys','微软官方工具集','🧰'),
    ('tools','实用工具','Ditto','https://ditto-cp.sourceforge.io','剪贴板管理工具','📋'),
    ('tools','实用工具','AutoHotkey','https://www.autohotkey.com','Windows自动化脚本','⌨️'),
    ('tools','实用工具','思源笔记','https://b3log.org/siyuan','本地优先双向链接笔记','📝'),
    ('tools','在线转换','ImgBB','https://imgbb.com','免费图床托管','🖼️'),
    ('tools','在线转换','Sm.ms','https://sm.ms','免费图片外链图床','📷'),

    # ===== 办公 补 =====
    ('office','文档笔记','FlowUs','https://flowus.cn','国产Notion替代','📝'),
    ('office','文档笔记','Wolai','https://www.wolai.com','我来笔记协作平台','📓'),

    # ===== 学习 补 =====
    ('study','知识阅读','书格','https://www.shuge.org','古籍善本数字图书馆','📜'),
    ('study','知识阅读','Linux中国','https://linux.cn','Linux开源中文社区','🐧'),

    # ===== 设计 补 =====
    ('design','设计灵感','站酷','https://www.zcool.com.cn','中国设计师互动平台','🧊'),
    ('design','设计灵感','UI中国','https://www.ui.cn','中文UI设计社区','🎨'),

    # ===== 生活 补 =====
    ('life','求职招聘','58同城','https://www.58.com','中国分类信息平台','🏠'),
    ('life','求职招聘','赶集网','https://www.ganji.com','分类信息与招聘','📋'),

    # ===== 新闻 补 =====
    ('news','科技资讯','少数派','https://sspai.com','数字生活效率指南','🧰'),
    ('news','国际媒体','Bloomberg','https://www.bloomberg.com','彭博财经新闻','💹'),
]

added = 0
for cat, sub, title, url, desc, icon in ADD:
    d = url.split('/')[2]
    c.execute('SELECT id FROM bookmarks WHERE url LIKE %s', (f'%{d}%',))
    if c.fetchone(): continue
    c.execute('INSERT INTO bookmarks (title,url,description,icon,category,sub_category) VALUES (%s,%s,%s,%s,%s,%s)', (title,url,desc,icon,cat,sub))
    added += 1

conn.commit()
c.execute("SELECT category, COUNT(*) FROM bookmarks GROUP BY category ORDER BY count(*) DESC")
names = {'dev':'开发技术','study':'学习百科','media':'影音娱乐','social':'社交社区','office':'办公效率','tools':'网络工具','ai':'人工智能','commerce':'购物交易','life':'生活服务','news':'新闻资讯','adult':'成人内容','service':'便民服务','design':'设计资源','game':'游戏电竞'}
total = 0
for cat, cnt in c.fetchall():
    print(f'  {names.get(cat,cat)}: {cnt}')
    total += cnt
print(f'  总计: {total} | 新增: {added}')
conn.close()

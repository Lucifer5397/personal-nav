"""精确重新归类 - 基于 URL 域名映射到 6 大分类"""
import mysql.connector
from urllib.parse import urlparse

conn = mysql.connector.connect(host='localhost', user='root', password='123456', database='pj1', buffered=True)
c = conn.cursor()

# 新分类
c.execute('DELETE FROM categories')
for key, name, color in [
    ('dev', '开发技术', '#ff6b6b'),
    ('study', '学习百科', '#4ecdc4'),
    ('media', '影音娱乐', '#45b7d1'),
    ('social', '社交社区', '#96ceb4'),
    ('office', '办公效率', '#feca57'),
    ('tools', '网络工具', '#a78bfa'),
]:
    c.execute('INSERT INTO categories (cat_key, cat_name, cat_color) VALUES (%s,%s,%s)', (key, name, color))

# 域名 -> (大分类, 子分类)  精确映射
DOMAIN_MAP = {
    # ============ 开发技术 (dev) ============
    'github.com': ('dev', '代码托管'),
    'gitlab.com': ('dev', '代码托管'),
    'gitee.com': ('dev', '代码托管'),
    'stackoverflow.com': ('dev', '技术社区'),
    'stackexchange.com': ('dev', '技术社区'),
    'news.ycombinator.com': ('dev', '技术社区'),
    'dev.to': ('dev', '技术社区'),
    'csdn.net': ('dev', '技术社区'),
    'juejin.cn': ('dev', '技术社区'),
    'segmentfault.com': ('dev', '技术社区'),
    'v2ex.com': ('dev', '技术社区'),
    'vscode.dev': ('dev', '在线IDE'),
    'codepen.io': ('dev', '在线IDE'),
    'codesandbox.io': ('dev', '在线IDE'),
    'replit.com': ('dev', '在线IDE'),
    'postman.com': ('dev', '开发工具'),
    'jsonformatter.org': ('dev', '开发工具'),
    'curlconverter.com': ('dev', '开发工具'),
    'gchq.github.io': ('dev', '开发工具'),  # CyberChef
    'it-tools.tech': ('dev', '开发工具'),
    'app.quicktype.io': ('dev', '开发工具'),
    'jwt.io': ('dev', '开发工具'),
    'vercel.com': ('dev', '云平台'),
    'netlify.com': ('dev', '云平台'),
    'render.com': ('dev', '云平台'),
    'railway.app': ('dev', '云平台'),
    'firebase.google.com': ('dev', '云平台'),
    'supabase.com': ('dev', '云平台'),
    'planetscale.com': ('dev', '云平台'),
    'mongodb.com': ('dev', '云平台'),
    'heroku.com': ('dev', '云平台'),
    'digitalocean.com': ('dev', '云平台'),
    'cloudflare.com': ('dev', '云平台'),
    'npmjs.com': ('dev', '云平台'),
    'pypi.org': ('dev', '云平台'),
    'hub.docker.com': ('dev', '云平台'),

    # ============ 学习百科 (study) ============
    'coursera.org': ('study', '在线课程'),
    'edx.org': ('study', '在线课程'),
    'udemy.com': ('study', '在线课程'),
    'khanacademy.org': ('study', '在线课程'),
    'udacity.com': ('study', '在线课程'),
    'pluralsight.com': ('study', '在线课程'),
    'skillshare.com': ('study', '在线课程'),
    'brilliant.org': ('study', '在线课程'),
    'ocw.mit.edu': ('study', '在线课程'),
    'online.stanford.edu': ('study', '在线课程'),
    'online-learning.harvard.edu': ('study', '在线课程'),
    'icourse163.org': ('study', '在线课程'),
    'xuetangx.com': ('study', '在线课程'),
    'open.163.com': ('study', '在线课程'),
    'ke.qq.com': ('study', '在线课程'),
    'codecademy.com': ('dev', '编程学习'),
    'freecodecamp.org': ('dev', '编程学习'),
    'leetcode.com': ('dev', '编程刷题'),
    'hackerrank.com': ('dev', '编程刷题'),
    'codewars.com': ('dev', '编程刷题'),
    'w3schools.com': ('dev', '技术文档'),
    'developer.mozilla.org': ('dev', '技术文档'),
    'geeksforgeeks.org': ('dev', '技术文档'),
    'tutorialspoint.com': ('dev', '技术文档'),
    'duolingo.com': ('study', '语言学习'),
    'memrise.com': ('study', '语言学习'),
    'busuu.com': ('study', '语言学习'),
    'hellotalk.com': ('study', '语言学习'),
    'quizlet.com': ('study', '语言学习'),
    'wikipedia.org': ('study', '百科参考'),
    'britannica.com': ('study', '百科参考'),
    'baike.baidu.com': ('study', '百科参考'),
    'arxiv.org': ('study', '学术资源'),
    'scholar.google.com': ('study', '学术资源'),
    'researchgate.net': ('study', '学术资源'),
    'wolframalpha.com': ('study', '学术资源'),
    'desmos.com': ('study', '学术资源'),
    'geogebra.org': ('study', '学术资源'),
    'gutenberg.org': ('study', '知识阅读'),
    'goodreads.com': ('study', '知识阅读'),
    'scribd.com': ('study', '知识阅读'),
    'z-lib.io': ('study', '知识阅读'),
    'medium.com': ('study', '知识阅读'),
    'zhihu.com': ('study', '知识阅读'),
    'wenku.baidu.com': ('study', '知识阅读'),
    'doc88.com': ('study', '知识阅读'),

    # ============ 影音娱乐 (media) ============
    'youtube.com': ('media', '视频平台'),
    'bilibili.com': ('media', '视频平台'),
    'netflix.com': ('media', '视频平台'),
    'disneyplus.com': ('media', '视频平台'),
    'max.com': ('media', '视频平台'),
    'primevideo.com': ('media', '视频平台'),
    'hulu.com': ('media', '视频平台'),
    'vimeo.com': ('media', '视频平台'),
    'iqiyi.com': ('media', '视频平台'),
    'spotify.com': ('media', '音乐平台'),
    'music.apple.com': ('media', '音乐平台'),
    'music.youtube.com': ('media', '音乐平台'),
    'soundcloud.com': ('media', '音乐平台'),
    'bandcamp.com': ('media', '音乐平台'),
    'deezer.com': ('media', '音乐平台'),
    'tidal.com': ('media', '音乐平台'),
    'y.qq.com': ('media', '音乐平台'),
    'music.163.com': ('media', '音乐平台'),
    'kugou.com': ('media', '音乐平台'),
    'twitch.tv': ('media', '游戏直播'),
    'steampowered.com': ('media', '游戏直播'),
    'epicgames.com': ('media', '游戏直播'),
    'gog.com': ('media', '游戏直播'),
    'roblox.com': ('media', '游戏直播'),
    'ign.com': ('media', '游戏直播'),
    'gamespot.com': ('media', '游戏直播'),
    'huya.com': ('media', '游戏直播'),
    'douyu.com': ('media', '游戏直播'),
    'imdb.com': ('media', '电影评分'),
    'rottentomatoes.com': ('media', '电影评分'),
    'letterboxd.com': ('media', '电影评分'),
    'maoyan.com': ('media', '电影评分'),
    'taopiaopiao.com': ('media', '电影评分'),
    'crunchyroll.com': ('media', '动漫艺术'),
    'webtoons.com': ('media', '动漫艺术'),
    'pixiv.net': ('media', '动漫艺术'),
    'deviantart.com': ('media', '动漫艺术'),
    'artstation.com': ('media', '动漫艺术'),
    'qidian.com': ('media', '文学阅读'),
    'jjwxc.net': ('media', '文学阅读'),
    'fanqienovel.com': ('media', '文学阅读'),
    'tiktok.com': ('media', '短视频'),
    'douyin.com': ('media', '短视频'),
    'kuaishou.com': ('media', '短视频'),
    'acfun.cn': ('media', '短视频'),
    'kickstarter.com': ('media', '众筹赞助'),
    'patreon.com': ('media', '众筹赞助'),

    # ============ 社交社区 (social) ============
    'facebook.com': ('social', '全球社交'),
    'x.com': ('social', '全球社交'),
    'instagram.com': ('social', '全球社交'),
    'linkedin.com': ('social', '全球社交'),
    'snapchat.com': ('social', '全球社交'),
    'threads.net': ('social', '全球社交'),
    'bsky.app': ('social', '全球社交'),
    'mastodon.social': ('social', '全球社交'),
    'reddit.com': ('social', '社区论坛'),
    'tumblr.com': ('social', '社区论坛'),
    'producthunt.com': ('social', '社区论坛'),
    'hupu.com': ('social', '社区论坛'),
    'bbs.nga.cn': ('social', '社区论坛'),
    'guokr.com': ('social', '社区论坛'),
    'sspai.com': ('social', '社区论坛'),
    'coolapk.com': ('social', '社区论坛'),
    'quora.com': ('social', '社区论坛'),
    'telegram.org': ('social', '即时通讯'),
    'whatsapp.com': ('social', '即时通讯'),
    'signal.org': ('social', '即时通讯'),
    'wechat.com': ('social', '即时通讯'),
    'im.qq.com': ('social', '即时通讯'),
    'line.me': ('social', '即时通讯'),
    'kakaocorp.com': ('social', '即时通讯'),
    'weibo.com': ('social', '内容社区'),
    'xiaohongshu.com': ('social', '内容社区'),
    'tieba.baidu.com': ('social', '内容社区'),
    'douban.com': ('social', '内容社区'),
    'flickr.com': ('social', '内容社区'),
    '500px.com': ('social', '内容社区'),
    'pinterest.com': ('social', '内容社区'),
    'substack.com': ('social', '创作者平台'),
    'vk.com': ('social', '全球社交'),
    'nextdoor.com': ('social', '社区论坛'),
    'meetup.com': ('social', '社区论坛'),
    'xing.com': ('social', '全球社交'),

    # ============ 办公效率 (office) ============
    'notion.so': ('office', '文档笔记'),
    'evernote.com': ('office', '文档笔记'),
    'obsidian.md': ('office', '文档笔记'),
    'airtable.com': ('office', '文档笔记'),
    'trello.com': ('office', '项目管理'),
    'atlassian.com': ('office', '项目管理'),
    'asana.com': ('office', '项目管理'),
    'monday.com': ('office', '项目管理'),
    'linear.app': ('office', '项目管理'),
    'clickup.com': ('office', '项目管理'),
    'slack.com': ('office', '通讯协作'),
    'teams.microsoft.com': ('office', '通讯协作'),
    'zoom.us': ('office', '通讯协作'),
    'meet.google.com': ('office', '通讯协作'),
    'discord.com': ('office', '通讯协作'),
    'figma.com': ('office', '设计白板'),
    'canva.com': ('office', '设计白板'),
    'adobe.com': ('office', '设计白板'),
    'dribbble.com': ('office', '设计白板'),
    'behance.net': ('office', '设计白板'),
    'miro.com': ('office', '设计白板'),
    'excalidraw.com': ('office', '设计白板'),
    'app.diagrams.net': ('office', '设计白板'),
    'docs.google.com': ('office', '在线文档'),
    'workspace.google.com': ('office', '在线文档'),
    'office.com': ('office', '在线文档'),
    'docs.qq.com': ('office', '在线文档'),
    'shimo.im': ('office', '在线文档'),
    'yuque.com': ('office', '在线文档'),
    'feishu.cn': ('office', '在线文档'),
    'kdocs.cn': ('office', '在线文档'),
    'zapier.com': ('office', '流程自动化'),
    'make.com': ('office', '流程自动化'),
    'ifttt.com': ('office', '流程自动化'),
    'calendly.com': ('office', '日程管理'),
    'todoist.com': ('office', '日程管理'),
    'ticktick.com': ('office', '日程管理'),
    'calendar.google.com': ('office', '日程管理'),
    'calendar.notion.so': ('office', '日程管理'),
    'stripe.com': ('office', '商务工具'),
    'paypal.com': ('office', '商务工具'),
    'squareup.com': ('office', '商务工具'),
    'docusign.com': ('office', '商务工具'),
    'hellosign.com': ('office', '商务工具'),
    'grammarly.com': ('office', '写作翻译'),
    'deepl.com': ('office', '写作翻译'),
    'translate.google.com': ('office', '写作翻译'),

    # ============ 网络工具 (tools) ============
    'google.com': ('tools', '搜索引擎'),
    'bing.com': ('tools', '搜索引擎'),
    'duckduckgo.com': ('tools', '搜索引擎'),
    'baidu.com': ('tools', '搜索引擎'),
    'yandex.com': ('tools', '搜索引擎'),
    'cloudconvert.com': ('tools', '在线转换'),
    'convertio.co': ('tools', '在线转换'),
    'zamzar.com': ('tools', '在线转换'),
    'smallpdf.com': ('tools', '在线转换'),
    'ilovepdf.com': ('tools', '在线转换'),
    'tools.pdf24.org': ('tools', '在线转换'),
    'lightpdf.com': ('tools', '在线转换'),
    'online-convert.com': ('tools', '在线转换'),
    'freeconvert.com': ('tools', '在线转换'),
    'aconvert.com': ('tools', '在线转换'),
    'tinypng.com': ('tools', '在线转换'),
    'squoosh.app': ('tools', '在线转换'),
    'remove.bg': ('tools', '在线转换'),
    'photopea.com': ('tools', '在线转换'),
    'pixlr.com': ('tools', '在线转换'),
    'mail.google.com': ('tools', '免费邮箱'),
    'outlook.live.com': ('tools', '免费邮箱'),
    'proton.me': ('tools', '免费邮箱'),
    'mail.yahoo.com': ('tools', '免费邮箱'),
    'mail.163.com': ('tools', '免费邮箱'),
    'mail.qq.com': ('tools', '免费邮箱'),
    'zoho.com': ('tools', '免费邮箱'),
    'tuta.com': ('tools', '免费邮箱'),
    'gmx.com': ('tools', '免费邮箱'),
    'mail.com': ('tools', '免费邮箱'),
    'voice.google.com': ('tools', '虚拟电话'),
    'textnow.com': ('tools', '虚拟电话'),
    'textfree.us': ('tools', '虚拟电话'),
    'talkatone.com': ('tools', '虚拟电话'),
    'dingtone.me': ('tools', '虚拟电话'),
    'burnerapp.com': ('tools', '虚拟电话'),
    'hushed.com': ('tools', '虚拟电话'),
    'sonetel.com': ('tools', '虚拟电话'),
    'twilio.com': ('tools', '虚拟电话'),
    'receive-smss.com': ('tools', '虚拟电话'),
    'freephonenum.com': ('tools', '虚拟电话'),
    'ca01.fcvipaff.pro': ('tools', 'VPN代理'),
    'one.one.one.one': ('tools', 'VPN代理'),
    'protonvpn.com': ('tools', 'VPN代理'),
    'windscribe.com': ('tools', 'VPN代理'),
    'hide.me': ('tools', 'VPN代理'),
    'mullvad.net': ('tools', 'VPN代理'),
    'tunnelbear.com': ('tools', 'VPN代理'),
    'dropbox.com': ('tools', '云存储'),
    'drive.google.com': ('tools', '云存储'),
    'onedrive.live.com': ('tools', '云存储'),
    'box.com': ('tools', '云存储'),
    'mega.io': ('tools', '云存储'),
    'wetransfer.com': ('tools', '云存储'),
    'send-anywhere.com': ('tools', '云存储'),
    'cowtransfer.com': ('tools', '云存储'),
    'wenshushu.cn': ('tools', '云存储'),
    'terabox.com': ('tools', '云存储'),
    'icloud.com.cn': ('tools', '云存储'),
    'icloud.com': ('tools', '云存储'),
    'temp-mail.org': ('tools', '临时邮箱'),
    '10minutemail.net': ('tools', '临时邮箱'),
    'guerrillamail.com': ('tools', '临时邮箱'),
    'privnote.com': ('tools', '临时邮箱'),
    'time.is': ('tools', '实用工具'),
    'downdetector.com': ('tools', '实用工具'),
    'speedtest.net': ('tools', '实用工具'),
    'virustotal.com': ('tools', '实用工具'),
    'haveibeenpwned.com': ('tools', '实用工具'),
}

def get_domain(url):
    try:
        d = urlparse(url).netloc.lower()
        d = d.replace('www.', '')
        # 尝试匹配二级域名
        parts = d.split('.')
        # 先试完整域名，再试去掉最左段的
        for i in range(len(parts) - 1):
            candidate = '.'.join(parts[i:])
            if candidate in DOMAIN_MAP:
                return candidate
        return d
    except:
        return ''

# 更新
c.execute('SELECT id, title, url FROM bookmarks')
rows = c.fetchall()
updated = 0
unmatched = []
for bid, title, url in rows:
    domain = get_domain(url)
    if domain in DOMAIN_MAP:
        cat, sub = DOMAIN_MAP[domain]
        # 检查是否和现有一致
        c.execute('SELECT category, sub_category FROM bookmarks WHERE id=%s', (bid,))
        old_cat, old_sub = c.fetchone()
        if old_cat != cat or old_sub != sub:
            c.execute('UPDATE bookmarks SET category=%s, sub_category=%s WHERE id=%s', (cat, sub, bid))
            updated += 1
    else:
        unmatched.append((bid, title, url, domain))

conn.commit()

# 处理未匹配的
for bid, title, url, domain in unmatched:
    # 尝试关键词兜底
    t = (title + ' ' + url).lower()
    # 只在 6 大类中选
    if any(k in t for k in ['google', 'bing', 'baidu', '搜索', 'search']):
        c.execute('UPDATE bookmarks SET category=%s, sub_category=%s WHERE id=%s', ('tools', '搜索引擎', bid))
    elif any(k in t for k in ['vpn', '代理', 'proxy']):
        c.execute('UPDATE bookmarks SET category=%s, sub_category=%s WHERE id=%s', ('tools', 'VPN代理', bid))
    elif any(k in t for k in ['mail', '邮箱', 'email', 'gmail', 'outlook']):
        c.execute('UPDATE bookmarks SET category=%s, sub_category=%s WHERE id=%s', ('tools', '免费邮箱', bid))
    elif any(k in t for k in ['convert', 'pdf', '转换', 'compress', '压缩']):
        c.execute('UPDATE bookmarks SET category=%s, sub_category=%s WHERE id=%s', ('tools', '在线转换', bid))
    elif any(k in t for k in ['cloud', 'drive', 'storage', '云', '盘', 'dropbox']):
        c.execute('UPDATE bookmarks SET category=%s, sub_category=%s WHERE id=%s', ('tools', '云存储', bid))
    else:
        c.execute('UPDATE bookmarks SET category=%s, sub_category=%s WHERE id=%s', ('tools', '', bid))
    updated += 1

conn.commit()

# 统计
cat_names = {'dev':'开发技术','study':'学习百科','media':'影音娱乐','social':'社交社区','office':'办公效率','tools':'网络工具'}
print(f'更新: {updated} 条\n')
c.execute("SELECT category, COUNT(*) FROM bookmarks GROUP BY category ORDER BY category")
tot = 0
for cat, cnt in c.fetchall():
    print(f'  {cat_names[cat]:6s}: {cnt:3d}')
    tot += cnt
print(f'  {"总计":6s}: {tot:3d}')

print('\n=== 子分类明细 ===')
c.execute("SELECT category, sub_category, COUNT(*) FROM bookmarks WHERE sub_category!='' GROUP BY category, sub_category ORDER BY category, sub_category")
for cat, sub, cnt in c.fetchall():
    print(f'  [{cat_names[cat]}] {sub}: {cnt}')

conn.close()

"""给所有书签添加详细子分类"""
import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', password='123456', database='pj1', buffered=True)
c = conn.cursor()

# 添加子分类字段
try:
    c.execute('ALTER TABLE bookmarks ADD COLUMN sub_category VARCHAR(30) DEFAULT "" AFTER category')
    print('已添加 sub_category 字段')
except:
    print('sub_category 字段已存在')

# 子分类映射 (title/url关键字 -> 子分类名)
SUBCAT_RULES = {
    # ===== 工作 =====
    ('github','gitlab','gitee','bitbucket','stack overflow'): '代码托管',
    ('jira','trello','asana','monday','linear','clickup','basecamp','wrike'): '项目管理',
    ('slack','teams','zoom','meet','discord','loom'): '通讯协作',
    ('figma','canva','adobe','dribbble','behance','miro','excalidraw','sketch','photoshop'): '设计创意',
    ('google workspace','office','microsoft 365','dropbox','drive','onedrive','box','icloud'): '云服务',
    ('notion','evernote','obsidian','airtable','notion calendar','todoist','calendly','docs','document'): '文档笔记',
    ('stripe','paypal','square','docusign','hellosign'): '金融支付',
    ('zapier','make','ifttt','automate'): '流程自动化',
}
SUBCAT_RULES_STUDY = {
    ('coursera','edx','udemy','khan academy','udacity','skillshare','pluralsight','linkedin learning','brilliant','mit opencourseware','stanford online','harvard online'): '在线课程',
    ('codecademy','freecodecamp','leetcode','hackerrank','codewars','w3schools','mdn','geeksforgeeks','tutorialspoint'): '编程学习',
    ('duolingo','memrise','busuu','hellotalk','babbel','quizlet'): '语言学习',
    ('arxiv','google scholar','researchgate','wolfram alpha','desmos','geogebra'): '学术资源',
    ('百度百科','知乎','b站','中国大学mooc','学堂在线','豆瓣','百度文库','道客巴巴','网易公开课','腾讯课堂'): '中文平台',
    ('wikipedia','britannica','medium','goodreads','project gutenberg','z-library','scribd','dev.to'): '知识阅读',
}
SUBCAT_RULES_ENTERTAINMENT = {
    ('youtube','netflix','disney','max','hbo','prime video','hulu','vimeo','b站','爱奇艺','腾讯视频'): '视频平台',
    ('spotify','apple music','youtube music','soundcloud','bandcamp','deezer','tidal','qq音乐','网易云音乐','酷狗音乐'): '音乐平台',
    ('twitch','steam','epic games','gog','roblox','ign','gamespot','虎牙直播','斗鱼直播'): '游戏平台',
    ('crunchyroll','funimation','webtoon','pixiv','bilibili','acfun'): '动漫漫画',
    ('起点中文网','晋江文学城','番茄小说'): '文学阅读',
    ('tiktok','抖音','快手','虎牙','斗鱼','acfun'): '直播短视频',
    ('imdb','rotten tomatoes','letterboxd','猫眼电影','淘票票','豆瓣'): '影评票务',
    ('deviantart','artstation','pinterest','kickstarter','patreon'): '创意社区',
}
SUBCAT_RULES_SOCIAL = {
    ('facebook','twitter','x.com','instagram','linkedin','tiktok','snapchat','threads'): '全球社交',
    ('telegram','whatsapp','signal','微信','wechat','qq','line','kakaotalk'): '即时通讯',
    ('reddit','quora','贴吧','hacker news','product hunt','tumblr','v2ex','nga','虎扑'): '社区论坛',
    ('github','gitlab','dev.to','stack exchange','csdn','掘金','segmentfault','dribbble','v2ex'): '专业社区',
    ('pinterest','flickr','500px','instagram'): '图片社交',
    ('小红书','豆瓣','知乎','微博'): '中文社区',
    ('mastodon','bluesky','vk','nextdoor','meetup','xing','onlyfans','substack','medium','果壳','少数派','酷安'): '其他社交',
}
SUBCAT_RULES_TOOLS = {
    ('google','bing','duckduckgo','百度','yandex'): '搜索引擎',
    ('cloudconvert','convertio','zamzar','smallpdf','ilovepdf','pdf24','lightpdf','online-convert','freeconvert','aconvert','tinypng','squoosh'): '在线转换',
    ('gmail','outlook','proton mail','yahoo mail','163邮箱','qq邮箱','zoho mail','tuta','gmx','mail.com'): '免费邮箱',
    ('google voice','textnow','textfree','talkatone','dingtone','burner','hushed','sonetel','twilio','receive-sms','freephonenum'): '虚拟电话',
    ('肥猫云','warp','proton vpn','windscribe','hide.me','mullvad','tunnelbear'): 'VPN代理',
    ('canva','figma','adobe express','remove.bg','photopea','pixlr'): '设计工具',
    ('notion','google docs','腾讯文档','石墨文档','语雀','飞书文档','金山文档'): '办公笔记',
    ('postman','json formatter','curl','cyberchef','it-tools','quicktype','jwt'): '开发工具',
    ('dropbox','google drive','mega','wetransfer','send anywhere','奶牛快传','文叔叔','terabox','box'): '云存储',
    ('wolfram alpha','time.is','draw.io','excalidraw','cronitor','downdetector','speedtest','virustotal','have i been pwned','temp mail','10分钟邮箱','guerrilla mail','privnote','deepl','google translate','grammarly'): '实用工具',
}

def get_subcat(title, url, cat):
    """根据标题和URL匹配子分类"""
    text = (title + ' ' + url).lower()
    rules_map = {
        'work': SUBCAT_RULES,
        'study': SUBCAT_RULES_STUDY,
        'entertainment': SUBCAT_RULES_ENTERTAINMENT,
        'social': SUBCAT_RULES_SOCIAL,
        'tools': SUBCAT_RULES_TOOLS,
    }
    rules = rules_map.get(cat, {})
    for keywords, subcat in rules.items():
        for kw in keywords:
            if kw.lower() in text:
                return subcat
    return ''

# 更新所有书签
c.execute('SELECT id, title, url, category FROM bookmarks')
rows = c.fetchall()
updated = 0
for bid, title, url, cat in rows:
    sub = get_subcat(title, url, cat)
    if sub:
        c.execute('UPDATE bookmarks SET sub_category=%s WHERE id=%s', (sub, bid))
        updated += 1

conn.commit()
print(f'已更新 {updated} 条子分类')

# 统计
c.execute("SELECT category, sub_category, COUNT(*) FROM bookmarks GROUP BY category, sub_category ORDER BY category, sub_category")
rows = c.fetchall()
cats = {}
for cat, sub, cnt in rows:
    cats.setdefault(cat, []).append((sub, cnt))

for cat in ['work','study','entertainment','social','tools']:
    name = {'work':'工作','study':'学习','entertainment':'娱乐','social':'社交','tools':'工具'}[cat]
    print(f'\n【{name}】')
    for sub, cnt in cats.get(cat, []):
        label = sub if sub else '(未分类)'
        print(f'  {label}: {cnt}')

c.execute("SELECT COUNT(*) FROM bookmarks WHERE sub_category=''")
empty = c.fetchone()[0]
print(f'\n未分类: {empty} 条')
conn.close()

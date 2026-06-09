"""
从 Bing 爬取知名网站 + 知名站点补充，按分类批量导入 MySQL pj1 库
使用 scrapling StealthySession 长连接，绕过反爬
策略：先爬 Bing 取最新结果，不足 50 个的用知名站点库补足
"""
import time
import random
import re
import mysql.connector
from scrapling.fetchers import StealthySession

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'pj1',
    'charset': 'utf8mb4'
}

CATEGORY_QUERIES = {
    'work': [
        'best productivity tools websites',
        'top project management platforms',
        'popular developer tools and services',
        'best online collaboration tools',
        'software development websites list',
        '工作效率最高的工具网站推荐',
        '程序员开发者常用网站合集',
    ],
    'study': [
        'best online learning platforms',
        'free programming courses websites',
        'top educational websites for students',
        'best language learning sites',
        'online degree and certification platforms',
        '自学网站推荐合集',
        '免费在线学习平台推荐',
    ],
    'entertainment': [
        'most popular streaming services',
        'best music streaming platforms',
        'popular gaming websites online',
        'top video and movie sites',
        'entertainment sites worldwide',
        '最受欢迎的娱乐网站',
        '全球热门视频音乐平台',
    ],
    'social': [
        'most popular social media platforms worldwide',
        'best online forums and communities',
        'top messaging and chat platforms',
        'social networking sites list',
        '全球社交媒体平台',
        '热门论坛社区网站',
    ],
    'tools': [
        'best online tools for developers',
        'popular design and creative tools',
        'cloud storage and file sharing sites',
        'useful online converters and utilities',
        '最好的在线工具网站合集',
        '设计师常用网站推荐',
        '免费在线工具推荐',
    ],
}

# 知名站点补足库（Bing 爬不到足够时用）
KNOWN_SITES = {
    'work': [
        ('GitHub', 'https://github.com', '代码托管与协作平台', '🐙'),
        ('GitLab', 'https://gitlab.com', 'DevOps 生命周期工具', '🦊'),
        ('Bitbucket', 'https://bitbucket.org', 'Git 代码管理平台', '📦'),
        ('Jira', 'https://www.atlassian.com/software/jira', '项目跟踪与敏捷开发', '📋'),
        ('Trello', 'https://trello.com', '看板式项目管理工具', '📌'),
        ('Asana', 'https://asana.com', '团队任务与项目管理', '✅'),
        ('Monday.com', 'https://monday.com', '工作操作系统平台', '📊'),
        ('Slack', 'https://slack.com', '团队即时通讯协作', '💬'),
        ('Microsoft Teams', 'https://teams.microsoft.com', '微软团队协作平台', '🪟'),
        ('Zoom', 'https://zoom.us', '视频会议与协作', '📹'),
        ('Notion', 'https://www.notion.so', '全能笔记与知识库', '📝'),
        ('Confluence', 'https://www.atlassian.com/software/confluence', '团队知识管理', '📚'),
        ('Google Workspace', 'https://workspace.google.com', '谷歌办公套件', '📧'),
        ('Office 365', 'https://www.office.com', '微软办公云服务', '📄'),
        ('Dropbox', 'https://www.dropbox.com', '云存储与文件同步', '📦'),
        ('Google Drive', 'https://drive.google.com', '谷歌云存储服务', '💾'),
        ('OneDrive', 'https://onedrive.live.com', '微软云存储', '☁️'),
        ('Box', 'https://www.box.com', '企业云内容管理', '📁'),
        ('Figma', 'https://www.figma.com', '协作式 UI/UX 设计工具', '🎨'),
        ('Canva', 'https://www.canva.com', '在线图形设计平台', '🎨'),
        ('Adobe Creative Cloud', 'https://www.adobe.com/creativecloud', '创意设计套件', '🖌️'),
        ('Docker Hub', 'https://hub.docker.com', '容器镜像仓库', '🐳'),
        ('PyPI', 'https://pypi.org', 'Python 包索引', '🐍'),
        ('npm', 'https://www.npmjs.com', 'Node.js 包管理器', '📦'),
        ('Vercel', 'https://vercel.com', '前端部署与边缘计算', '▲'),
        ('Netlify', 'https://www.netlify.com', '现代 Web 部署平台', '🚀'),
        ('Cloudflare', 'https://www.cloudflare.com', 'CDN 与网络安全', '🛡️'),
        ('AWS Console', 'https://aws.amazon.com/console', '亚马逊云管理', '☁️'),
        ('Azure Portal', 'https://portal.azure.com', '微软云管理', '🪟'),
        ('Google Cloud Console', 'https://console.cloud.google.com', '谷歌云管理', '🔧'),
        ('Heroku', 'https://www.heroku.com', '云应用平台', '💜'),
        ('DigitalOcean', 'https://www.digitalocean.com', '开发者云服务', '🌊'),
        ('Linear', 'https://linear.app', '现代项目管理工具', '📐'),
        ('Basecamp', 'https://basecamp.com', '项目协作经典工具', '⛺'),
        ('ClickUp', 'https://clickup.com', '一体化生产力平台', '⚡'),
        ('Todoist', 'https://todoist.com', '跨平台任务管理', '📝'),
        ('Evernote', 'https://evernote.com', '笔记与知识整理', '📓'),
        ('Miro', 'https://miro.com', '在线白板协作', '🖊️'),
        ('Loom', 'https://www.loom.com', '视频消息录制工具', '🎥'),
        ('Calendly', 'https://calendly.com', '日程预约管理', '📅'),
        ('Zapier', 'https://zapier.com', '自动化工作流连接', '⚡'),
        ('IFTTT', 'https://ifttt.com', '条件触发自动化', '🔗'),
        ('Make', 'https://www.make.com', '可视化自动化集成', '🧩'),
        ('Airtable', 'https://airtable.com', '电子表格数据库混合', '📊'),
        ('Typeform', 'https://www.typeform.com', '互动式表单设计', '📋'),
        ('SurveyMonkey', 'https://www.surveymonkey.com', '在线问卷调查', '📊'),
        ('HubSpot', 'https://www.hubspot.com', 'CRM 与营销平台', '🎯'),
        ('Salesforce', 'https://www.salesforce.com', '企业 CRM 领导者', '☁️'),
        ('Stripe', 'https://stripe.com', '在线支付处理', '💳'),
        ('PayPal', 'https://www.paypal.com', '全球支付平台', '💰'),
    ],
    'study': [
        ('Coursera', 'https://www.coursera.org', '全球大学在线课程', '🎓'),
        ('edX', 'https://www.edx.org', '名校免费在线课程', '🏛️'),
        ('Udemy', 'https://www.udemy.com', '海量职业技能课程', '📚'),
        ('Khan Academy', 'https://www.khanacademy.org', '免费全龄教育平台', '🏫'),
        ('Udacity', 'https://www.udacity.com', '前沿技术纳米学位', '🎯'),
        ('Codecademy', 'https://www.codecademy.com', '交互式编程学习', '💻'),
        ('freeCodeCamp', 'https://www.freecodecamp.org', '免费编程学习社区', '🆓'),
        ('LeetCode', 'https://leetcode.com', '算法面试刷题平台', '🧩'),
        ('HackerRank', 'https://www.hackerrank.com', '编程挑战与面试', '🏆'),
        ('CodeWars', 'https://www.codewars.com', '编程道场实战练习', '⚔️'),
        ('Pluralsight', 'https://www.pluralsight.com', '技术技能进阶平台', '📖'),
        ('LinkedIn Learning', 'https://www.linkedin.com/learning', '职业技能视频课程', '🎬'),
        ('Skillshare', 'https://www.skillshare.com', '创意技能分享平台', '✨'),
        ('Duolingo', 'https://www.duolingo.com', '游戏化语言学习', '🦉'),
        ('Memrise', 'https://www.memrise.com', '语境化语言记忆', '🌍'),
        ('Busuu', 'https://www.busuu.com', '社交化语言学习', '🗣️'),
        ('Babbel', 'https://www.babbel.com', '实用对话语言课程', '💬'),
        ('Quizlet', 'https://quizlet.com', '闪卡记忆学习工具', '🃏'),
        ('Brilliant', 'https://brilliant.org', '互动数学科学学习', '💡'),
        ('MIT OpenCourseWare', 'https://ocw.mit.edu', '麻省理工免费课件', '🏛️'),
        ('Stanford Online', 'https://online.stanford.edu', '斯坦福在线课程', '🌲'),
        ('Harvard Online', 'https://online-learning.harvard.edu', '哈佛在线学习', '🎓'),
        ('W3Schools', 'https://www.w3schools.com', 'Web 技术参考教程', '🌐'),
        ('MDN Web Docs', 'https://developer.mozilla.org', 'Web 开发权威文档', '📘'),
        ('GeeksforGeeks', 'https://www.geeksforgeeks.org', '计算机科学知识库', '💡'),
        ('TutorialsPoint', 'https://www.tutorialspoint.com', '技术教程大全', '📗'),
        ('Stack Overflow', 'https://stackoverflow.com', '程序员问答社区', '❓'),
        ('Dev.to', 'https://dev.to', '开发者社区与博客', '✍️'),
        ('Medium', 'https://medium.com', '深度阅读与写作', '📝'),
        ('ArXiv', 'https://arxiv.org', '学术预印本论文库', '📄'),
        ('Google Scholar', 'https://scholar.google.com', '学术文献搜索', '📖'),
        ('ResearchGate', 'https://www.researchgate.net', '科研社交网络', '🔬'),
        ('Sci-Hub', 'https://sci-hub.se', '学术论文获取', '🔑'),
        ('Z-Library', 'https://z-lib.io', '电子书资源库', '📚'),
        ('Project Gutenberg', 'https://www.gutenberg.org', '免费公版电子书', '📕'),
        ('Open Library', 'https://openlibrary.org', '开放图书目录', '📚'),
        ('Scribd', 'https://www.scribd.com', '数字图书馆订阅', '📖'),
        ('Goodreads', 'https://www.goodreads.com', '读书社交与书评', '📚'),
        ('Wolfram Alpha', 'https://www.wolframalpha.com', '计算知识引擎', '🧮'),
        ('Desmos', 'https://www.desmos.com', '在线图形计算器', '📈'),
        ('GeoGebra', 'https://www.geogebra.org', '动态数学软件', '📐'),
        ('Chegg', 'https://www.chegg.com', '在线辅导与教科书', '📖'),
        ('Grammarly', 'https://www.grammarly.com', 'AI 写作助手', '✍️'),
        ('DeepL', 'https://www.deepl.com', '高质量 AI 翻译', '🌍'),
        ('Wikipedia', 'https://www.wikipedia.org', '自由的百科全书', '📖'),
        ('Britannica', 'https://www.britannica.com', '大英百科全书在线', '🏛️'),
        ('百度百科', 'https://baike.baidu.com', '中文百科全书', '📖'),
        ('知乎', 'https://www.zhihu.com', '中文知识问答社区', '❔'),
        ('B站', 'https://www.bilibili.com', '弹幕视频与学习社区', '📺'),
        ('中国大学MOOC', 'https://www.icourse163.org', '中国大学精品课程', '🇨🇳'),
    ],
    'entertainment': [
        ('YouTube', 'https://www.youtube.com', '全球视频分享平台', '🎬'),
        ('Netflix', 'https://www.netflix.com', '流媒体影视巨头', '📺'),
        ('Disney+', 'https://www.disneyplus.com', '迪士尼流媒体服务', '🏰'),
        ('HBO Max', 'https://www.max.com', 'HBO 流媒体平台', '🎥'),
        ('Amazon Prime Video', 'https://www.primevideo.com', '亚马逊影视流媒体', '🎬'),
        ('Hulu', 'https://www.hulu.com', '美国电视流媒体', '📺'),
        ('Spotify', 'https://open.spotify.com', '全球音乐流媒体', '🎵'),
        ('Apple Music', 'https://music.apple.com', '苹果音乐服务', '🍎'),
        ('YouTube Music', 'https://music.youtube.com', 'YouTube 音乐服务', '🎶'),
        ('SoundCloud', 'https://soundcloud.com', '独立音乐人平台', '☁️'),
        ('Bandcamp', 'https://bandcamp.com', '独立音乐直购', '🎸'),
        ('Tidal', 'https://tidal.com', '高保真音乐流媒体', '🎧'),
        ('Deezer', 'https://www.deezer.com', '全球音乐流媒体', '🎼'),
        ('Pandora', 'https://www.pandora.com', '个性化音乐电台', '📻'),
        ('Twitch', 'https://www.twitch.tv', '游戏直播平台', '🎮'),
        ('Steam', 'https://store.steampowered.com', 'PC 游戏最大平台', '🎮'),
        ('Epic Games', 'https://www.epicgames.com', '游戏与引擎平台', '🎮'),
        ('GOG.com', 'https://www.gog.com', '无 DRM 经典游戏', '🎮'),
        ('Roblox', 'https://www.roblox.com', '用户创作游戏平台', '🎲'),
        ('Minecraft', 'https://www.minecraft.net', '沙盒建造游戏', '⛏️'),
        ('IGN', 'https://www.ign.com', '游戏媒体与评测', '🎮'),
        ('GameSpot', 'https://www.gamespot.com', '游戏新闻与评测', '🕹️'),
        ('IMDb', 'https://www.imdb.com', '电影电视剧数据库', '🎬'),
        ('Rotten Tomatoes', 'https://www.rottentomatoes.com', '电影评分聚合', '🍅'),
        ('Letterboxd', 'https://letterboxd.com', '影迷社交日记', '🎬'),
        ('Crunchyroll', 'https://www.crunchyroll.com', '动漫流媒体平台', '🍥'),
        ('Funimation', 'https://www.funimation.com', '英文动漫配音平台', '🎌'),
        ('Webtoon', 'https://www.webtoons.com', '数字漫画平台', '📱'),
        ('Tapas', 'https://tapas.io', '网络漫画与小说', '📖'),
        ('Pixiv', 'https://www.pixiv.net', '插画创作社区', '🎨'),
        ('DeviantArt', 'https://www.deviantart.com', '艺术创作社区', '🖼️'),
        ('ArtStation', 'https://www.artstation.com', '专业艺术家展示平台', '🎨'),
        ('Dribbble', 'https://dribbble.com', '设计师作品展示', '🏀'),
        ('Behance', 'https://www.behance.net', 'Adobe 创意作品展示', '🖼️'),
        ('TikTok', 'https://www.tiktok.com', '短视频社交平台', '🎵'),
        ('Instagram', 'https://www.instagram.com', '图片社交分享', '📷'),
        ('Pinterest', 'https://www.pinterest.com', '灵感图片收藏', '📌'),
        ('Vimeo', 'https://vimeo.com', '高质量视频平台', '🎥'),
        ('Dailymotion', 'https://www.dailymotion.com', '全球视频分享', '📺'),
        ('Kickstarter', 'https://www.kickstarter.com', '创意众筹平台', '🚀'),
        ('Patreon', 'https://www.patreon.com', '创作者会员订阅', '💎'),
        ('豆瓣', 'https://www.douban.com', '中文书影音社区', '📚'),
        ('虎牙', 'https://www.huya.com', '中国游戏直播', '🐯'),
        ('斗鱼', 'https://www.douyu.com', '游戏电竞直播', '🐟'),
        ('抖音', 'https://www.douyin.com', '中国短视频平台', '🎵'),
        ('快手', 'https://www.kuaishou.com', '国民短视频社区', '⚡'),
        ('QQ音乐', 'https://y.qq.com', '腾讯音乐服务', '🎵'),
        ('网易云音乐', 'https://music.163.com', '音乐社区与播放器', '🎶'),
        ('起点中文网', 'https://www.qidian.com', '原创网络文学', '📖'),
        ('晋江文学城', 'https://www.jjwxc.net', '女性向文学原创', '📚'),
    ],
    'social': [
        ('Facebook', 'https://www.facebook.com', '全球社交网络', '👤'),
        ('X (Twitter)', 'https://x.com', '全球即时短消息', '🐦'),
        ('Instagram', 'https://www.instagram.com', '图片视频社交', '📷'),
        ('LinkedIn', 'https://www.linkedin.com', '职业社交网络', '💼'),
        ('TikTok', 'https://www.tiktok.com', '短视频社交', '🎵'),
        ('Snapchat', 'https://www.snapchat.com', '阅后即焚社交', '👻'),
        ('Reddit', 'https://www.reddit.com', '社交新闻聚合与论坛', '🦊'),
        ('Pinterest', 'https://www.pinterest.com', '图片灵感社交', '📌'),
        ('Discord', 'https://discord.com', '游戏社区语音聊天', '🎮'),
        ('Telegram', 'https://telegram.org', '加密即时通讯', '✈️'),
        ('WhatsApp', 'https://www.whatsapp.com', '全球即时通讯', '💬'),
        ('Signal', 'https://signal.org', '隐私加密通讯', '🔒'),
        ('WeChat', 'https://www.wechat.com', '微信全球版', '💬'),
        ('LINE', 'https://line.me', '日韩主流通讯', '🟢'),
        ('KakaoTalk', 'https://www.kakaocorp.com', '韩国国民通讯', '💛'),
        ('Viber', 'https://www.viber.com', '免费通讯应用', '📞'),
        ('Skype', 'https://www.skype.com', '微软视频通讯', '📹'),
        ('Quora', 'https://www.quora.com', '知识问答社区', '❓'),
        ('Tumblr', 'https://www.tumblr.com', '轻博客社交', '📝'),
        ('Mastodon', 'https://mastodon.social', '去中心化社交网络', '🐘'),
        ('Bluesky', 'https://bsky.app', '去中心化社交新星', '☁️'),
        ('Threads', 'https://www.threads.net', 'Instagram 文字社交', '🧵'),
        ('Nextdoor', 'https://nextdoor.com', '邻里社区社交', '🏘️'),
        ('Meetup', 'https://www.meetup.com', '线下兴趣聚会', '🤝'),
        ('VK', 'https://vk.com', '俄罗斯最大社交网络', '🇷🇺'),
        ('Weibo', 'https://weibo.com', '新浪微博', '🔴'),
        ('知乎', 'https://www.zhihu.com', '中文知识问答', '❔'),
        ('豆瓣', 'https://www.douban.com', '中文兴趣社区', '📚'),
        ('贴吧', 'https://tieba.baidu.com', '百度兴趣贴吧', '📌'),
        ('小红书', 'https://www.xiaohongshu.com', '生活方式社区', '📕'),
        ('Hacker News', 'https://news.ycombinator.com', '科技创业社区', '🔷'),
        ('Product Hunt', 'https://www.producthunt.com', '新产品发现社区', '🚀'),
        ('Lobsters', 'https://lobste.rs', '技术链接聚合', '🦞'),
        ('Stack Exchange', 'https://stackexchange.com', '问答社区网络', '🔗'),
        ('4chan', 'https://www.4chan.org', '匿名贴图论坛', '🍀'),
        ('Flickr', 'https://www.flickr.com', '照片分享社区', '📷'),
        ('500px', 'https://500px.com', '摄影作品展示', '📸'),
        ('Medium', 'https://medium.com', '深度写作平台', '✍️'),
        ('Substack', 'https://substack.com', ' newsletter 订阅平台', '📧'),
        ('Beehiiv', 'https://www.beehiiv.com', '创作者通讯平台', '🐝'),
        ('OnlyFans', 'https://onlyfans.com', '创作者付费订阅', '🔞'),
        ('Cameo', 'https://www.cameo.com', '名人定制视频', '🌟'),
        ('LinkedIn', 'https://www.linkedin.com', '职业社交', '💼'),
        ('Xing', 'https://www.xing.com', '德国职业社交', '🟢'),
        ('ResearchGate', 'https://www.researchgate.net', '科研人员社交', '🔬'),
        ('Academia.edu', 'https://www.academia.edu', '学术论文分享', '📄'),
        ('GitHub', 'https://github.com', '开发者社交协作', '🐙'),
        ('GitLab', 'https://gitlab.com', '开发者 DevOps 平台', '🦊'),
        ('Dev.to', 'https://dev.to', '开发者写作社区', '✍️'),
        ('Dribbble', 'https://dribbble.com', '设计师社交', '🏀'),
    ],
    'tools': [
        ('Google', 'https://www.google.com', '全球搜索引擎', '🔍'),
        ('Bing', 'https://www.bing.com', '微软搜索引擎', '🔎'),
        ('DuckDuckGo', 'https://duckduckgo.com', '隐私搜索引擎', '🦆'),
        ('Baidu', 'https://www.baidu.com', '中文搜索引擎', '🔍'),
        ('Google Translate', 'https://translate.google.com', '谷歌翻译服务', '🌍'),
        ('DeepL', 'https://www.deepl.com', 'AI 高质量翻译', '🌍'),
        ('Grammarly', 'https://www.grammarly.com', 'AI 英文写作助手', '✍️'),
        ('Canva', 'https://www.canva.com', '在线设计平台', '🎨'),
        ('Figma', 'https://www.figma.com', '协作式设计工具', '🎨'),
        ('Adobe Express', 'https://www.adobe.com/express', 'Adobe 免费设计工具', '🖌️'),
        ('Remove.bg', 'https://www.remove.bg', 'AI 一键去背景', '🖼️'),
        ('TinyPNG', 'https://tinypng.com', '图片智能压缩', '🗜️'),
        ('Squoosh', 'https://squoosh.app', '谷歌图片优化工具', '📷'),
        ('Excalidraw', 'https://excalidraw.com', '手绘风格白板工具', '✏️'),
        ('Draw.io', 'https://app.diagrams.net', '免费在线绘图', '📐'),
        ('Lucidchart', 'https://www.lucidchart.com', '在线流程图工具', '📊'),
        ('Miro', 'https://miro.com', '在线协作白板', '🖊️'),
        ('Notion', 'https://www.notion.so', '全能笔记与知识库', '📝'),
        ('Obsidian', 'https://obsidian.md', '本地优先知识管理', '💎'),
        ('Evernote', 'https://evernote.com', '跨平台笔记应用', '📓'),
        ('OneNote', 'https://www.onenote.com', '微软数字笔记本', '📒'),
        ('Google Keep', 'https://keep.google.com', '谷歌轻量笔记', '📝'),
        ('Bear', 'https://bear.app', '优雅 Markdown 笔记', '🐻'),
        ('Trello', 'https://trello.com', '看板式任务管理', '📌'),
        ('Todoist', 'https://todoist.com', '跨平台待办事项', '✅'),
        ('TickTick', 'https://ticktick.com', '时间管理日程', '⏰'),
        ('Calendly', 'https://calendly.com', '在线预约日程', '📅'),
        ('Google Calendar', 'https://calendar.google.com', '谷歌日历', '📅'),
        ('IFTTT', 'https://ifttt.com', '条件触发自动化', '🔗'),
        ('Zapier', 'https://zapier.com', '应用自动化集成', '⚡'),
        ('Make', 'https://www.make.com', '可视化工作流', '🧩'),
        ('n8n', 'https://n8n.io', '开源工作流自动化', '🔧'),
        ('Postman', 'https://www.postman.com', 'API 开发测试工具', '📮'),
        ('Insomnia', 'https://insomnia.rest', 'REST/GraphQL 客户端', '🌙'),
        ('JSON Formatter', 'https://jsonformatter.org', 'JSON 在线格式化', '📋'),
        ('CodePen', 'https://codepen.io', '前端代码沙盒', '✏️'),
        ('JSFiddle', 'https://jsfiddle.net', '在线 JS 编辑器', '🎻'),
        ('Replit', 'https://replit.com', '在线编程环境', '🔄'),
        ('CodeSandbox', 'https://codesandbox.io', 'Web 开发沙盒', '📦'),
        ('GitHub Codespaces', 'https://github.com/features/codespaces', '云端开发环境', '☁️'),
        ('Vercel', 'https://vercel.com', '前端部署平台', '▲'),
        ('Netlify', 'https://www.netlify.com', '现代 Web 部署', '🚀'),
        ('Render', 'https://render.com', '全栈云部署', '⚡'),
        ('Railway', 'https://railway.app', '开发者云平台', '🚂'),
        ('Supabase', 'https://supabase.com', '开源 Firebase 替代', '🟢'),
        ('Firebase', 'https://firebase.google.com', '谷歌后端即服务', '🔥'),
        ('PlanetScale', 'https://planetscale.com', 'MySQL 云平台', '🗄️'),
        ('MongoDB Atlas', 'https://www.mongodb.com/atlas', '云端 MongoDB', '🍃'),
        ('Notion', 'https://www.notion.so', '全能笔记协作', '📝'),
        ('Slack', 'https://slack.com', '团队通讯协作', '💬'),
    ],
}

def get_db():
    conn = mysql.connector.connect(**DB_CONFIG, buffered=True)
    return conn

def url_to_domain(url):
    m = re.search(r'https?://([^/]+)', url)
    return m.group(1).lower().replace('www.', '') if m else url.lower()

def already_exists(cursor, domain):
    cursor.execute('SELECT id FROM bookmarks WHERE url LIKE %s', (f'%{domain}%',))
    row = cursor.fetchone()
    return row is not None

def crawl_bing(session, query, seen_domains, cursor, cat_key):
    """用 StealthySession 搜一次 Bing，提取结果"""
    results = []
    search_url = f'https://www.bing.com/search?q={query}&count=30'

    try:
        page = session.fetch(search_url, google_search=False, wait=2500)
        items = page.css('li.b_algo')

        for item in items:
            title_els = item.css('h2 a')
            desc_els = item.css('.b_caption p')

            if not title_els:
                continue
            title_el = title_els[0]

            title = title_el.css('::text').get() or title_el.text_content().strip()
            url = title_el.attrib.get('href', '') if hasattr(title_el, 'attrib') else title_el.get('href', '')
            desc = desc_els[0].css('::text').get() if desc_els else ''

            if not title or not url:
                continue
            if len(title) < 3 or len(url) < 10:
                continue
            if any(bad in url.lower() for bad in ['bing.com', 'microsoft.com/search', '/search?', 'login.', 'signin']):
                continue

            domain = url_to_domain(url)
            if domain in seen_domains or already_exists(cursor, domain):
                continue
            seen_domains.add(domain)

            icon = '🌐'
            kmap = {'github': '🐙','google': '🔍','youtube': '🎬','twitter': '🐦','x.com': '🐦','reddit': '🦊','linkedin': '💼','stack': '❓','spotify': '🎵','notion': '📝','figma': '🎨','coursera': '🎓','udemy': '📚','netflix': '📺','discord': '💬','slack': '💬','zoom': '📹','dropbox': '📦','canva': '🎨','wikipedia': '📖','amazon': '🛒','apple': '🍎','microsoft': '🪟','adobe': '🖌️','gitlab': '🦊','duckduckgo':'🦆','twitch':'🎮','steam':'🎮','tiktok':'🎵','telegram':'✈️','whatsapp':'💬','pinterest':'📌','quora':'❓','medium':'✍️'}
            for k, v in kmap.items():
                if k in domain:
                    icon = v
                    break

            results.append({
                'title': title.strip()[:100],
                'url': url.strip()[:500],
                'description': desc.strip()[:200] or title.strip(),
                'icon': icon,
                'category': cat_key,
            })
    except Exception as e:
        print(f'      搜索出错: {e}')

    return results

def main():
    print('=== Bing 爬虫 + 知名站点入库 ===\n')

    cat_names = {'work': '工作', 'study': '学习', 'entertainment': '娱乐', 'social': '社交', 'tools': '工具'}
    total_added = 0

    print('启动隐身浏览器 session (保持连接)...')
    with StealthySession(headless=True) as session:
        for cat_key, queries in CATEGORY_QUERIES.items():
            print(f'\n[分类: {cat_names[cat_key]} ({cat_key}) 目标: 50个]')
            print('-' * 50)

            # Step 1: 从 Bing 爬取
            conn = get_db()
            cursor = conn.cursor()
            seen_domains = set()
            crawled = []

            for i, query in enumerate(queries):
                if len(crawled) >= 40:  # 爬够 40 个就停，剩下的用补足库
                    break
                wait = random.uniform(2.5, 4.5)
                print(f'  [{i+1}/{len(queries)}] 搜索: "{query}" (等待 {wait:.1f}s)...')
                time.sleep(wait)
                new = crawl_bing(session, query, seen_domains, cursor, cat_key)
                crawled.extend(new)
                print(f'       获得 {len(new)} 条新结果 (累计 {len(crawled)})')

                if len(crawled) >= 40:
                    break

            # Step 2: 不足 50 个，用知名站点补足（重新开 db 连接）
            if len(crawled) < 50 and cat_key in KNOWN_SITES:
                print(f'  Bing 共得 {len(crawled)} 个，从知名站点库补足...')
                conn2 = get_db()
                cur2 = conn2.cursor()
                for title, url, desc, icon in KNOWN_SITES[cat_key]:
                    if len(crawled) >= 50:
                        break
                    domain = url_to_domain(url)
                    if domain in seen_domains or already_exists(cur2, domain):
                        continue
                    seen_domains.add(domain)
                    crawled.append({
                        'title': title, 'url': url, 'description': desc,
                        'icon': icon, 'category': cat_key,
                    })
                print(f'  补足后共 {len(crawled)} 个')
                conn2.close()

            conn.close()

            # Step 3: 写入数据库
            if crawled:
                conn = get_db()
                cur = conn.cursor()
                added = 0
                for r in crawled[:50]:
                    try:
                        cur.execute(
                            'INSERT IGNORE INTO bookmarks (title, url, description, icon, category) VALUES (%s,%s,%s,%s,%s)',
                            (r['title'], r['url'], r['description'], r['icon'], r['category'])
                        )
                        if cur.rowcount > 0:
                            added += 1
                    except Exception as e:
                        print(f'  插入失败: {r["title"]} - {e}')
                conn.commit()
                conn.close()
                total_added += added
                print(f'  >>> 本分类写入 {added} 个书签')

            # 分类间隔
            cats_list = list(CATEGORY_QUERIES.keys())
            if cat_key != cats_list[-1]:
                w = random.uniform(4, 7)
                print(f'  分类间隔等待 {w:.1f}s ...')
                time.sleep(w)

    # 最终统计
    conn = get_db()
    cursor = conn.cursor()
    print('\n=== 最终统计 ===')
    for cat_key, name in cat_names.items():
        cursor.execute('SELECT COUNT(*) FROM bookmarks WHERE category = %s', (cat_key,))
        print(f'  {name}: {cursor.fetchone()[0]} 个')
    cursor.execute('SELECT COUNT(*) FROM bookmarks')
    print(f'  总计: {cursor.fetchone()[0]} 个')
    conn.close()
    print(f'\n本次新增: {total_added} 个')

if __name__ == '__main__':
    main()

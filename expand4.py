import mysql.connector
conn=mysql.connector.connect(host='localhost',user='root',password='123456',database='pj1',buffered=True)
c=conn.cursor()
sites=[
('dev','技术社区','RubyGems','https://rubygems.org','Ruby包仓库','💎'),
('dev','技术社区','Crates.io','https://crates.io','Rust包仓库','📦'),
('dev','技术社区','NuGet','https://www.nuget.org','.NET包管理','📦'),
('dev','技术社区','Mozilla','https://www.mozilla.org','开源浏览器组织','🦊'),
('dev','技术社区','Chromium','https://www.chromium.org','开源浏览器项目','🔵'),
('dev','技术社区','WebKit','https://webkit.org','Safari引擎','🧭'),
('dev','技术社区','Electron','https://www.electronjs.org','桌面应用框架','⚛️'),
('dev','技术社区','Tauri','https://tauri.app','轻量桌面框架','🦀'),
('dev','技术社区','Apache','https://httpd.apache.org','经典Web服务器','🪶'),
('study','在线课程','Code.org','https://code.org','儿童编程启蒙','👶'),
('study','在线课程','Scratch','https://scratch.mit.edu','MIT图形编程','🐱'),
('study','学术资源','IEEE Xplore','https://ieeexplore.ieee.org','IEEE论文库','📡'),
('study','学术资源','ScienceDirect','https://www.sciencedirect.com','Elsevier论文','🔬'),
('study','学术资源','SpringerLink','https://link.springer.com','Springer论文','📄'),
('study','语言学习','LingQ','https://www.lingq.com','沉浸语言学习','🌍'),
('study','语言学习','Italki','https://www.italki.com','在线语言教师','🗣️'),
('media','音乐平台','Last.fm','https://www.last.fm','音乐记录推荐','🎧'),
('media','文学阅读','Wattpad','https://www.wattpad.com','全球小说社区','📖'),
('social','即时通讯','Skype','https://www.skype.com','微软视频通话','📹'),
('social','即时通讯','Viber','https://www.viber.com','免费国际通话','📞'),
('office','文档笔记','Notability','https://notability.com','iPad手写笔记','✏️'),
('office','文档笔记','GoodNotes','https://www.goodnotes.com','数字笔记','📓'),
('office','写作翻译','QuillBot','https://quillbot.com','AI英文改写','✍️'),
('office','写作翻译','Linguee','https://www.linguee.com','例句翻译词典','📖'),
('office','设计白板','Whimsical','https://whimsical.com','极简协作绘图','✨'),
('office','设计白板','Tldraw','https://www.tldraw.com','开源白板','✏️'),
('tools','搜索引擎','Yahoo','https://www.yahoo.com','老牌门户搜索','🟣'),
('tools','搜索引擎','Ask.com','https://www.ask.com','问答式搜索','❓'),
('tools','实用工具','FlightRadar24','https://www.flightradar24.com','全球航班追踪','✈️'),
('tools','实用工具','MarineTraffic','https://www.marinetraffic.com','船舶追踪','🚢'),
('tools','实用工具','Radio Garden','https://radio.garden','全球电台','📻'),
('tools','实用工具','Rainmeter','https://www.rainmeter.net','桌面美化','🖥️'),
('tools','实用工具','ShareX','https://getsharex.com','开源截图录屏','📸'),
('tools','实用工具','OBS Studio','https://obsproject.com','开源直播录屏','🎥'),
('tools','实用工具','HandBrake','https://handbrake.fr','开源视频转码','🎬'),
('tools','实用工具','7-Zip','https://www.7-zip.org','开源压缩软件','🗜️'),
('tools','实用工具','KeePass','https://keepass.info','开源密码管理','🔑'),
('tools','实用工具','Bitwarden','https://bitwarden.com','开源密码管理器','🔐'),
('tools','实用工具','1Password','https://1password.com','商业密码管理','🔐'),
('commerce','中国电商','1688','https://www.1688.com','阿里批发采购','🏭'),
('commerce','中国电商','义乌购','https://www.yiwugo.com','小商品批发','🛒'),
('life','金融理财','京东金融','https://jr.jd.com','京东金融服务','💰'),
('life','金融理财','度小满','https://www.duxiaoman.com','百度金融服务','💳'),
('life','出行旅游','驴妈妈','https://www.lvmama.com','自助游服务','🐴'),
('life','求职招聘','实习僧','https://www.shixiseng.com','大学生实习','🎓'),
('life','求职招聘','脉脉','https://maimai.cn','职场社交招聘','🤝'),
('life','餐饮外卖','瑞幸咖啡','https://www.luckincoffee.com','新零售咖啡','☕'),
('life','餐饮外卖','星巴克','https://www.starbucks.com.cn','咖啡连锁','☕'),
('news','综合资讯','观察者网','https://www.guancha.cn','时政评论','👁️'),
('news','综合资讯','财新网','https://www.caixin.com','财经新闻','💰'),
('news','综合资讯','第一财经','https://www.yicai.com','专业财经','📊'),
('news','科技资讯','雷锋网','https://www.leiphone.com','智能硬件','🤖'),
('news','科技资讯','爱范儿','https://www.ifanr.com','数字生活','📱'),
('news','科技资讯','驱动之家','https://www.mydrivers.com','硬件驱动','🖥️'),
('gov','政务服务','海关总署','https://www.customs.gov.cn','海关服务','🛃'),
('gov','政务服务','外交部','https://www.fmprc.gov.cn','外交服务','🌏'),
('gov','政务服务','司法部','https://www.moj.gov.cn','法律服务','⚖️'),
('gov','政务服务','气象局','https://www.cma.gov.cn','气象服务','🌤️'),
('health','问诊挂号','平安好医生','https://www.jk.cn','在线医疗','👨‍⚕️'),
('health','运动健身','Fitbit','https://www.fitbit.com','健康追踪','⌚'),
('health','运动健身','MyFitnessPal','https://www.myfitnesspal.com','卡路里计算','🥗'),
('health','运动健身','Nike Training','https://www.nike.com/ntc-app','Nike健身','🏋️'),
('adult','社区','Fc2','https://fc2.com','日本综合平台','🔞'),
]
added=0
for cat,sub,title,url,desc,icon in sites:
    d=url.split('/')[2]
    c.execute('SELECT id FROM bookmarks WHERE url LIKE %s',(f'%{d}%',))
    if c.fetchone(): continue
    c.execute('INSERT INTO bookmarks (title,url,description,icon,category,sub_category) VALUES (%s,%s,%s,%s,%s,%s)',(title,url,desc,icon,cat,sub))
    added+=1
conn.commit()
c.execute('SELECT COUNT(*) FROM bookmarks')
print(f'Total: {c.fetchone()[0]} | New: {added}')
conn.close()

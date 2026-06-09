"""第二波扩充：补到1000+"""
import mysql.connector
DB = {'host': 'localhost', 'user': 'root', 'password': '123456', 'database': 'pj1', 'charset': 'utf8mb4', 'buffered': True}

SITES = [
    # ===== AI 补充 =====
    ('ai','大模型对话','秘塔AI','https://metaso.cn','学术检索AI助手','🔬'),
    ('ai','大模型对话','天工AI','https://www.tiangong.cn','昆仑万维大模型','⚡'),
    ('ai','大模型对话','海螺AI','https://hailuoai.com','MiniMax大模型','🐚'),
    ('ai','AI编程','Devin','https://devin.ai','AI软件工程师代理','🤖'),
    ('ai','AI编程','Sourcegraph Cody','https://sourcegraph.com/cody','代码理解AI助手','🔍'),
    ('ai','AI编程','Pieces','https://pieces.app','AI代码片段管理','🧩'),
    ('ai','AI图像','Ideogram','https://ideogram.ai','AI文字logo生成','🔤'),
    ('ai','AI图像','Clipdrop','https://clipdrop.co','AI图像编辑套件','✂️'),
    ('ai','AI图像','Magnific','https://magnific.ai','AI图像超分放大','🔍'),
    ('ai','AI视频','Kling','https://kling.kuaishou.com','快手可灵AI视频','🎬'),
    ('ai','AI音频','Fish Audio','https://fish.audio','开源AI语音合成','🐟'),
    ('ai','AI音频','Audiobox','https://audiobox.meta.com','Meta AI音频生成','📦'),
    ('ai','开放平台','硅基流动','https://siliconflow.cn','国产大模型推理云','☁️'),
    ('ai','开放平台','OpenRouter','https://openrouter.ai','多模型统一API路由','🔀'),
    ('ai','开放平台','Vercel AI SDK','https://sdk.vercel.ai','AI应用开发SDK','▲'),

    # ===== 开发技术 补充 =====
    ('dev','云平台','Koyeb','https://www.koyeb.com','全球部署Serverless','🌍'),
    ('dev','云平台','Fly.io','https://fly.io','边缘容器部署平台','✈️'),
    ('dev','云平台','Coolify','https://coolify.io','开源Vercel替代','❄️'),
    ('dev','云平台','Dokploy','https://dokploy.com','开源Docker部署','🐳'),
    ('dev','开发工具','Vite','https://vitejs.dev','下一代前端构建工具','⚡'),
    ('dev','开发工具','TurboRepo','https://turbo.build','高性能Monorepo工具','🏎️'),
    ('dev','开发工具','Vitest','https://vitest.dev','Vite原生测试框架','✅'),
    ('dev','开发工具','Playwright','https://playwright.dev','微软自动化测试框架','🎭'),
    ('dev','开发工具','Prisma','https://www.prisma.io','Node.js ORM 工具','🔺'),
    ('dev','开发工具','Drizzle','https://orm.drizzle.team','TypeScript轻量ORM','💧'),
    ('dev','开发工具','Docker','https://www.docker.com','容器化平台官网','🐳'),
    ('dev','开发工具','Kubernetes','https://kubernetes.io','容器编排平台','☸️'),
    ('dev','开发工具','Terraform','https://www.terraform.io','基础设施即代码','🏗️'),
    ('dev','开发工具','Ansible','https://www.ansible.com','自动化运维工具','🤖'),
    ('dev','技术社区','Crunchbase','https://www.crunchbase.com','创业公司数据库','📊'),
    ('dev','技术社区','HackerOne','https://www.hackerone.com','漏洞赏金平台','🪲'),
    ('dev','技术社区','OWASP','https://owasp.org','Web应用安全标准','🛡️'),

    # ===== 学习百科 补充 =====
    ('study','百科参考','360百科','https://baike.so.com','360百科知识平台','📖'),
    ('study','百科参考','MBA智库百科','https://wiki.mbalib.com','经管知识百科','💼'),
    ('study','百科参考','医学百科','https://www.wiki8.com','中文医学知识库','🏥'),
    ('study','在线课程','网易云课堂','https://study.163.com','职业技能在线教育','☁️'),
    ('study','在线课程','51CTO学堂','https://edu.51cto.com','IT技术培训平台','💻'),
    ('study','在线课程','CSDN学院','https://edu.csdn.net','程序员技能学习','🎓'),
    ('study','在线课程','B站课堂','https://www.bilibili.com/cheese','哔哩哔哩付费课程','📺'),
    ('study','语言学习','沪江网校','https://class.hujiang.com','多语种在线教育','📖'),

    # ===== 影音娱乐 补充 =====
    ('media','视频平台','MangoTV国际','https://www.mangotv.com','芒果TV国际版','🥭'),
    ('media','视频平台','iQIYI国际','https://www.iq.com','爱奇艺国际版','▶️'),
    ('media','音乐平台','酷我音乐','https://www.kuwo.cn','老牌数字音乐平台','🎤'),
    ('media','音乐平台','千千音乐','https://music.taihe.com','太合音乐集团','🎵'),
    ('media','音乐平台','荔枝FM','https://www.lizhi.fm','声音互动社区','🎙️'),
    ('media','音乐平台','喜马拉雅','https://www.ximalaya.com','音频分享与有声书','📻'),
    ('media','游戏直播','Nintendo', 'https://www.nintendo.com','任天堂官方主页','🎮'),
    ('media','游戏直播','PlayStation','https://www.playstation.com','索尼PlayStation官网','🎮'),
    ('media','游戏直播','Xbox','https://www.xbox.com','微软Xbox游戏官网','🎮'),
    ('media','游戏直播','小黑盒','https://www.xiaoheihe.cn','Steam玩家社区','📦'),
    ('media','文学阅读','LOFTER','https://www.lofter.com','网易轻博客创作社区','✍️'),
    ('media','电影评分','烂番茄','https://www.rottentomatoes.com','好莱坞影评聚合','🍅'),

    # ===== 社交社区 补充 =====
    ('social','内容社区','知乎专栏','https://zhuanlan.zhihu.com','知乎创作者专栏','✍️'),
    ('social','内容社区','简书','https://www.jianshu.com','中文创作阅读平台','📝'),
    ('social','社区论坛','McBBS','https://www.mcbbs.net','中文Minecraft社区','⛏️'),
    ('social','社区论坛','吾爱破解','https://www.52pojie.cn','软件逆向安全论坛','🔓'),
    ('social','社区论坛','全球主机','https://hostloc.com','主机与网络交流','🌐'),
    ('social','社区论坛','恩山论坛','https://www.right.com.cn','路由器固件论坛','📡'),

    # ===== 办公效率 补充 =====
    ('office','商务工具','Tower','https://tower.im','轻量级项目管理','🗼'),
    ('office','商务工具','Teambition','https://www.teambition.com','阿里团队协作工具','🤝'),
    ('office','在线文档','腾讯文档','https://docs.qq.com','腾讯协作办公','📃'),
    ('office','在线文档','钉钉文档','https://www.dingtalk.com','钉钉内置办公套件','📌'),
    ('office','在线文档','WPS','https://www.wps.cn','金山办公国产套件','📝'),
    ('office','日程管理','滴答清单','https://dida365.com','跨平台GTD日程管理','⏰'),
    ('office','日程管理','番茄ToDo','https://tomatodo.com','番茄工作法计时器','🍅'),
    ('office','写作翻译','DeepL Write','https://www.deepl.com/write','AI英文写作润色','✍️'),
    ('office','写作翻译','写作猫','https://www.xiezuocat.com','AI中文写作助手','🐱'),
    ('office','设计白板','亿图图示','https://www.edrawsoft.cn','国产综合绘图工具','📊'),

    # ===== 网络工具 补充 =====
    ('tools','搜索引擎','秘塔搜索','https://metaso.cn','无广告AI搜索','🔍'),
    ('tools','搜索引擎','Qwant','https://www.qwant.com','法国隐私搜索引擎','🇫🇷'),
    ('tools','搜索引擎','Swisscows','https://swisscows.com','瑞士家庭友好搜索','🇨🇭'),
    ('tools','在线转换','PDF2Go','https://www.pdf2go.com','在线PDF编辑转换','🔄'),
    ('tools','在线转换','Pdf.io','https://pdf.io','免费PDF处理工具','📄'),
    ('tools','在线转换','Ezgif','https://ezgif.com','在线GIF编辑制作','🎞️'),
    ('tools','在线转换','OnlineVideoConverter','https://www.onlinevideoconverter.com','在线视频格式转换','🎬'),
    ('tools','在线转换','Veed.io','https://www.veed.io','在线视频编辑字幕','🎥'),
    ('tools','免费邮箱','腾讯企业邮','https://exmail.qq.com','腾讯免费企业邮箱','🏢'),
    ('tools','免费邮箱','飞书邮箱','https://www.feishu.cn','飞书企业邮箱','🪶'),
    ('tools','免费邮箱','Yandex Mail','https://mail.yandex.com','俄罗斯免费邮箱','🇷🇺'),
    ('tools','VPN代理','ProtonVPN','https://protonvpn.com','瑞士隐私免费VPN','🔐'),
    ('tools','VPN代理','SurfShark','https://surfshark.com','荷兰高性价比VPN','🦈'),
    ('tools','VPN代理','ExpressVPN','https://www.expressvpn.com','老牌高端VPN','🚀'),
    ('tools','VPN代理','NordVPN','https://nordvpn.com','巴拿马安全VPN','🗻'),
    ('tools','VPN代理','快连VPN','https://www.letsvpn.buzz','中国可用高速VPN','⚡'),
    ('tools','云存储','坚果云','https://www.jianguoyun.com','国产同步加密网盘','🥜'),
    ('tools','云存储','天翼云盘','https://cloud.189.cn','中国电信个人云盘','☁️'),
    ('tools','云存储','和彩云','https://caiyun.feixin.10086.cn','中国移动云盘','📱'),
    ('tools','云存储','iCloud','https://www.icloud.com','苹果生态云存储','🍎'),
    ('tools','实用工具','Ping.eu','https://ping.eu','在线网络诊断工具','🔧'),
    ('tools','实用工具','DownForEveryone','https://downforeveryoneorjustme.com','网站宕机检测','📉'),
    ('tools','实用工具','GTmetrix','https://gtmetrix.com','网站性能分析工具','⚡'),
    ('tools','实用工具','PageSpeed Insights','https://pagespeed.web.dev','谷歌网页速度测试','🚀'),
    ('tools','实用工具','SSL Checker','https://www.sslshopper.com','SSL证书检测工具','🔒'),
    ('tools','实用工具','DNS Checker','https://dnschecker.org','全球DNS传播检测','🌍'),
    ('tools','实用工具','Caniuse','https://caniuse.com','浏览器兼容性速查','🌐'),
    ('tools','实用工具','Unicode Table','https://unicode-table.com','Unicode字符大全','🔤'),
    ('tools','实用工具','Emojipedia','https://emojipedia.org','Emoji百科大全','😀'),
    ('tools','实用工具','AlternativeTo','https://alternativeto.net','软件替代品推荐','🔄'),
    ('tools','实用工具','Product Hunt','https://www.producthunt.com','新产品每日发现','🚀'),

    # ===== 购物交易 补充 =====
    ('commerce','全球电商','Wish','https://www.wish.com','全球移动电商平台','🛍️'),
    ('commerce','全球电商','Etsy','https://www.etsy.com','手工艺品创意电商','🎨'),
    ('commerce','中国电商','当当','https://www.dangdang.com','中国网上书店','📚'),
    ('commerce','中国电商','考拉海购','https://www.kaola.com','网易跨境进口电商','🐨'),
    ('commerce','中国电商','得物','https://www.dewu.com','潮流正品鉴定交易','👟'),
    ('commerce','中国电商','识货','https://www.shihuo.cn','运动装备导购平台','🏀'),
    ('commerce','二手交易','爱回收','https://www.aihuishou.com','电子产品回收交易','♻️'),
    ('commerce','数码产品','荣耀商城','https://www.hihonor.com/cn','荣耀官方商城','📱'),
    ('commerce','数码产品','OPPO商城','https://www.opposhop.cn','OPPO官方商城','📱'),
    ('commerce','数码产品','vivo商城','https://shop.vivo.com.cn','vivo官方商城','📱'),
    ('commerce','数码产品','魅族商城','https://www.meizu.com','魅族官方商城','📱'),

    # ===== 生活服务 补充 =====
    ('life','出行旅游','12306','https://www.12306.cn','中国铁路官方购票','🚄'),
    ('life','出行旅游','滴滴出行','https://www.didiglobal.com','中国网约车平台','🚗'),
    ('life','出行旅游','曹操出行','https://www.caocaokeji.cn','吉利旗下网约车','🚘'),
    ('life','出行旅游','哈啰', 'https://www.hellobike.com','共享单车出行','🚲'),
    ('life','地图导航','腾讯地图','https://map.qq.com','腾讯地图导航服务','🗺️'),
    ('life','餐饮外卖','叮咚买菜','https://www.ddxq.mobi','生鲜电商配送','🥬'),
    ('life','餐饮外卖','盒马','https://www.freshhema.com','阿里新零售生鲜','🦛'),
    ('life','餐饮外卖','每日优鲜','https://www.missfresh.cn','生鲜O2O电商','🍎'),
    ('life','金融理财','中国银联','https://www.unionpay.com','银行卡联合组织','💳'),
    ('life','金融理财','蚂蚁财富','https://www.antfortune.com','蚂蚁集团理财平台','🐜'),
    ('life','金融理财','东方财富','https://www.eastmoney.com','中国财经门户','📈'),
    ('life','金融理财','同花顺','https://www.10jqka.com.cn','股票行情与交易','📊'),
    ('life','生活缴费','国家电网','https://www.95598.cn','电力服务缴费平台','⚡'),
    ('life','生活缴费','中国移动','https://www.10086.cn','中国移动网上营业厅','📶'),
    ('life','生活缴费','中国联通','https://www.10010.com','中国联通网上营业厅','📶'),
    ('life','生活缴费','中国电信','https://www.189.cn','中国电信网上营业厅','📶'),

    # ===== 新闻资讯 补充 =====
    ('news','综合资讯','澎湃新闻','https://www.thepaper.cn','上海东方报业新媒体','📰'),
    ('news','综合资讯','界面新闻','https://www.jiemian.com','财经与商业新媒体','📊'),
    ('news','综合资讯','华尔街见闻','https://wallstreetcn.com','全球财经资讯','🏦'),
    ('news','科技资讯','品玩','https://www.pingwest.com','全球科技资讯媒体','🔌'),
    ('news','科技资讯','差评','https://www.chaping.cn','科技吐槽与评测','🤖'),
    ('news','科技资讯','量子位','https://www.qbitai.com','AI与前沿科技报道','🔬'),
    ('news','科技资讯','Wired','https://www.wired.com','美国科技文化杂志','📡'),
    ('news','国际媒体','纽约时报中文','https://cn.nytimes.com','纽约时报中文网','📰'),
    ('news','国际媒体','华尔街日报','https://www.wsj.com','美国商业财经日报','📰'),
    ('news','国际媒体','FT中文网','https://www.ftchinese.com','金融时报中文版','🇬🇧'),

    # ===== 成人内容 补充 =====
    ('adult','视频','MissAV','https://missav.com','日本成人影片在线','🔞'),
    ('adult','社区','91论坛','https://91porn.com','中文成人视频社区','🔞'),
    ('adult','二次元','Hitomi.la','https://hitomi.la','同人志在线阅读','📖'),
    ('adult','信息','Adult Empire','https://www.adultempire.com','成人影片在线商城','🔞'),
    ('adult','社区','Fansly','https://fansly.com','创作者成人内容订阅','🔞'),

    # ===== 新增：政府服务 (gov) =====
    ('gov','中央政府','中国政府网','https://www.gov.cn','中华人民共和国中央人民政府','🇨🇳'),
    ('gov','个税社保','个人所得税','https://www.etax.chinatax.gov.cn','个税申报查询平台','💰'),
    ('gov','个税社保','国家社保平台','https://si.12333.gov.cn','社保查询服务平台','🏥'),
    ('gov','个税社保','住房公积金','https://www.12329.cn','全国公积金查询','🏠'),
    ('gov','交通出行','交管12123','https://122.gov.cn','交通安全综合服务','🚗'),
    ('gov','企业服务','国家企业信用','https://www.gsxt.gov.cn','企业信息公示系统','📋'),
    ('gov','企业服务','商标局','https://sbj.cnipa.gov.cn','国家知识产权商标局','®️'),
    ('gov','教育考试','学信网','https://www.chsi.com.cn','教育部学历查询','🎓'),
    ('gov','教育考试','研招网','https://yz.chsi.com.cn','中国研究生招生信息','📝'),
    ('gov','出入境','移民管理局','https://www.nia.gov.cn','出入境证件办理','🛂'),

    # ===== 新增：健康医疗 (health) =====
    ('health','问诊挂号','好大夫','https://www.haodf.com','在线医疗咨询挂号','👨‍⚕️'),
    ('health','问诊挂号','微医','https://www.guahao.com','互联网医院挂号','🏥'),
    ('health','问诊挂号','丁香园','https://www.dxy.cn','医学专业社区与科普','🌿'),
    ('health','问诊挂号','京东健康','https://www.jdhealth.com','在线购药与问诊','💊'),
    ('health','问诊挂号','阿里健康','https://www.alihealth.cn','阿里医疗健康平台','🏥'),
    ('health','运动健身','Keep','https://www.gotokeep.com','移动健身训练平台','🏃'),
    ('health','运动健身','薄荷健康','https://www.boohee.com','饮食热量管理减肥','🌿'),
    ('health','心理健康','壹心理','https://www.xinli001.com','心理健康服务平台','🧠'),
]

def main():
    conn = mysql.connector.connect(**DB)
    c = conn.cursor()

    # 注册新分类
    for key, name, color in [('gov','政务服务','#3b82f6'),('health','健康医疗','#22c55e')]:
        c.execute('INSERT IGNORE INTO categories (cat_key, cat_name, cat_color) VALUES (%s,%s,%s)',(key,name,color))

    added = 0
    skipped = 0
    for cat, sub, title, url, desc, icon in SITES:
        domain = url.split('/')[2]
        c.execute('SELECT id FROM bookmarks WHERE url LIKE %s', (f'%{domain}%',))
        if c.fetchone():
            skipped += 1
            continue
        c.execute(
            'INSERT INTO bookmarks (title, url, description, icon, category, sub_category) VALUES (%s,%s,%s,%s,%s,%s)',
            (title, url, desc, icon, cat, sub)
        )
        added += 1

    conn.commit()
    c.execute("SELECT category, COUNT(*) FROM bookmarks GROUP BY category ORDER BY category")
    cat_map = {'dev':'开发技术','study':'学习百科','media':'影音娱乐','social':'社交社区','office':'办公效率','tools':'网络工具','ai':'人工智能','commerce':'购物交易','life':'生活服务','news':'新闻资讯','adult':'成人内容','gov':'政务服务','health':'健康医疗'}
    total = 0
    for cat, cnt in c.fetchall():
        name = cat_map.get(cat, cat)
        print(f'  {name}: {cnt}')
        total += cnt
    print(f'  总计: {total}')
    print(f'\n本轮新增: {added}, 跳过重复: {skipped}')
    conn.close()

if __name__ == '__main__':
    main()

import mysql.connector
DB = {'host': 'localhost', 'user': 'root', 'password': '123456', 'database': 'pj1', 'charset': 'utf8mb4', 'buffered': True}

SITES = [
    ('dev','开发工具','Babel','https://babeljs.io','JS编译器','📘'),
    ('dev','开发工具','Webpack','https://webpack.js.org','模块打包','📦'),
    ('dev','开发工具','Rollup','https://rollupjs.org','ESM打包器','🔧'),
    ('dev','开发工具','Astro','https://astro.build','内容优先框架','🚀'),
    ('dev','开发工具','Next.js','https://nextjs.org','React全栈框架','▲'),
    ('dev','开发工具','Nuxt','https://nuxt.com','Vue全栈框架','💚'),
    ('dev','开发工具','Svelte','https://svelte.dev','编译型框架','🧡'),
    ('dev','开发工具','Solid','https://www.solidjs.com','高性能框架','⚡'),
    ('dev','开发工具','NestJS','https://nestjs.com','Node企业框架','🏗️'),
    ('dev','开发工具','FastAPI','https://fastapi.tiangolo.com','Python API框架','🐍'),
    ('dev','开发工具','tRPC','https://trpc.io','类型安全API','🔗'),
    ('dev','开发工具','Zod','https://zod.dev','TS模式验证','✅'),
    ('dev','开发工具','Redux','https://redux.js.org','状态管理','🔄'),
    ('dev','开发工具','TanStack Query','https://tanstack.com/query','异步状态','📡'),
    ('dev','开发工具','Storybook','https://storybook.js.org','UI组件环境','📖'),
    ('dev','开发工具','Sentry','https://sentry.io','错误监控','🔍'),
    ('dev','开发工具','Datadog','https://www.datadoghq.com','云监控平台','🐶'),
    ('dev','开发工具','New Relic','https://newrelic.com','全栈可观测','📊'),
    ('dev','开发工具','Elastic','https://www.elastic.co','搜索分析引擎','🔍'),
    ('dev','开发工具','Redis','https://redis.io','内存数据库','🔴'),
    ('dev','开发工具','PostgreSQL','https://www.postgresql.org','开源数据库','🐘'),
    ('dev','开发工具','MySQL','https://www.mysql.com','关系型数据库','🐬'),
    ('dev','开发工具','SQLite','https://www.sqlite.org','轻量数据库','🪶'),
    ('dev','开发工具','ClickHouse','https://clickhouse.com','分析数据库','⚡'),
    ('dev','开发工具','NGINX','https://nginx.org','Web服务器','🟢'),
    ('dev','开发工具','Caddy','https://caddyserver.com','自动HTTPS','🔒'),
    ('dev','开发工具','Traefik','https://traefik.io','云原生代理','🔀'),
    ('dev','开发工具','Fastify','https://fastify.dev','高性能Node框架','⚡'),
    ('dev','开发工具','Hono','https://hono.dev','边缘Web框架','🔥'),
    ('dev','开发工具','Kafka','https://kafka.apache.org','流处理平台','📡'),
    ('dev','开发工具','RabbitMQ','https://www.rabbitmq.com','消息队列','🐰'),
    ('dev','开发工具','NATS','https://nats.io','云原生消息','📨'),
    ('dev','开发工具','VictoriaMetrics','https://victoriametrics.com','时序数据库','📈'),
    ('dev','开发工具','Prometheus','https://prometheus.io','监控告警系统','🔥'),
    ('dev','开发工具','Grafana','https://grafana.com','可视化仪表盘','📊'),
    ('dev','开发工具','Kibana','https://www.elastic.co/kibana','Elastic可视化','📈'),

    ('study','在线课程','可汗学院','https://zh.khanacademy.org','免费教育','🏫'),
    ('study','在线课程','学堂云','https://www.xuetangx.com','清华MOOC','🏛️'),
    ('study','百科参考','WikiHow','https://zh.wikihow.com','万事指南','📗'),
    ('study','百科参考','全历史','https://www.allhistory.com','历史可视化','📜'),
    ('study','百科参考','古诗文网','https://www.gushiwen.cn','古诗文宝库','📜'),
    ('study','百科参考','抖音百科','https://www.baike.com','字节百科','📖'),
    ('study','学术资源','知网','https://www.cnki.net','学术数据库','📄'),
    ('study','学术资源','万方','https://www.wanfangdata.com.cn','学术库','📊'),
    ('study','学术资源','Semantic Scholar','https://www.semanticscholar.org','AI学术搜索','🤖'),
    ('study','学术资源','PubMed','https://pubmed.ncbi.nlm.nih.gov','生物医学库','🧬'),
    ('study','知识阅读','得到','https://www.igetget.com','知识服务','📚'),

    ('media','视频平台','CCTV','https://tv.cctv.com','央视视频','📺'),
    ('media','音乐平台','咪咕音乐','https://music.migu.cn','中国移动音乐','🎶'),
    ('media','游戏直播','游民星空','https://www.gamersky.com','单机游戏资讯','🌌'),
    ('media','游戏直播','3DM','https://www.3dmgame.com','游戏汉化资讯','🎮'),
    ('media','游戏直播','游侠网','https://www.ali213.net','PC游戏门户','⚔️'),
    ('media','动漫艺术','Bilibili漫画','https://manga.bilibili.com','B站漫画','📖'),
    ('media','动漫艺术','动漫之家','https://www.dmzj.com','中文漫画','📚'),

    ('social','社区论坛','豆瓣小组','https://www.douban.com/group','兴趣小组','👥'),
    ('social','社区论坛','百度知道','https://zhidao.baidu.com','中文问答','❓'),
    ('social','社区论坛','天涯社区','https://www.tianya.cn','老牌论坛','🌍'),
    ('social','内容社区','美篇','https://www.meipian.cn','图文创作','📷'),
    ('social','内容社区','马蜂窝','https://www.mafengwo.cn','旅游攻略','🐝'),

    ('office','商务工具','飞书','https://www.feishu.cn','字节协作','🪶'),
    ('office','商务工具','钉钉','https://www.dingtalk.com','阿里办公','📌'),
    ('office','商务工具','企业微信','https://work.weixin.qq.com','腾讯企业','🏢'),
    ('office','项目管理','Worktile','https://worktile.com','国产协作','🧩'),
    ('office','项目管理','禅道','https://www.zentao.net','开源项目管理','🧘'),
    ('office','设计白板','即时设计','https://js.design','国产UI设计','🎨'),
    ('office','设计白板','摹客','https://www.mockplus.cn','原型设计','🖌️'),
    ('office','设计白板','墨刀','https://modao.cc','产品原型','🔪'),

    ('tools','免费邮箱','新浪邮箱','https://mail.sina.com.cn','新浪邮箱','📧'),
    ('tools','免费邮箱','搜狐邮箱','https://mail.sohu.com','搜狐邮箱','📨'),
    ('tools','实用工具','稿定设计','https://www.gaoding.com','设计模板','🎨'),
    ('tools','实用工具','创客贴','https://www.chuangkit.com','在线设计','🖼️'),
    ('tools','实用工具','幕布','https://mubu.com','大纲笔记','📋'),
    ('tools','实用工具','Xmind','https://xmind.cn','思维导图','🧠'),
    ('tools','实用工具','石墨文档','https://shimo.im','轻量文档','✍️'),
    ('tools','实用工具','腾讯问卷','https://wj.qq.com','在线问卷','📋'),
    ('tools','实用工具','问卷星','https://www.wjx.cn','问卷调查','⭐'),
    ('tools','实用工具','金数据','https://jinshuju.net','表单收集','📊'),

    ('commerce','全球电商','Shopify','https://www.shopify.com','电商建站','🏪'),
    ('commerce','中国电商','什么值得买','https://www.smzdm.com','消费决策','💰'),
    ('commerce','中国电商','慢慢买','https://www.manmanbuy.com','历史价格','📉'),

    ('life','金融理财','中国银行','https://www.boc.cn','中行官网','🏦'),
    ('life','金融理财','建设银行','https://www.ccb.com','建行官网','🏦'),
    ('life','金融理财','工商银行','https://www.icbc.com.cn','工行官网','🏦'),
    ('life','金融理财','农业银行','https://www.abchina.com','农行官网','🏦'),
    ('life','出行旅游','穷游','https://www.qyer.com','出境攻略','🌍'),

    ('news','综合资讯','新华社','https://www.xinhuanet.com','国家通讯社','📰'),
    ('news','综合资讯','人民网','https://www.people.com.cn','人民日报','📰'),
    ('news','综合资讯','央视网','https://www.cctv.com','央视官网','📺'),
    ('news','新闻资讯','环球网','https://www.huanqiu.com','环球时报','🌍'),
    ('news','科技资讯','极客公园','https://www.geekpark.net','科技媒体','🧠'),

    ('adult','视频','JavLibrary','https://www.javlibrary.com','日本影片信息库','🔞'),
    ('adult','图片','Gelbooru','https://gelbooru.com','动漫图库','🖼️'),
    ('adult','图片','Danbooru','https://danbooru.donmai.us','动漫数据库','🖼️'),

    ('gov','政务服务','国家医保局','https://www.nhsa.gov.cn','医保平台','🏥'),
    ('gov','政务服务','公安部','https://www.mps.gov.cn','公安服务','👮'),
    ('gov','政务服务','民政部','https://www.mca.gov.cn','民政服务','🤝'),
    ('gov','政务服务','央行','https://www.pbc.gov.cn','中国人民银行','🏦'),

    ('health','运动健身','咕咚','https://www.codoon.com','运动记录','🏃'),
    ('health','运动健身','悦跑圈','https://www.thejoyrun.com','跑步社交','🏃'),
    ('health','心理健康','简单心理','https://www.jiandanxinli.com','心理咨询','🧠'),
]

conn = mysql.connector.connect(**DB)
c = conn.cursor()
added = 0
for cat, sub, title, url, desc, icon in SITES:
    domain = url.split('/')[2]
    c.execute('SELECT id FROM bookmarks WHERE url LIKE %s', (f'%{domain}%',))
    if c.fetchone(): continue
    c.execute('INSERT INTO bookmarks (title, url, description, icon, category, sub_category) VALUES (%s,%s,%s,%s,%s,%s)',(title, url, desc, icon, cat, sub))
    added += 1

conn.commit()
c.execute("SELECT category, COUNT(*) FROM bookmarks GROUP BY category ORDER BY count(*) DESC")
names = {'dev':'开发技术','study':'学习百科','media':'影音娱乐','social':'社交社区','office':'办公效率','tools':'网络工具','ai':'人工智能','commerce':'购物交易','life':'生活服务','news':'新闻资讯','adult':'成人内容','gov':'政务服务','health':'健康医疗'}
total = 0
for cat, cnt in c.fetchall():
    print(f'  {names.get(cat,cat)}: {cnt}')
    total += cnt
print(f'  总计: {total} | 新增: {added}')
conn.close()

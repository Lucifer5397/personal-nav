"""
扩充书签到 1000+，重点：AI大模型官网、开放平台、各大公司官网
按域名去重，纯中文描述
"""
import mysql.connector

DB = {'host': 'localhost', 'user': 'root', 'password': '123456', 'database': 'pj1', 'charset': 'utf8mb4', 'buffered': True}

# ===== 先补充新分类 =====
NEW_CATS = [
    ('ai', '人工智能', '#10b981'),
    ('adult', '成人内容', '#ef4444'),
]

# ===== 新网站数据 (分类, 子分类, 标题, 网址, 描述, 图标) =====
NEW_SITES = [
    # ==================== 人工智能 (ai) ====================
    # -- 大模型对话 --
    ('ai', '大模型对话', 'ChatGPT', 'https://chat.openai.com', 'OpenAI 旗舰对话AI', '🤖'),
    ('ai', '大模型对话', 'Claude', 'https://claude.ai', 'Anthropic 对话AI助手', '🧠'),
    ('ai', '大模型对话', 'Gemini', 'https://gemini.google.com', '谷歌多模态大模型', '💎'),
    ('ai', '大模型对话', 'DeepSeek', 'https://chat.deepseek.com', '中国深度求索大模型', '🔍'),
    ('ai', '大模型对话', '文心一言', 'https://yiyan.baidu.com', '百度知识增强大模型', '📝'),
    ('ai', '大模型对话', '通义千问', 'https://tongyi.aliyun.com', '阿里通义系列大模型', '☁️'),
    ('ai', '大模型对话', 'Kimi', 'https://kimi.moonshot.cn', '月之暗面长文本对话', '🌙'),
    ('ai', '大模型对话', '豆包', 'https://www.doubao.com', '字节跳动AI对话助手', '🫘'),
    ('ai', '大模型对话', '智谱清言', 'https://chatglm.cn', '智谱AI ChatGLM对话', '💬'),
    ('ai', '大模型对话', '百川智能', 'https://www.baichuan-ai.com', '百川大模型对话平台', '🌊'),
    ('ai', '大模型对话', 'Poe', 'https://poe.com', '一站式多模型聚合对话', '🔮'),
    ('ai', '大模型对话', 'Perplexity', 'https://www.perplexity.ai', 'AI搜索引擎对话助手', '🔎'),
    ('ai', '大模型对话', 'Grok', 'https://grok.x.ai', 'xAI 马斯克大模型', '🚀'),
    ('ai', '大模型对话', 'Copilot', 'https://copilot.microsoft.com', '微软 AI 编程助手', '🪟'),
    ('ai', '大模型对话', 'Mistral', 'https://chat.mistral.ai', '法国领先大模型平台', '🇫🇷'),
    # -- AI开放平台 --
    ('ai', '开放平台', 'OpenAI Platform', 'https://platform.openai.com', 'GPT API 开发者平台', '🔌'),
    ('ai', '开放平台', 'Anthropic Console', 'https://console.anthropic.com', 'Claude API 管理控制台', '🖥️'),
    ('ai', '开放平台', 'Google AI Studio', 'https://aistudio.google.com', '谷歌Gemini免费开发环境', '🧪'),
    ('ai', '开放平台', 'DeepSeek Platform', 'https://platform.deepseek.com', 'DeepSeek API 开发平台', '🔧'),
    ('ai', '开放平台', 'Groq', 'https://groq.com', '超快推理 LPU 引擎', '⚡'),
    ('ai', '开放平台', 'Together AI', 'https://www.together.ai', '开源模型云端推理平台', '🤝'),
    ('ai', '开放平台', 'Replicate', 'https://replicate.com', 'AI 模型云端运行平台', '🔄'),
    ('ai', '开放平台', 'Hugging Face', 'https://huggingface.co', '全球最大AI模型社区', '🤗'),
    ('ai', '开放平台', 'Civitai', 'https://civitai.com', 'Stable Diffusion模型分享', '🎨'),
    ('ai', '开放平台', 'ModelScope', 'https://www.modelscope.cn', '阿里AI模型开源社区', '🧩'),
    # -- AI编程 --
    ('ai', 'AI编程', 'GitHub Copilot', 'https://github.com/features/copilot', 'GitHub AI编程助手', '👨‍💻'),
    ('ai', 'AI编程', 'Cursor', 'https://cursor.sh', 'AI原生代码编辑器', '🖱️'),
    ('ai', 'AI编程', 'Windsurf', 'https://codeium.com/windsurf', 'Codeium AI IDE编辑器', '🌊'),
    ('ai', 'AI编程', 'v0 by Vercel', 'https://v0.dev', 'AI前端UI生成工具', '🖼️'),
    ('ai', 'AI编程', 'Bolt.new', 'https://bolt.new', 'AI全栈应用在线生成', '⚡'),
    ('ai', 'AI编程', 'Lovable', 'https://lovable.dev', 'AI快速构建Web应用', '❤️'),
    ('ai', 'AI编程', 'Codeium', 'https://codeium.com', '免费AI代码补全插件', '🧩'),
    ('ai', 'AI编程', 'Tabnine', 'https://www.tabnine.com', 'AI代码补全引擎', '9️⃣'),
    # -- AI图像 --
    ('ai', 'AI图像', 'Midjourney', 'https://www.midjourney.com', '顶级AI艺术图像生成', '🎨'),
    ('ai', 'AI图像', 'DALL-E', 'https://openai.com/dall-e', 'OpenAI 文本生成图像', '🖼️'),
    ('ai', 'AI图像', 'Stable Diffusion', 'https://stability.ai', '开源AI图像生成模型', '🖌️'),
    ('ai', 'AI图像', 'Leonardo.ai', 'https://leonardo.ai', 'AI游戏资产与图像生成', '🎮'),
    ('ai', 'AI图像', 'Runway', 'https://runwayml.com', 'AI视频生成与编辑', '🎬'),
    ('ai', 'AI图像', 'Krea.ai', 'https://www.krea.ai', 'AI实时图像生成画布', '🖼️'),
    # -- AI视频 --
    ('ai', 'AI视频', 'Sora', 'https://sora.com', 'OpenAI 文本生成视频', '🎥'),
    ('ai', 'AI视频', 'Pika', 'https://pika.art', 'AI视频生成与编辑工具', '🎬'),
    ('ai', 'AI视频', 'HeyGen', 'https://www.heygen.com', 'AI数字人视频生成', '👤'),
    ('ai', 'AI视频', 'Synthesia', 'https://www.synthesia.io', 'AI虚拟主播视频平台', '🎙️'),
    # -- AI音频 --
    ('ai', 'AI音频', 'Suno', 'https://suno.com', 'AI音乐创作生成平台', '🎵'),
    ('ai', 'AI音频', 'Udio', 'https://www.udio.com', 'AI高质量音乐生成', '🎶'),
    ('ai', 'AI音频', 'ElevenLabs', 'https://elevenlabs.io', 'AI语音合成与克隆', '🗣️'),
    ('ai', 'AI音频', 'NotebookLM', 'https://notebooklm.google.com', '谷歌AI笔记与播客生成', '📓'),

    # ==================== 开发技术 (dev) 扩充 ====================
    ('dev', '代码托管', 'SourceForge', 'https://sourceforge.net', '老牌开源项目托管平台', '📦'),
    ('dev', '代码托管', 'Codeberg', 'https://codeberg.org', '欧洲非营利开源托管', '🏔️'),
    ('dev', '代码托管', 'Launchpad', 'https://launchpad.net', 'Ubuntu开源项目托管', '🚀'),
    ('dev', '技术社区', '稀土掘金', 'https://juejin.cn', '中文开发者技术社区', '💎'),
    ('dev', '技术社区', '思否', 'https://segmentfault.com', '中文技术问答社区', '🔧'),
    ('dev', '技术社区', 'InfoQ', 'https://www.infoq.cn', '技术资讯与大会报道', '📰'),
    ('dev', '技术社区', '开源中国', 'https://www.oschina.net', '中文开源技术社区', '🏮'),
    ('dev', '技术社区', 'Ruby China', 'https://ruby-china.org', '中文Ruby开发者社区', '💎'),
    ('dev', '云平台', 'Linode', 'https://www.linode.com', '老牌Linux云服务器', '🐧'),
    ('dev', '云平台', 'Vultr', 'https://www.vultr.com', '全球多地云服务器', '🌍'),
    ('dev', '云平台', 'OVHcloud', 'https://www.ovhcloud.com', '欧洲最大云服务商', '🇪🇺'),
    ('dev', '云平台', 'Hetzner', 'https://www.hetzner.com', '德国高性价比云服务器', '🇩🇪'),
    ('dev', '云平台', 'Alibaba Cloud', 'https://www.alibabacloud.com', '阿里云国际版', '☁️'),
    ('dev', '云平台', 'Oracle Cloud', 'https://www.oracle.com/cloud', '甲骨文免费云服务', '🆓'),
    ('dev', '云平台', 'Cloudflare Pages', 'https://pages.cloudflare.com', '边缘网络静态部署', '🛡️'),
    ('dev', '开发工具', 'Swagger', 'https://swagger.io', 'API文档设计与生成', '📋'),
    ('dev', '开发工具', 'GraphQL', 'https://graphql.org', 'API查询语言官网', '◈'),
    ('dev', '开发工具', 'gRPC', 'https://grpc.io', '谷歌高性能RPC框架', '🔗'),
    ('dev', '开发工具', 'ESLint', 'https://eslint.org', 'JavaScript代码检查', '✅'),
    ('dev', '开发工具', 'Prettier', 'https://prettier.io', '代码格式化工具官网', '✨'),
    ('dev', '开发工具', 'Biome', 'https://biomejs.dev', 'Rust实现JS/TS工具链', '🦀'),
    ('dev', '开发工具', 'Rust', 'https://www.rust-lang.org', 'Rust编程语言官网', '🦀'),
    ('dev', '开发工具', 'Go', 'https://go.dev', 'Go编程语言官网', '🔵'),
    ('dev', '开发工具', 'Python', 'https://www.python.org', 'Python编程语言官网', '🐍'),
    ('dev', '开发工具', 'Node.js', 'https://nodejs.org', 'Node.js运行时官网', '💚'),
    ('dev', '开发工具', 'Deno', 'https://deno.com', '现代JS/TS安全运行时', '🦕'),
    ('dev', '开发工具', 'Bun', 'https://bun.sh', '极速JS运行时与打包器', '🥟'),
    ('dev', '开发工具', 'pnpm', 'https://pnpm.io', '快速磁盘高效包管理器', '📦'),
    ('dev', '开发工具', 'Laravel', 'https://laravel.com', 'PHP开发框架官网', '🔺'),
    ('dev', '开发工具', 'Django', 'https://www.djangoproject.com', 'Python Web框架官网', '🎸'),
    ('dev', '开发工具', 'Tailwind CSS', 'https://tailwindcss.com', '原子化CSS框架官网', '🎨'),
    ('dev', '在线IDE', 'GitHub Codespaces', 'https://github.com/features/codespaces', '云端开发环境秒启', '☁️'),
    ('dev', '在线IDE', 'Gitpod', 'https://www.gitpod.io', '云端开发环境自动化', '🖥️'),
    ('dev', '在线IDE', 'StackBlitz', 'https://stackblitz.com', 'Web开发在线IDE', '⚡'),

    # ==================== 学习百科 (study) 扩充 ====================
    ('study', '在线课程', '极客时间', 'https://time.geekbang.org', 'IT领域实战技能课程', '⏰'),
    ('study', '在线课程', '慕课网', 'https://www.imooc.com', 'IT技能在线学习平台', '🎓'),
    ('study', '在线课程', '实验楼', 'https://www.lanqiao.cn', '在线Linux与编程实验', '🧪'),
    ('study', '在线课程', 'DataCamp', 'https://www.datacamp.com', '数据科学在线学习', '📊'),
    ('study', '在线课程', 'Kaggle', 'https://www.kaggle.com', '数据科学竞赛与学习', '🏆'),
    ('study', '百科参考', '维基百科', 'https://zh.wikipedia.org', '自由的在线百科全书', '📖'),
    ('study', '百科参考', '萌娘百科', 'https://zh.moegirl.org.cn', 'ACG文化百科全书', '🌸'),
    ('study', '百科参考', 'Stack Exchange', 'https://stackexchange.com', '问答社区网络全家桶', '🔗'),
    ('study', '知识阅读', '得到', 'https://www.dedao.cn', '知识服务与听书平台', '📚'),
    ('study', '知识阅读', '微信读书', 'https://weread.qq.com', '腾讯正版电子书阅读', '📱'),
    ('study', '知识阅读', '掌阅', 'https://www.zhangyue.com', '数字阅读与出版平台', '📖'),
    ('study', '语言学习', '多邻国', 'https://www.duolingo.cn', '游戏化免费语言学习', '🦉'),

    # ==================== 影音娱乐 (media) 扩充 ====================
    ('media', '视频平台', '腾讯视频', 'https://v.qq.com', '腾讯综合视频平台', '🎬'),
    ('media', '视频平台', '优酷', 'https://www.youku.com', '阿里旗下视频平台', '▶️'),
    ('media', '视频平台', '芒果TV', 'https://www.mgtv.com', '湖南卫视综艺独播', '🥭'),
    ('media', '视频平台', '韩剧TV', 'https://www.hanjutv.com', '韩剧在线播放平台', '🇰🇷'),
    ('media', '音乐平台', 'Spotify', 'https://open.spotify.com', '全球最大音乐流媒体', '🎵'),
    ('media', '游戏直播', '虎牙直播', 'https://www.huya.com', '中国领先游戏直播', '🐯'),
    ('media', '动漫艺术', '樱花动漫', 'https://www.yhdmp.com', '动漫在线观看平台', '🍥'),
    ('media', '文学阅读', '纵横中文网', 'https://www.zongheng.com', '百度旗下原创文学', '📖'),
    ('media', '文学阅读', '17K小说网', 'https://www.17k.com', '中文在线原创文学', '📚'),
    ('media', '文学阅读', '掌阅文学', 'https://www.ireader.com.cn', '移动阅读与创作平台', '📱'),

    # ==================== 社交社区 (social) 扩充 ====================
    ('social', '全球社交', 'Telegram', 'https://telegram.org', '加密即时通讯与频道', '✈️'),
    ('social', '社区论坛', 'NGA玩家社区', 'https://bbs.nga.cn', '暴雪游戏与ACG论坛', '🎮'),
    ('social', '社区论坛', 'Stage1st', 'https://bbs.saraba1st.com', '动漫游戏宅向论坛', '🍀'),
    ('social', '社区论坛', 'chiphell', 'https://www.chiphell.com', '数码硬件玩家论坛', '💻'),
    ('social', '社区论坛', 'V2EX', 'https://www.v2ex.com', '创意工作者社区', '💡'),
    ('social', '社区论坛', 'Hostloc', 'https://hostloc.com', '全球主机交流论坛', '🌐'),
    ('social', '内容社区', '什么值得买', 'https://www.smzdm.com', '消费决策内容社区', '💰'),
    ('social', '即时通讯', '飞书', 'https://www.feishu.cn', '字节跳动企业协作', '🪶'),
    ('social', '即时通讯', '钉钉', 'https://www.dingtalk.com', '阿里企业通讯办公', '📌'),
    ('social', '即时通讯', '企业微信', 'https://work.weixin.qq.com', '腾讯企业通讯平台', '🏢'),

    # ==================== 办公效率 (office) 扩充 ====================
    ('office', '文档笔记', '飞书文档', 'https://www.feishu.cn/product/docs', '下一代协作文档', '🪶'),
    ('office', '文档笔记', 'Logseq', 'https://logseq.com', '开源双向链接笔记', '🧩'),
    ('office', '文档笔记', 'Craft', 'https://www.craft.do', '颜值最高的文档工具', '✨'),
    ('office', '设计白板', 'Sketch', 'https://www.sketch.com', 'Mac原生UI设计工具', '🎨'),
    ('office', '设计白板', 'Pixso', 'https://pixso.cn', '国产协作UI设计工具', '🖌️'),
    ('office', '设计白板', 'MasterGo', 'https://mastergo.com', '中文协同设计平台', '🎨'),
    ('office', '设计白板', 'ProcessOn', 'https://www.processon.com', '在线流程图与思维导图', '📊'),
    ('office', '商务工具', 'Notion Calendar', 'https://calendar.notion.so', 'Notion 日程管理', '📅'),
    ('office', '商务工具', 'Bubble', 'https://bubble.io', '无代码Web应用构建', '🫧'),
    ('office', '商务工具', 'Webflow', 'https://webflow.com', '可视化网站设计开发', '🌊'),
    ('office', '商务工具', 'Framer', 'https://www.framer.com', '交互原型与网站设计', '🖼️'),

    # ==================== 网络工具 (tools) 扩充 ====================
    ('tools', '搜索引擎', '搜狗搜索', 'https://www.sogou.com', '腾讯旗下搜索引擎', '🐕'),
    ('tools', '搜索引擎', '360搜索', 'https://www.so.com', '360安全搜索引擎', '🔍'),
    ('tools', '搜索引擎', 'Ecosia', 'https://www.ecosia.org', '种树环保搜索引擎', '🌳'),
    ('tools', '搜索引擎', 'Startpage', 'https://www.startpage.com', '匿名谷歌搜索结果', '🕵️'),
    ('tools', '搜索引擎', 'Brave Search', 'https://search.brave.com', 'Brave独立搜索引擎', '🦁'),
    ('tools', '搜索引擎', 'Kagi', 'https://kagi.com', '付费高质量搜索引擎', '🔑'),
    ('tools', '在线转换', 'OnlineOCR', 'https://www.onlineocr.net', '图片PDF文字识别转换', '📄'),
    ('tools', '在线转换', 'PDF Candy', 'https://pdfcandy.com', '免费PDF在线工具箱', '🍬'),
    ('tools', '在线转换', 'DocHub', 'https://dochub.com', '在线PDF编辑与签名', '📝'),
    ('tools', '在线转换', 'PDFescape', 'https://www.pdfescape.com', '免费在线PDF编辑器', '📑'),
    ('tools', '免费邮箱', '126邮箱', 'https://www.126.com', '网易免费电子邮箱', '📮'),
    ('tools', '免费邮箱', '189邮箱', 'https://mail.189.cn', '中国电信免费邮箱', '📧'),
    ('tools', '免费邮箱', '阿里云邮箱', 'https://mail.aliyun.com', '阿里企业免费邮箱', '☁️'),
    ('tools', '免费邮箱', 'Mail.ru', 'https://mail.ru', '俄罗斯最大邮箱服务', '🇷🇺'),
    ('tools', '云存储', '百度网盘', 'https://pan.baidu.com', '中国最大个人网盘', '💾'),
    ('tools', '云存储', '阿里云盘', 'https://www.aliyundrive.com', '阿里不限速云盘', '☁️'),
    ('tools', '云存储', '夸克网盘', 'https://pan.quark.cn', '夸克浏览器云存储', '📁'),
    ('tools', '云存储', '蓝奏云', 'https://www.lanzou.com', '小文件快速分享网盘', '🔵'),
    ('tools', '云存储', '123云盘', 'https://www.123pan.com', '免费大容量云存储', '💿'),
    ('tools', '实用工具', 'IPIP.net', 'https://www.ipip.net', 'IP地址查询与定位', '📍'),
    ('tools', '实用工具', '站长工具', 'https://tool.chinaz.com', '中文网站站长工具箱', '🛠️'),
    ('tools', '实用工具', '爱站网', 'https://www.aizhan.com', 'SEO综合查询工具', '📈'),
    ('tools', '实用工具', 'SimilarWeb', 'https://www.similarweb.com', '网站流量排名分析', '📊'),
    ('tools', '实用工具', 'BuiltWith', 'https://builtwith.com', '网站技术栈探测工具', '🔍'),
    ('tools', '实用工具', 'Wayback Machine', 'https://web.archive.org', '互联网历史时光机', '⏳'),
    ('tools', '实用工具', 'ExplainShell', 'https://explainshell.com', 'Shell命令可视化解释', '🐚'),
    ('tools', '实用工具', 'Crontab Guru', 'https://crontab.guru', 'Cron表达式在线编辑', '⏱️'),
    ('tools', '实用工具', 'RegExr', 'https://regexr.com', '正则表达式学习测试', '📐'),
    ('tools', '实用工具', 'Carbon', 'https://carbon.now.sh', '代码截图美化分享', '🖼️'),
    ('tools', '实用工具', 'Ray.so', 'https://ray.so', 'Raycast代码截图工具', '📸'),

    # ==================== 新增：购物交易 (commerce) ====================
    ('commerce', '全球电商', 'Amazon', 'https://www.amazon.com', '全球最大电商平台', '🛒'),
    ('commerce', '全球电商', 'eBay', 'https://www.ebay.com', '全球C2C拍卖电商', '🏷️'),
    ('commerce', '全球电商', 'AliExpress', 'https://www.aliexpress.com', '阿里全球速卖通', '🌍'),
    ('commerce', '全球电商', 'Shopee', 'https://shopee.com', '东南亚最大电商平台', '🛍️'),
    ('commerce', '全球电商', 'Lazada', 'https://www.lazada.com', '阿里东南亚电商', '🛒'),
    ('commerce', '中国电商', '淘宝', 'https://www.taobao.com', '中国最大C2C电商', '🛒'),
    ('commerce', '中国电商', '天猫', 'https://www.tmall.com', '阿里B2C品牌商城', '🐱'),
    ('commerce', '中国电商', '京东', 'https://www.jd.com', '自营正品电商平台', '🐶'),
    ('commerce', '中国电商', '拼多多', 'https://www.pinduoduo.com', '社交团购电商平台', '🧩'),
    ('commerce', '中国电商', '苏宁易购', 'https://www.suning.com', '家电3C零售电商', '🏪'),
    ('commerce', '中国电商', '唯品会', 'https://www.vip.com', '品牌特卖折扣电商', '🎁'),
    ('commerce', '二手交易', '闲鱼', 'https://www.goofish.com', '阿里闲置二手交易', '🐟'),
    ('commerce', '二手交易', '转转', 'https://www.zhuanzhuan.com', '58同城二手交易', '🔄'),
    ('commerce', '数码产品', 'Apple Store', 'https://www.apple.com/store', '苹果官方在线商城', '🍎'),
    ('commerce', '数码产品', '华为商城', 'https://www.vmall.com', '华为官方电商平台', '📱'),
    ('commerce', '数码产品', '小米商城', 'https://www.mi.com', '小米官方直营商城', '📱'),

    # ==================== 新增：生活服务 (life) ====================
    ('life', '出行旅游', '携程', 'https://www.ctrip.com', '中国最大在线旅游平台', '✈️'),
    ('life', '出行旅游', '飞猪', 'https://www.fliggy.com', '阿里旗下旅行平台', '🐷'),
    ('life', '出行旅游', '去哪儿', 'https://www.qunar.com', '旅游搜索引擎平台', '🎒'),
    ('life', '出行旅游', '同程旅行', 'https://www.ly.com', '在线旅游预订服务', '🏨'),
    ('life', '出行旅游', 'Booking', 'https://www.booking.com', '全球酒店预订平台', '🏨'),
    ('life', '出行旅游', 'Airbnb', 'https://www.airbnb.com', '全球民宿短租平台', '🏠'),
    ('life', '地图导航', '高德地图', 'https://www.amap.com', '阿里数字地图导航', '🗺️'),
    ('life', '地图导航', '百度地图', 'https://map.baidu.com', '百度智能地图服务', '📍'),
    ('life', '地图导航', 'Google Maps', 'https://maps.google.com', '谷歌全球地图导航', '🌍'),
    ('life', '餐饮外卖', '美团', 'https://www.meituan.com', '吃喝玩乐本地生活', '🍔'),
    ('life', '餐饮外卖', '饿了么', 'https://www.ele.me', '阿里在线外卖平台', '🛵'),
    ('life', '餐饮外卖', '大众点评', 'https://www.dianping.com', '本地消费评价指南', '⭐'),
    ('life', '餐饮外卖', '肯德基', 'https://www.kfc.com.cn', '肯德基中国官网', '🍗'),
    ('life', '求职招聘', 'BOSS直聘', 'https://www.zhipin.com', '直聊式求职招聘', '💼'),
    ('life', '求职招聘', '前程无忧', 'https://www.51job.com', '老牌综合招聘平台', '📋'),
    ('life', '求职招聘', '智联招聘', 'https://www.zhaopin.com', '中国综合招聘网站', '🔍'),
    ('life', '求职招聘', '猎聘', 'https://www.liepin.com', '中高端人才招聘', '🎯'),
    ('life', '求职招聘', '拉勾', 'https://www.lagou.com', '互联网行业招聘', '💻'),
    ('life', '金融理财', '支付宝', 'https://www.alipay.com', '中国最大移动支付', '💳'),
    ('life', '金融理财', '微信支付', 'https://pay.weixin.qq.com', '腾讯移动支付平台', '💚'),
    ('life', '金融理财', '招商银行', 'https://www.cmbchina.com', '零售银行标杆', '🏦'),
    ('life', '金融理财', '天天基金', 'https://fund.eastmoney.com', '东方财富基金平台', '📈'),
    ('life', '金融理财', '雪球', 'https://xueqiu.com', '投资者交流社区', '❄️'),

    # ==================== 新增：新闻资讯 (news) ====================
    ('news', '综合资讯', '新浪新闻', 'https://news.sina.com.cn', '新浪综合新闻门户', '📰'),
    ('news', '综合资讯', '腾讯新闻', 'https://news.qq.com', '腾讯综合新闻平台', '📱'),
    ('news', '综合资讯', '网易新闻', 'https://news.163.com', '有态度新闻门户', '📰'),
    ('news', '综合资讯', '搜狐新闻', 'https://news.sohu.com', '搜狐综合新闻频道', '📰'),
    ('news', '综合资讯', '今日头条', 'https://www.toutiao.com', '字节跳动推荐引擎', '📋'),
    ('news', '科技资讯', '36氪', 'https://36kr.com', '新商业科技媒体', '🔷'),
    ('news', '科技资讯', '虎嗅', 'https://www.huxiu.com', '科技商业深度观察', '🐯'),
    ('news', '科技资讯', 'IT之家', 'https://www.ithome.com', 'IT科技前沿资讯', '💻'),
    ('news', '科技资讯', '少数派', 'https://sspai.com', '数字生活效率指南', '🧰'),
    ('news', '科技资讯', '机器之心', 'https://www.jiqizhixin.com', '人工智能专业媒体', '🤖'),
    ('news', '国际媒体', 'BBC中文', 'https://www.bbc.com/zhongwen', 'BBC中文新闻', '🇬🇧'),
    ('news', '国际媒体', 'Reuters', 'https://www.reuters.com', '路透社全球新闻', '📡'),
    ('news', '国际媒体', 'CNN', 'https://www.cnn.com', '美国有线电视新闻网', '📺'),
    ('news', '国际媒体', 'The Verge', 'https://www.theverge.com', '科技与生活方式媒体', '🔌'),
    ('news', '国际媒体', 'TechCrunch', 'https://techcrunch.com', '科技创业与投资报道', '🚀'),

    # ==================== 成人内容 (adult) ====================
    ('adult', '视频', 'Pornhub', 'https://www.pornhub.com', '全球最大成人视频网站', '🔞'),
    ('adult', '视频', 'XVideos', 'https://www.xvideos.com', '成人视频分享平台', '🔞'),
    ('adult', '视频', 'Xnxx', 'https://www.xnxx.com', '成人视频社区', '🔞'),
    ('adult', '视频', 'XHamster', 'https://xhamster.com', '成人视频与社区', '🔞'),
    ('adult', '视频', 'RedTube', 'https://www.redtube.com', '成人视频流媒体', '🔞'),
    ('adult', '视频', 'YouPorn', 'https://www.youporn.com', '成人视频分享', '🔞'),
    ('adult', '视频', 'SpankBang', 'https://spankbang.com', '免费成人视频平台', '🔞'),
    ('adult', '图片', 'JavBus', 'https://www.javbus.com', '日本成人影片数据库', '🔞'),
    ('adult', '图片', 'JavDB', 'https://javdb.com', '成人影片评分社区', '🔞'),
    ('adult', '直播', 'Stripchat', 'https://stripchat.com', '成人直播平台', '🔞'),
    ('adult', '直播', 'Chaturbate', 'https://chaturbate.com', '全球成人直播社区', '🔞'),
    ('adult', '直播', 'LiveJasmin', 'https://www.livejasmin.com', '高端成人直播平台', '🔞'),
    ('adult', '二次元', 'Pixiv', 'https://www.pixiv.net', '日本插画创作社区', '🎨'),
    ('adult', '二次元', 'E-Hentai', 'https://e-hentai.org', '同人志画廊数据库', '📚'),
    ('adult', '二次元', 'Nhentai', 'https://nhentai.net', '同人志在线阅读', '📖'),
    ('adult', '社区', 'Sis001', 'https://www.sis001.com', '中文成人综合社区', '🔞'),
    ('adult', '社区', '1024社区', 'https://cl.1024ter.xyz', '中文技术成人论坛', '🔞'),
    ('adult', '社区', 'SexInSex', 'https://www.sexinsex.net', '中文成人信息社区', '🔞'),
]

def main():
    conn = mysql.connector.connect(**DB)
    c = conn.cursor()

    # 先注册新分类
    for cat_key, cat_name, cat_color in NEW_CATS:
        c.execute('INSERT IGNORE INTO categories (cat_key, cat_name, cat_color) VALUES (%s,%s,%s)',
                  (cat_key, cat_name, cat_color))

    # 插入新网站，跳过已存在的URL
    added = 0
    skipped = 0
    for cat, sub, title, url, desc, icon in NEW_SITES:
        c.execute('SELECT id FROM bookmarks WHERE url LIKE %s', (f'%{url.split("/")[2]}%',))
        if c.fetchone():
            skipped += 1
            continue
        c.execute(
            'INSERT INTO bookmarks (title, url, description, icon, category, sub_category) VALUES (%s,%s,%s,%s,%s,%s)',
            (title, url, desc, icon, cat, sub)
        )
        added += 1

    conn.commit()

    # 统计
    c.execute("SELECT category, COUNT(*) FROM bookmarks GROUP BY category ORDER BY category")
    cat_map = {'dev':'开发技术','study':'学习百科','media':'影音娱乐','social':'社交社区','office':'办公效率','tools':'网络工具','ai':'人工智能','commerce':'购物交易','life':'生活服务','news':'新闻资讯','adult':'成人内容'}
    total = 0
    print('=== 当前统计 ===')
    for cat, cnt in c.fetchall():
        name = cat_map.get(cat, cat)
        print(f'  {name}: {cnt}')
        total += cnt
    print(f'  总计: {total}')
    print(f'\n本次新增: {added}, 跳过重复: {skipped}')

    conn.close()

if __name__ == '__main__':
    main()

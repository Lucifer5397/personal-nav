# 个人导航中心 v2.0

一个基于 Flask + MySQL 的个人书签导航网站，含 943 个精选网站、14 大分类、拼音模糊搜索、收藏功能、罗马模拟时钟。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.12 + Flask |
| 数据库 | MySQL 8.0 (pj1库) |
| 前端 | 原生 HTML/CSS/JS（零框架依赖） |
| 图标 | Canvas 绘制罗马数字模拟时钟 |

## 项目结构

```
web-app/
├── app.py                 # Flask 后端 API
├── index.html             # 主页面 (123行)
├── style.css              # 样式表 (328行)
├── script.js              # 逻辑脚本 (760+行)
├── favicon.ico             # 桌面图标
├── startup.bat             # 开机自启脚本
├── open_nav.bat            # 一键打开导航
├── recategorize.py         # 分类重组工具
├── expand_bookmarks.py     # 网站扩充脚本
├── expand_bookmarks[2-4].py
├── restructure.py          # 分类重构工具
├── check_urls.py           # URL 可访问性检测
├── topup.py                # 分类补足工具
├── make_shortcut.py        # 桌面快捷方式生成
└── README.md
```

## 数据库表结构

### bookmarks 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT AUTO_INCREMENT | 主键 |
| title | VARCHAR(100) | 网站标题 |
| url | VARCHAR(500) | 网站地址 |
| description | VARCHAR(500) | 中文简介 |
| icon | VARCHAR(10) | Emoji 图标 |
| category | VARCHAR(50) | 大类代码 |
| sub_category | VARCHAR(30) | 子分类名 |
| is_favorited | TINYINT(1) | 是否收藏 |
| sort_order | INT | 排序权重 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### categories 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| cat_key | VARCHAR(50) | 分类代码 |
| cat_name | VARCHAR(50) | 分类中文名 |
| cat_color | VARCHAR(20) | 分类颜色 |
| created_at | TIMESTAMP | 创建时间 |

## 分类体系（14大类）

| 分类 | 代码 | 数量 | 子分类 |
|------|------|------|--------|
| 网络工具 | tools | 171 | 搜索引擎、在线转换、免费邮箱、虚拟电话、VPN代理、云存储、临时邮箱、实用工具 |
| 开发技术 | dev | 136 | 代码托管、技术社区、在线IDE、开发工具、技术文档、云平台 |
| 学习百科 | study | 78 | 在线课程、百科参考、学术资源、知识阅读、语言学习 |
| 影音娱乐 | media | 64 | 视频平台、音乐平台、动漫艺术、文学阅读、电影评分、短视频 |
| 办公效率 | office | 62 | 项目管理、文档笔记、通讯协作、在线文档、设计白板、流程自动化、商务工具 |
| 社交社区 | social | 61 | 全球社交、即时通讯、社区论坛、内容社区、创作者平台 |
| 人工智能 | ai | 59 | 大模型对话、开放平台、AI编程、AI图像、AI视频、AI音频 |
| 便民服务 | service | 57 | 快递物流、天气服务、企业查询、法律咨询、教育考试、政务服务 |
| 设计资源 | design | 53 | 图标资源、字体资源、图片素材、配色工具、设计灵感、在线工具 |
| 游戏电竞 | game | 40 | 数字平台、电竞社区、游戏资讯、游戏公司、游戏Mod |
| 新闻资讯 | news | 40 | 综合资讯、科技资讯、国际媒体 |
| 生活服务 | life | 39 | 出行旅游、地图导航、餐饮外卖、求职招聘、金融理财、房产家居 |
| 购物交易 | commerce | 35 | 全球电商、中国电商、二手交易、数码产品 |
| 成人内容 | adult | 50 | 网站、社区、图片、漫画 |

## API 接口

### 书签

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/bookmarks` | 列表 `?category=tools` `?favorite=1` |
| GET | `/api/bookmarks/<id>` | 单个 |
| POST | `/api/bookmarks` | 新增 `{title,url,description,icon,category}` |
| PUT | `/api/bookmarks/<id>` | 编辑 |
| DELETE | `/api/bookmarks/<id>` | 删除 |
| PUT | `/api/bookmarks/<id>/favorite` | 切换收藏 |

### 分类

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/categories` | 列表 |
| POST | `/api/categories` | 新增 `{cat_key,cat_name,cat_color}` |
| PUT | `/api/categories/<key>` | 编辑 |
| DELETE | `/api/categories/<key>` | 删除（书签移至tools） |

## 前端功能

### 搜索
- **拼音全拼匹配**：输入 `feishu` 匹配"飞书"
- **拼音首字母**：输入 `fs` 匹配"飞书"、"番茄小说"
- **模糊匹配**：输入字符按顺序出现在标题/拼音中即可匹配
- **原文匹配**：直接匹配中英文

### A-Z 字母索引
- 按网站首字母过滤（A-Z），中文归 `#`
- 仅在无搜索状态下显示

### 子分类筛选
- 每个大类下显示子分类芯片
- 点击过滤，显示数量

### 收藏
- 卡片左上角 ❤️ 爱心
- 点击切换收藏状态
- 未收藏：毛玻璃空心 `♡`
- 已收藏：红色 `❤️`
- 收藏时 hover 触发心跳动画
- "❤️ 收藏"标签查看所有收藏

### 卡片操作
- 右上角 `⋮` 三点菜单
- ✏️ 编辑 / 🗑 删除
- 点击卡片空白区域 → 打开网站

### 罗马模拟时钟
- 左上角 Canvas 绘制
- 罗马数字 I~XII
- 时针(金)、分针(青)、秒针(红)
- 完全响应式：字号、指针、刻度均按比例缩放
- 支持 DPR 高清渲染

### 个性设置
- 自定义主标题 / 副标题
- 存 localStorage，刷新不丢

## 启动方式

### 手动启动
```bash
cd E:\works\web-app
python app.py
# 浏览器打开 http://localhost:5000
```

### 开机自启
已配置 Windows 任务计划 `个人导航中心`：
- 每次登录后延迟 30 秒自动启动 Flask
- MySQL 需设为自动启动（默认已是）

### 桌面快捷方式
- 桌面 `个人导航中心.lnk`
- 指南针图标
- 双击打开 http://localhost:5000

## 维护工具

### 扩充网站
```bash
python expand_bookmarks.py     # 第一批扩充
python topup.py                # 分类补足
```

### 检测死链
```bash
python check_urls.py           # 并发50线程检测所有URL，自动清理不可达
```

### 重归类
```bash
python recategorize.py         # 网站域名精确映射到分类
python restructure.py          # 分类体系重构
```

## 回滚

```bash
git checkout 9df6c3f           # 拆分前单文件版本
git checkout a75995c           # 分包版本（低版本）
git checkout df89d5d           # v2.0 最新版本
```

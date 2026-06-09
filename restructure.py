"""重组分类：新增设计资源/游戏电竞，合并政务+健康→便民服务"""
import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', password='123456', database='pj1', buffered=True)
c = conn.cursor()

# Step 1: 合并政务服务+健康医疗 → 便民服务
c.execute("UPDATE categories SET cat_key='service', cat_name='便民服务', cat_color='#3b82f6' WHERE cat_key='gov'")
c.execute("DELETE FROM categories WHERE cat_key='health'")
c.execute("UPDATE bookmarks SET category='service' WHERE category IN ('gov','health')")
print('[OK] 政务服务+健康医疗 > 便民服务')

# Step 2: 新建设计资源和游戏电竞分类
for key, name, color in [('design', '设计资源', '#f59e0b'), ('game', '游戏电竞', '#8b5cf6')]:
    c.execute('INSERT IGNORE INTO categories (cat_key, cat_name, cat_color) VALUES (%s,%s,%s)', (key, name, color))
print('[OK] 设计资源 + 游戏电竞 分类已创建')

# Step 3: 从影音娱乐拆分游戏相关
GAME_KW = [
    ('twitch.tv','直播'), ('steampowered','平台'), ('epicgames','平台'), ('gog.com','平台'),
    ('roblox','平台'), ('ign.com','媒体'), ('gamespot','媒体'), ('nintendo','平台'),
    ('playstation','平台'), ('xbox','平台'), ('xiaoheihe','社区'),
    ('3dmgame','媒体'), ('gamersky','媒体'), ('ali213','媒体'),
    ('bbs.nga','社区'), ('虎牙','直播'), ('斗鱼','直播'),
]
for kw, sub in GAME_KW:
    c.execute("UPDATE bookmarks SET category='game', sub_category=%s WHERE category='media' AND (title LIKE %s OR url LIKE %s)", (sub, f'%{kw}%', f'%{kw}%'))
print('[OK] 游戏类从影音娱乐拆分')

# Step 4: 从办公/工具拆分设计资源
DESIGN_KW = [
    ('figma','设计工具'), ('canva','设计工具'), ('dribbble','设计社区'), ('behance','设计社区'),
    ('sketch','设计工具'), ('pixso','设计工具'), ('mastergo','设计工具'),
    ('mockplus','原型工具'), ('modao','原型工具'), ('lanhuapp','协作平台'),
    ('js.design','设计工具'), ('创客贴','模板素材'), ('gaoding','模板素材'),
    ('chuangkit','模板素材'), ('processon','绘图工具'), ('draw.io','绘图工具'),
    ('excalidraw','绘图工具'), ('lucidchart','绘图工具'), ('whimsical','绘图工具'),
    ('tldraw','绘图工具'), ('xmind','思维导图'), ('mubu','思维导图'),
    ('edrawsoft','绘图工具'), ('亿图','绘图工具'),
]
for kw, sub in DESIGN_KW:
    c.execute("UPDATE bookmarks SET category='design', sub_category=%s WHERE category IN ('office','tools') AND (title LIKE %s OR url LIKE %s)", (sub, f'%{kw}%', f'%{kw}%'))
print('[OK] 设计资源拆分完成')

# Step 5: 补充新网站
ADD = [
    # 设计资源
    ('design','图标资源','IconFont','https://www.iconfont.cn','阿里矢量图标库','🔣'),
    ('design','图标资源','Font Awesome','https://fontawesome.com','Web图标字体库','🔤'),
    ('design','图标资源','Feather Icons','https://feathericons.com','极简开源图标集','🪶'),
    ('design','图标资源','Heroicons','https://heroicons.com','Tailwind团队图标','🎯'),
    ('design','图标资源','Lucide','https://lucide.dev','开源图标库','✨'),
    ('design','字体资源','Google Fonts','https://fonts.google.com','谷歌免费Web字体','🔤'),
    ('design','字体资源','字体天下','https://www.fonts.net.cn','中英文字体下载','🀄'),
    ('design','字体资源','识字体网','https://www.likefont.com','字体识别与下载','🔍'),
    ('design','字体资源','DaFont','https://www.dafont.com','海外免费字体库','🔤'),
    ('design','字体资源','Font Squirrel','https://www.fontsquirrel.com','免费商用字体','🐿️'),
    ('design','图片素材','Unsplash','https://unsplash.com','免费高清摄影图片','📷'),
    ('design','图片素材','Pexels','https://www.pexels.com','免费素材图片视频','📸'),
    ('design','图片素材','Pixabay','https://pixabay.com','免费图片视频音频','🖼️'),
    ('design','图片素材','Freepik','https://www.freepik.com','海量矢量素材模板','📐'),
    ('design','配色工具','Coolors','https://coolors.co','配色方案生成器','🎨'),
    ('design','配色工具','Adobe Color','https://color.adobe.com','Adobe官方配色工具','🖌️'),
    ('design','配色工具','ColorHunt','https://colorhunt.co','精选配色调色板','🎯'),
    ('design','配色工具','中国色','https://zhongguose.com','中国传统色查阅','🏮'),
    ('design','配色工具','Gradient','https://gradient.style','CSS渐变生成','🌈'),
    ('design','设计灵感','Awwwards','https://www.awwwards.com','全球最佳网站设计奖','🏆'),
    ('design','设计灵感','SiteInspire','https://www.siteinspire.com','网站设计灵感收集','✨'),
    ('design','设计灵感','Mobbin','https://mobbin.com','App截屏设计参考','📱'),
    ('design','设计灵感','Collect UI','https://collectui.com','UI设计灵感分类库','🗂️'),
    ('design','在线工具','SVG Repo','https://www.svgrepo.com','免费SVG图标矢量','🔷'),
    ('design','在线工具','Remove.bg','https://www.remove.bg','AI一键去背景','🖼️'),
    ('design','在线工具','Waifu2x','https://waifu2x.udp.jp','二次元图片放大','🔍'),
    ('design','在线工具','Bigjpg','https://bigjpg.com','AI图片无损放大','🔎'),
    # 游戏电竞
    ('game','数字平台','itch.io','https://itch.io','独立游戏发布平台','🎲'),
    ('game','数字平台','TapTap','https://www.taptap.cn','手游发现与社区','📱'),
    ('game','数字平台','4399游戏','https://www.4399.com','中文小游戏门户','🎮'),
    ('game','电竞社区','Liquipedia','https://liquipedia.net','电竞百科维基','📖'),
    ('game','电竞社区','HLTV','https://www.hltv.org','CS2电竞数据新闻','🔫'),
    ('game','电竞社区','Dotabuff','https://www.dotabuff.com','Dota2数据统计','📊'),
    ('game','电竞社区','OP.GG','https://www.op.gg','LOL数据查询排名','🏆'),
    ('game','游戏资讯','Fami通','https://www.famitsu.com','日本权威游戏媒体','🇯🇵'),
    ('game','游戏资讯','游研社','https://www.yystv.cn','中文游戏文化媒体','🎮'),
    ('game','游戏资讯','机核','https://www.gcores.com','游戏电台文化社区','📻'),
    ('game','游戏公司','Riot Games','https://www.riotgames.com','英雄联盟拳头公司','🥊'),
    ('game','游戏公司','Blizzard','https://www.blizzard.com','暴雪娱乐官网','❄️'),
    ('game','游戏公司','米哈游','https://www.mihoyo.com','原神崩坏开发商','🎭'),
    ('game','游戏公司','鹰角网络','https://www.hypergryph.com','明日方舟开发商','🏹'),
    ('game','游戏公司','腾讯游戏','https://game.qq.com','腾讯游戏官网','🎮'),
    ('game','游戏公司','网易游戏','https://game.163.com','网易游戏官网','🎮'),
    ('game','游戏Mod','Nexus Mods','https://www.nexusmods.com','全球最大游戏Mod社区','🧩'),
    ('game','游戏Mod','CurseForge','https://www.curseforge.com','魔兽世界等Mod平台','🔧'),
    # 便民服务
    ('service','教育考试','中国教育考试网','https://www.neea.edu.cn','教育部考试中心','📝'),
    ('service','教育考试','教师资格证','https://ntce.neea.edu.cn','中小学教师资格','👩‍🏫'),
    ('service','公共服务','国家图书馆','https://www.nlc.cn','中国国家数字图书馆','📚'),
]

added = 0
for cat, sub, title, url, desc, icon in ADD:
    d = url.split('/')[2]
    c.execute('SELECT id FROM bookmarks WHERE url LIKE %s', (f'%{d}%',))
    if c.fetchone(): continue
    c.execute('INSERT INTO bookmarks (title,url,description,icon,category,sub_category) VALUES (%s,%s,%s,%s,%s,%s)', (title, url, desc, icon, cat, sub))
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

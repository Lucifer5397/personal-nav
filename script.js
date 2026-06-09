// ==================== API ====================
const API = '/api';

async function api(url, options = {}) {
    const res = await fetch(API + url, {
        headers: { 'Content-Type': 'application/json' },
        ...options
    });
    return res.json();
}

// ==================== 全局状态 ====================
let bookmarks = [];
let categories = {};
let currentFilter = 'all';
let currentSearch = '';
const DEFAULT_TITLE = '个人导航中心';
const DEFAULT_SUBTITLE = '通往数字世界的门户';

// ==================== 加载数据 ====================
async function loadBookmarks() {
    const resp = await api('/bookmarks');
    bookmarks = resp;
    renderBookmarks();
}

async function loadCategories() {
    const resp = await api('/categories');
    categories = {};
    resp.forEach(c => { categories[c.cat_key] = { name: c.cat_name, color: c.cat_color }; });
    renderCategoryNav();
    renderSettingsCatList();
    fillCategorySelect();
}

// ==================== 拼音模糊搜索（首字母+全拼） ====================
const CHAR_TO_PINYIN = {};
function buildCharPinyinMap() {
    const map = {
        'a':'啊阿安爱奥','ai':'爱艾碍哀矮','an':'安按案暗岸','ao':'奥傲熬凹澳',
        'ba':'巴八爸把霸','bai':'白百摆败拜','ban':'班办半板般','bang':'帮棒邦绑榜',
        'bao':'包宝保报爆','bei':'北贝背倍备','ben':'本奔笨','bi':'比必笔毕闭',
        'bian':'边变便遍编','biao':'标表彪','bie':'别憋','bin':'宾彬斌',
        'bing':'冰兵丙病','bo':'波播伯博薄','bu':'不布步部补',
        'ca':'擦茶差查','cai':'才采菜财猜','can':'参餐残','cang':'仓苍舱藏',
        'cao':'草操曹','ce':'册策测侧','ceng':'层曾蹭','cha':'查茶插差叉',
        'chai':'柴拆豺','chan':'产颤缠蝉馋','chang':'长常场厂唱','chao':'超朝潮抄吵',
        'che':'车扯彻撤','chen':'陈晨尘沉','cheng':'成城程乘承','chi':'吃迟池持尺',
        'chong':'冲虫崇充','chou':'抽仇愁筹丑','chu':'出处触楚初','chuan':'川传船穿',
        'chuang':'窗床创闯','chui':'吹垂锤','chun':'春纯唇','ci':'次此词刺赐',
        'cong':'从聪丛','cu':'粗促醋簇','cuan':'窜篡','cui':'催脆翠崔',
        'cun':'村存寸','cuo':'错搓挫措','da':'大达打答搭','dai':'代带待戴贷',
        'dan':'单但蛋淡胆','dang':'当党挡荡档','dao':'刀道到倒导','de':'的得德',
        'deng':'灯登等邓','di':'第地低底敌','dian':'点电店典殿','diao':'掉调吊雕',
        'die':'爹跌叠蝶','ding':'丁顶定订鼎','dong':'东动冬洞董','dou':'都斗豆逗兜',
        'du':'读独度毒堵','duan':'段断端短','dui':'对队堆兑','dun':'顿盾蹲敦',
        'duo':'多朵夺躲','e':'饿额鹅恶俄','en':'恩','er':'儿而耳二尔',
        'fa':'发法罚乏伐','fan':'反饭范翻凡','fang':'方放房防访','fei':'非飞肥废肺',
        'fen':'分粉份奋芬','feng':'风峰封丰疯','fo':'佛','fou':'否',
        'fu':'夫父付复负','ga':'嘎','gai':'该改盖钙','gan':'干感敢肝甘',
        'gang':'刚钢港岗','gao':'高搞告稿','ge':'个哥歌格革','gei':'给',
        'gen':'根跟','geng':'更耕耿','gong':'工公功宫弓','gou':'狗够勾沟购',
        'gu':'古谷股鼓故','gua':'瓜刮挂寡','guai':'怪拐乖','guan':'关管官观冠',
        'guang':'光广逛','gui':'归鬼贵桂规','gun':'滚棍','guo':'国果过郭锅',
        'ha':'哈蛤','hai':'海害还孩嗨','han':'汉含寒汗喊','hang':'行航杭',
        'hao':'好号浩豪毫','he':'和河喝合核','hei':'黑嘿','hen':'很恨痕狠',
        'heng':'横衡恒','hong':'红宏洪鸿','hou':'后厚候吼','hu':'虎护互湖呼',
        'hua':'花画华化话','huai':'坏怀淮','huan':'欢环缓幻换','huang':'黄皇荒慌',
        'hui':'回会灰挥辉','hun':'混婚昏魂','huo':'火或活获货',
        'ji':'机及几记集','jia':'家加假价甲','jian':'见间件建简','jiang':'将江讲降',
        'jiao':'叫交教角较','jie':'接节解界借','jin':'今金进近尽','jing':'经京景精静',
        'jiu':'就九酒旧救','ju':'居局具句举','juan':'卷捐鹃','jue':'觉决绝爵',
        'jun':'军君均菌俊','ka':'卡喀咖','kai':'开凯快楷','kan':'看刊堪砍',
        'kang':'康抗亢','kao':'考靠拷烤','ke':'可克科客课','ken':'肯垦恳',
        'kong':'空孔恐控','kou':'口扣寇','ku':'苦库哭酷枯','kua':'夸跨',
        'kuai':'快块筷','kuan':'宽款','kuang':'狂况矿筐','kui':'亏葵窥盔',
        'kun':'困昆坤','kuo':'扩括廓阔','la':'拉啦辣腊垃','lai':'来赖莱',
        'lan':'蓝兰烂拦懒','lang':'狼郎朗浪廊','lao':'老劳牢捞','le':'了乐勒',
        'lei':'雷累类泪垒','leng':'冷楞愣','li':'里李理力利','lian':'连脸练恋莲',
        'liang':'两亮梁良量','liao':'了聊料辽廖','lie':'列烈裂猎劣','lin':'林临邻淋',
        'ling':'零灵领令陵','liu':'流刘留六柳','long':'龙隆笼聋','lou':'楼漏露搂',
        'lu':'路鲁录陆鹿','lv':'绿旅吕律虑','luan':'乱卵','lun':'论轮伦',
        'luo':'罗落洛骆螺','ma':'马妈麻吗码','mai':'买卖麦埋迈','man':'满慢曼蛮漫',
        'mang':'忙芒盲莽','mao':'毛猫冒帽茂','me':'么','mei':'美每妹梅媒',
        'men':'门们闷','meng':'梦孟猛蒙盟','mi':'米密迷秘蜜','mian':'面免棉眠勉',
        'miao':'苗秒妙描','min':'民敏闽','ming':'明名命鸣冥','mo':'摸磨魔墨末',
        'mu':'木目母牧墓','na':'那拿哪纳钠','nai':'乃耐奶奈','nan':'男南难',
        'nao':'脑闹挠','ne':'呢讷','nei':'内','neng':'能','ni':'你尼泥逆倪',
        'nian':'年念粘碾','niang':'娘酿','ning':'宁凝拧','niu':'牛扭纽',
        'nong':'农弄浓脓','nv':'女','nuan':'暖','nuo':'诺挪懦',
        'ou':'欧偶藕鸥呕','pa':'怕爬趴帕啪','pai':'拍排派牌','pan':'盘判盼潘攀',
        'pang':'旁胖庞','pao':'跑炮泡抛','pei':'配陪培赔佩','pen':'盆喷',
        'peng':'朋棚碰蓬鹏','pi':'皮批匹屁辟','pian':'片偏篇骗','piao':'票飘漂',
        'pie':'撇瞥','pin':'拼品贫频聘','ping':'平评瓶屏萍','po':'破坡婆迫',
        'pu':'普扑铺葡朴','qi':'起其七期气','qia':'恰洽掐','qian':'前钱千浅牵',
        'qiang':'强墙枪抢','qiao':'桥巧敲翘','qie':'切且窃茄','qin':'亲秦琴勤侵',
        'qing':'青清情晴轻','qiu':'秋求球丘','qu':'去曲取区趣','quan':'全权泉圈',
        'que':'却缺确雀','qun':'群裙','ran':'然染燃','rang':'让嚷壤',
        'rao':'绕扰饶','re':'热惹','ren':'人认任忍仁','reng':'扔仍',
        'ri':'日','rong':'容荣融冗','rou':'肉柔揉','ru':'如入乳儒',
        'ruan':'软阮','rui':'瑞锐蕊','run':'润闰','ruo':'若弱',
        'sa':'撒洒萨','sai':'赛塞腮','san':'三散伞珊','sang':'桑丧嗓',
        'sao':'扫骚嫂','se':'色涩瑟','sen':'森','sha':'沙杀傻厦啥',
        'shai':'晒筛','shan':'山闪善扇衫','shang':'上商伤赏','shao':'少烧哨绍',
        'she':'社设舍蛇舌','shen':'深申神身审','sheng':'生声升胜圣','shi':'是十时事市',
        'shou':'手收首守受','shu':'书数树属输','shua':'刷耍','shuai':'帅衰摔',
        'shuang':'双霜爽','shui':'水谁睡税','shun':'顺瞬','shuo':'说硕朔',
        'si':'四死思司私','song':'送松宋颂','sou':'搜艘','su':'苏素速诉宿',
        'suan':'算酸蒜','sui':'虽随岁碎穗','sun':'孙损笋','suo':'所索缩锁',
        'ta':'他她它塔踏','tai':'太台泰态胎','tan':'谈坦叹摊滩','tang':'唐堂糖汤躺',
        'tao':'桃逃讨套涛','te':'特','teng':'腾疼藤','ti':'提体题替梯',
        'tian':'天田甜填添','tiao':'条跳挑调','tie':'铁贴帖','ting':'听停庭挺亭',
        'tong':'同通痛童铜','tou':'头投透偷','tu':'图土突涂徒','tuan':'团',
        'tui':'推腿退','tun':'吞屯臀','tuo':'脱托拖驼妥',
        'wa':'挖哇蛙瓦袜','wai':'外歪','wan':'万完玩晚湾','wang':'王网往望亡',
        'wei':'为位未味微','wen':'文问温闻稳','weng':'翁嗡','wo':'我握窝卧',
        'wu':'五无物务屋','xi':'西系喜细洗','xia':'下夏霞虾瞎','xian':'先现县线显',
        'xiang':'向想香乡相','xiao':'小笑校消晓','xie':'写些谢协歇','xin':'新心信辛欣',
        'xing':'星行兴性姓','xiong':'兄雄凶胸','xiu':'休修秀袖锈','xu':'许需虚续序',
        'xuan':'宣选旋轩悬','xue':'学雪血穴','xun':'寻训讯迅勋',
        'ya':'呀压牙亚雅','yan':'言眼烟严研','yang':'阳样养洋杨','yao':'要药摇腰遥',
        'ye':'也夜业叶野','yi':'一以意医依','yin':'因音引银阴','ying':'应英影硬营',
        'yong':'用永勇拥泳','you':'有又由油优','yu':'于与余鱼雨','yuan':'元原园远院',
        'yue':'月越约岳悦','yun':'云运允韵孕',
        'za':'杂砸咱','zai':'在再载灾宰','zan':'赞暂','zang':'藏脏',
        'zao':'早造澡噪糟','ze':'则责择泽','zei':'贼','zen':'怎',
        'zeng':'增赠','zha':'扎炸渣札闸','zhai':'摘宅债斋寨','zhan':'占站展战盏',
        'zhang':'张章长掌仗','zhao':'找照招赵兆','zhe':'这者折哲浙','zhen':'真针珍振镇',
        'zheng':'正争整证政','zhi':'之只支知直','zhong':'中重种众忠','zhou':'周州舟宙',
        'zhu':'主住注祝助','zhua':'抓爪','zhuai':'拽','zhuan':'转专砖赚',
        'zhuang':'装庄壮桩','zhui':'追锥坠','zhun':'准','zhuo':'捉桌卓灼',
        'zi':'子自字紫资','zong':'总宗棕踪','zou':'走奏邹','zu':'足组祖租阻',
        'zuan':'钻纂','zui':'最醉罪嘴','zun':'尊遵','zuo':'做左坐座昨',
    };
    for (const [py, chars] of Object.entries(map)) {
        for (const ch of chars) {
            if (!CHAR_TO_PINYIN[ch]) CHAR_TO_PINYIN[ch] = py;
        }
    }
}
buildCharPinyinMap();

function getPinyin(text) { return [...text].map(ch => CHAR_TO_PINYIN[ch] || ch).join(''); }

function getPinyinInitials(text) { return [...text].map(ch => (CHAR_TO_PINYIN[ch] || ch)[0] || ch).join(''); }

function pinyinFuzzyMatch(text, query) {
    if (!query) return true;
    const lower = text.toLowerCase();
    const q = query.toLowerCase();
    // 1. 直接匹配
    if (lower.includes(q)) return true;
    // 2. 全拼匹配（如 feishu → 飞书）
    const fullPinyin = getPinyin(text).toLowerCase();
    if (fullPinyin.includes(q)) return true;
    // 3. 首字母匹配（如 fs → 飞书）
    if (getPinyinInitials(text).includes(q)) return true;
    // 4. 首字母按序匹配（如 fs → 飞书文档）
    let qi = 0;
    const initials = getPinyinInitials(text);
    for (const ch of initials) { if (ch === q[qi]) qi++; if (qi >= q.length) return true; }
    // 5. 原文按序模糊
    qi = 0;
    for (const ch of lower) { if (ch === q[qi]) qi++; if (qi >= q.length) return true; }
    return false;
}

// ==================== 渲染 ====================
let azLetter = 'all';
let subcatFilter = 'all';

function renderCategoryNav() {
    const nav = document.getElementById('categoryNav');
    nav.innerHTML = '';

    // 收藏标签
    const favBtn = document.createElement('button');
    favBtn.className = 'category-btn';
    favBtn.dataset.category = 'favorites';
    favBtn.textContent = '❤️ 收藏';
    favBtn.onclick = () => { currentFilter = 'favorites'; azLetter = 'all'; subcatFilter = 'all'; renderBookmarks(); updateActiveCat('favorites'); buildAZBar(); renderSubcatFilter(); };
    nav.appendChild(favBtn);

    const allBtn = document.createElement('button');
    allBtn.className = 'category-btn active';
    allBtn.dataset.category = 'all';
    allBtn.textContent = '全部';
    allBtn.onclick = () => { currentFilter = 'all'; azLetter = 'all'; subcatFilter = 'all'; renderBookmarks(); updateActiveCat('all'); buildAZBar(); renderSubcatFilter(); };
    nav.appendChild(allBtn);
    Object.keys(categories).forEach(key => {
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.dataset.category = key;
        btn.textContent = categories[key].name;
        btn.onclick = () => { currentFilter = key; azLetter = 'all'; subcatFilter = 'all'; renderBookmarks(); updateActiveCat(key); buildAZBar(); renderSubcatFilter(); };
        nav.appendChild(btn);
    });
}

function updateActiveCat(cat) {
    document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
    const btn = document.querySelector(`.category-btn[data-category="${cat}"]`);
    if (btn) btn.classList.add('active');
}

function buildAZBar() {
    const bar = document.getElementById('azBar');
    bar.innerHTML = '';
    const allBtn = document.createElement('button');
    allBtn.className = 'az-btn' + (azLetter === 'all' ? ' active' : '');
    allBtn.dataset.letter = 'all';
    allBtn.textContent = '全';
    allBtn.addEventListener('click', () => {
        azLetter = 'all';
        renderBookmarks();
        buildAZBar();
    });
    bar.appendChild(allBtn);
    const set = new Set();
    let list = currentFilter === 'all' ? bookmarks : bookmarks.filter(b => b.category === currentFilter);
    list.forEach(b => {
        const ch = b.title.charAt(0).toUpperCase();
        if (ch >= 'A' && ch <= 'Z') set.add(ch);
        else set.add('#');
    });
    const letters = [...set].sort();
    letters.forEach(l => {
        const btn = document.createElement('button');
        btn.className = 'az-btn' + (azLetter === l ? ' active' : '');
        btn.dataset.letter = l;
        btn.textContent = l;
        btn.addEventListener('click', () => {
            azLetter = l;
            renderBookmarks();
            buildAZBar();
        });
        bar.appendChild(btn);
    });
}

function renderSubcatFilter() {
    const container = document.getElementById('subcatFilter');
    if (!container) return;
    const set = new Map();
    let list = currentFilter === 'all' ? bookmarks : bookmarks.filter(b => b.category === currentFilter);
    list.forEach(b => {
        if (b.sub_category) {
            set.set(b.sub_category, (set.get(b.sub_category) || 0) + 1);
        }
    });
    if (set.size <= 1) { container.style.display = 'none'; return; }
    container.style.display = 'flex';
    container.innerHTML = '';
    const allChip = document.createElement('span');
    allChip.className = 'subcat-chip' + (subcatFilter === 'all' ? ' active' : '');
    allChip.textContent = '全部';
    allChip.addEventListener('click', () => {
        subcatFilter = 'all';
        renderBookmarks();
        renderSubcatFilter();
    });
    container.appendChild(allChip);
    for (const [name, cnt] of set) {
        const chip = document.createElement('span');
        chip.className = 'subcat-chip' + (name === subcatFilter ? ' active' : '');
        chip.textContent = `${name}(${cnt})`;
        chip.addEventListener('click', () => {
            subcatFilter = name;
            renderBookmarks();
            renderSubcatFilter();
        });
        container.appendChild(chip);
    }
}

function renderBookmarks() {
    const grid = document.getElementById('bookmarkGrid');
    const noRes = document.getElementById('noResults');
    let filtered;
    if (currentFilter === 'favorites') {
        filtered = bookmarks.filter(b => b.is_favorited);
    } else if (currentFilter === 'all') {
        filtered = bookmarks;
    } else {
        filtered = bookmarks.filter(b => b.category === currentFilter);
    }

    // A-Z 过滤
    if (azLetter !== 'all') {
        filtered = filtered.filter(b => {
            const ch = b.title.charAt(0).toUpperCase();
            if (azLetter === '#') return !(ch >= 'A' && ch <= 'Z');
            return ch === azLetter;
        });
    }

    // 子分类过滤
    if (subcatFilter !== 'all') {
        filtered = filtered.filter(b => b.sub_category === subcatFilter);
    }

    // 模糊搜索
    const s = currentSearch.trim();
    if (s) {
        filtered = filtered.filter(b =>
            pinyinFuzzyMatch(b.title, s) ||
            pinyinFuzzyMatch(b.description, s) ||
            pinyinFuzzyMatch(b.url, s) ||
            (categories[b.category] && pinyinFuzzyMatch(categories[b.category].name, s))
        );
    }

    // 无搜索时更新 A-Z 条
    if (!currentSearch.trim()) buildAZBar();

    if (filtered.length === 0) {
        grid.innerHTML = '';
        noRes.style.display = 'block';
        return;
    }
    noRes.style.display = 'none';
    grid.innerHTML = '';
    filtered.forEach((b, i) => {
        const card = document.createElement('div');
        card.className = 'bookmark-card';
        const subTag = b.sub_category ? `<span class="bookmark-subcat">${b.sub_category}</span>` : '';
        const heartClass = b.is_favorited ? 'fav-heart favorited' : 'fav-heart';
        card.innerHTML = `
            <span class="${heartClass}" data-id="${b.id}">${b.is_favorited ? '❤️' : '♡'}</span>
            <button class="card-menu-btn" title="更多操作">⋮</button>
            <div class="card-menu-dropdown">
                <div class="menu-item edit-item">✏️ 编辑</div>
                <div class="menu-item danger del-item">🗑 删除</div>
            </div>
            <div class="bookmark-icon">${b.icon || '🌐'}</div>
            <div class="bookmark-title">${b.title}</div>
            <div class="bookmark-desc">${b.description || ''}</div>
            <span class="bookmark-cat" style="color:${(categories[b.category]||{}).color||'#fff'}">${(categories[b.category]||{}).name||b.category}${subTag}</span>
        `;
        // 收藏点击
        card.querySelector('.fav-heart').addEventListener('click', async (e) => {
            e.stopPropagation();
            const resp = await api(`/bookmarks/${b.id}/favorite`, { method: 'PUT' });
            if (!resp.error) {
                b.is_favorited = resp.is_favorited;
                await loadBookmarks();
            }
        });
        const menuBtn = card.querySelector('.card-menu-btn');
        const dropdown = card.querySelector('.card-menu-dropdown');

        menuBtn.onclick = (e) => {
            e.stopPropagation();
            // 关闭其他已打开的菜单
            document.querySelectorAll('.card-menu-dropdown.show').forEach(d => {
                if (d !== dropdown) d.classList.remove('show');
            });
            dropdown.classList.toggle('show');
        };
        card.querySelector('.edit-item').onclick = (e) => {
            e.stopPropagation();
            dropdown.classList.remove('show');
            openEditModal(b);
        };
        card.querySelector('.del-item').onclick = (e) => {
            e.stopPropagation();
            dropdown.classList.remove('show');
            deleteBookmark(b.id);
        };
        card.onclick = (e) => {
            // 点击卡片本体打开链接（排除菜单区域）
            if (e.target.closest('.card-menu-btn') || e.target.closest('.card-menu-dropdown')) return;
            window.open(b.url, '_blank');
        };
        grid.appendChild(card);
        setTimeout(() => card.classList.add('loaded'), i * 25);
    });

    // 全局点击关闭菜单
    if (!document._menuCloseBound) {
        document.addEventListener('click', () => {
            document.querySelectorAll('.card-menu-dropdown.show').forEach(d => d.classList.remove('show'));
        });
        document._menuCloseBound = true;
    }
}

// ==================== CRUD ====================
async function addBookmark() {
    const title = prompt('网站标题:');
    if (!title) return;
    const url = prompt('网址 (https://...):');
    if (!url) return;
    const desc = prompt('描述:') || '';
    const icon = prompt('图标 emoji:', '🌐') || '🌐';
    let catOpts = Object.keys(categories).map(k => `${k}=${categories[k].name}`).join(', ');
    const cat = prompt(`分类 (${catOpts}):`, 'tools') || 'tools';

    await api('/bookmarks', {
        method: 'POST',
        body: JSON.stringify({ title, url, description: desc, icon, category: cat })
    });
    await loadBookmarks();
}

async function deleteBookmark(id) {
    if (!confirm('确定删除？')) return;
    await api(`/bookmarks/${id}`, { method: 'DELETE' });
    await loadBookmarks();
}

async function saveBookmark(e) {
    e.preventDefault();
    const id = document.getElementById('editId').value;
    const data = {
        title: document.getElementById('editTitle').value,
        url: document.getElementById('editUrl').value,
        description: document.getElementById('editDesc').value,
        icon: document.getElementById('editIcon').value,
        category: document.getElementById('editCategory').value,
    };
    if (id) {
        await api(`/bookmarks/${id}`, { method: 'PUT', body: JSON.stringify(data) });
    } else {
        await api('/bookmarks', { method: 'POST', body: JSON.stringify(data) });
    }
    document.getElementById('editModal').classList.remove('show');
    await loadBookmarks();
}

function openEditModal(bm = null) {
    document.getElementById('editId').value = bm ? bm.id : '';
    document.getElementById('editTitle').value = bm ? bm.title : '';
    document.getElementById('editUrl').value = bm ? bm.url : '';
    document.getElementById('editDesc').value = bm ? bm.description : '';
    document.getElementById('editIcon').value = bm ? bm.icon : '🌐';
    document.getElementById('editModalTitle').textContent = bm ? '编辑书签' : '添加书签';
    fillCategorySelect(bm ? bm.category : 'tools');
    document.getElementById('editModal').classList.add('show');
}

function fillCategorySelect(selected = 'tools') {
    const sel = document.getElementById('editCategory');
    sel.innerHTML = '';
    Object.keys(categories).forEach(key => {
        sel.innerHTML += `<option value="${key}" ${key === selected ? 'selected' : ''}>${categories[key].name}</option>`;
    });
}

// ==================== 设置 ====================
function renderSettingsCatList() {
    const container = document.getElementById('catList');
    container.innerHTML = Object.keys(categories).map(key => `
        <div class="cat-item">
            <span class="cat-name">${categories[key].name}</span>
            <div class="cat-actions">
                <button onclick="editCategory('${key}')">修改</button>
                <button onclick="deleteCategory('${key}')">删除</button>
            </div>
        </div>
    `).join('');
}

async function addCategory() {
    const input = document.getElementById('newCatName');
    const name = input.value.trim();
    if (!name) return;
    const key = name.replace(/\s+/g, '-').toLowerCase();
    const colors = ['#ff6b6b','#4ecdc4','#45b7d1','#96ceb4','#feca57','#ff9aa2','#e2f0cb'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    const resp = await api('/categories', {
        method: 'POST',
        body: JSON.stringify({ cat_key: key, cat_name: name, cat_color: color })
    });
    if (resp.error) { alert(resp.error); return; }
    input.value = '';
    document.getElementById('addCatDialog').style.display = 'none';
    document.getElementById('showAddCatDialogBtn').style.display = '';
    await loadCategories();
}

function showAddCatDialog() {
    document.getElementById('addCatDialog').style.display = 'block';
    document.getElementById('showAddCatDialogBtn').style.display = 'none';
    const input = document.getElementById('newCatName');
    input.value = '';
    input.focus();
}

function hideAddCatDialog() {
    document.getElementById('addCatDialog').style.display = 'none';
    document.getElementById('showAddCatDialogBtn').style.display = '';
    document.getElementById('newCatName').value = '';
}

async function editCategory(key) {
    const newName = prompt('新名称:', categories[key].name);
    if (!newName || newName.trim() === categories[key].name) return;
    await api(`/categories/${key}`, { method: 'PUT', body: JSON.stringify({ cat_name: newName.trim() }) });
    await loadCategories();
    await loadBookmarks();
}

async function deleteCategory(key) {
    if (!confirm(`删除分类 "${categories[key].name}"？该分类下书签将移至"工具"。`)) return;
    await api(`/categories/${key}`, { method: 'DELETE' });
    await loadCategories();
    await loadBookmarks();
}

// ==================== 个性设置 ====================
function loadSiteConfig() {
    const title = localStorage.getItem('siteTitle') || DEFAULT_TITLE;
    const subtitle = localStorage.getItem('siteSubtitle') || DEFAULT_SUBTITLE;
    document.getElementById('heroTitle').textContent = title;
    document.getElementById('heroSubtitle').textContent = subtitle;
}

function savePersonalize() {
    const title = document.getElementById('settingTitle').value.trim() || DEFAULT_TITLE;
    const subtitle = document.getElementById('settingSubtitle').value.trim() || DEFAULT_SUBTITLE;
    localStorage.setItem('siteTitle', title);
    localStorage.setItem('siteSubtitle', subtitle);
    document.getElementById('heroTitle').textContent = title;
    document.getElementById('heroSubtitle').textContent = subtitle;
    document.getElementById('personalizeSaved').style.display = 'inline';
    setTimeout(() => {
        document.getElementById('personalizeSaved').style.display = 'none';
    }, 2000);
}

function initPersonalizeTab() {
    document.getElementById('settingTitle').value = localStorage.getItem('siteTitle') || DEFAULT_TITLE;
    document.getElementById('settingSubtitle').value = localStorage.getItem('siteSubtitle') || DEFAULT_SUBTITLE;
    document.getElementById('personalizeSaved').style.display = 'none';
}

document.getElementById('savePersonalizeBtn').addEventListener('click', savePersonalize);
['settingTitle', 'settingSubtitle'].forEach(id => {
    document.getElementById(id).addEventListener('keydown', (e) => {
        if (e.key === 'Enter') savePersonalize();
    });
});

// ==================== 背景动画 ====================
function initBackground() {
    const canvas = document.getElementById('bgCanvas');
    const ctx = canvas.getContext('2d');
    let w, h, particles = [];

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const count = Math.floor(w * h / 2500);
    for (let i = 0; i < count; i++) {
        particles.push({
            x: Math.random() * w, y: Math.random() * h,
            size: Math.random() * 1.5 + 0.5,
            speed: Math.random() * 0.5 + 0.1,
            angle: Math.random() * Math.PI * 2,
            opacity: Math.random() * 0.3 + 0.1,
            color: Math.random() > 0.7 ? '#ffd700' : '#00ffff'
        });
    }

    function animate() {
        const grad = ctx.createLinearGradient(0, 0, 0, h);
        grad.addColorStop(0, '#0a0815');
        grad.addColorStop(1, '#120f25');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);
        particles.forEach(p => {
            p.x += Math.cos(p.angle) * p.speed;
            p.y += Math.sin(p.angle) * p.speed;
            if (p.x < 0) p.x = w;
            if (p.x > w) p.x = 0;
            if (p.y < 0) p.y = h;
            if (p.y > h) p.y = 0;
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.opacity;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;
        requestAnimationFrame(animate);
    }
    animate();
}

// ==================== 罗马数字模拟时钟 ====================
const ROMAN = ['XII', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI'];

function drawAnalogClock() {
    const canvas = document.getElementById('analogClock');
    const ctx = canvas.getContext('2d');
    const r = canvas.width / 2;
    const now = new Date();
    const h = now.getHours() % 12;
    const m = now.getMinutes();
    const s = now.getSeconds();

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 表盘
    ctx.beginPath();
    ctx.arc(r, r, r - 2, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(15,12,26,0.85)';
    ctx.fill();
    ctx.strokeStyle = 'rgba(0,255,255,0.5)';
    ctx.lineWidth = 2;
    ctx.stroke();

    // 外圈装饰环
    ctx.beginPath();
    ctx.arc(r, r, r - 4, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(255,215,0,0.25)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // 罗马数字
    ctx.font = 'bold 12px "Georgia", "Times New Roman", serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    for (let i = 0; i < 12; i++) {
        const angle = (i * 30 - 90) * Math.PI / 180;
        const x = r + (r - 32) * Math.cos(angle);
        const y = r + (r - 32) * Math.sin(angle);
        ctx.fillStyle = '#ffd700';
        ctx.shadowColor = 'rgba(255,215,0,0.5)';
        ctx.shadowBlur = 4;
        ctx.fillText(ROMAN[i], x, y);
        ctx.shadowBlur = 0;
    }

    // 分钟刻度
    for (let i = 0; i < 60; i++) {
        const angle = (i * 6 - 90) * Math.PI / 180;
        const isHour = i % 5 === 0;
        const inner = isHour ? r - 14 : r - 6;
        const outer = r - 2;
        ctx.beginPath();
        ctx.moveTo(r + inner * Math.cos(angle), r + inner * Math.sin(angle));
        ctx.lineTo(r + outer * Math.cos(angle), r + outer * Math.sin(angle));
        ctx.strokeStyle = isHour ? 'rgba(255,215,0,0.7)' : 'rgba(255,255,255,0.2)';
        ctx.lineWidth = isHour ? 2.5 : 0.6;
        ctx.stroke();
    }

    // 时针
    const hAngle = ((h + m / 60) * 30 - 90) * Math.PI / 180;
    drawHand(ctx, r, hAngle, r * 0.4, 'rgba(255,215,0,0.9)', 3.5);

    // 分针
    const mAngle = ((m + s / 60) * 6 - 90) * Math.PI / 180;
    drawHand(ctx, r, mAngle, r * 0.55, 'rgba(0,255,255,0.85)', 2.5);

    // 秒针
    const sAngle = (s * 6 - 90) * Math.PI / 180;
    drawHand(ctx, r, sAngle, r * 0.65, '#ff6b6b', 1);

    // 中心点
    ctx.beginPath();
    ctx.arc(r, r, 4, 0, Math.PI * 2);
    ctx.fillStyle = '#fff';
    ctx.fill();
    ctx.beginPath();
    ctx.arc(r, r, 2.5, 0, Math.PI * 2);
    ctx.fillStyle = '#0f0c1a';
    ctx.fill();
}

function drawHand(ctx, r, angle, length, color, width) {
    ctx.beginPath();
    ctx.moveTo(r, r);
    ctx.lineTo(r + length * Math.cos(angle), r + length * Math.sin(angle));
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    ctx.stroke();
}

function startAnalogClock() {
    drawAnalogClock();
    setInterval(drawAnalogClock, 1000);
}

// ==================== 初始化 ====================
async function init() {
    document.body.classList.add('page-loaded');
    loadSiteConfig();
    initBackground();
    startAnalogClock();

    await loadCategories();
    await loadBookmarks();
    buildAZBar();
    renderSubcatFilter();

    // 搜索
    document.getElementById('searchInput').addEventListener('input', (e) => {
        currentSearch = e.target.value;
        renderBookmarks();
    });

    // 添加书签按钮
    document.getElementById('addBookmarkBtn').addEventListener('click', addBookmark);

    // 编辑表单
    document.getElementById('editForm').addEventListener('submit', saveBookmark);
    document.getElementById('closeEditModal').addEventListener('click', () => {
        document.getElementById('editModal').classList.remove('show');
    });

    // 设置模态框
    document.getElementById('settingsBtn').addEventListener('click', () => {
        renderSettingsCatList();
        initPersonalizeTab();
        document.getElementById('settingsModal').classList.add('show');
    });
    document.getElementById('closeSettings').addEventListener('click', () => {
        document.getElementById('settingsModal').classList.remove('show');
    });

    // 设置tab切换
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab + 'Tab').classList.add('active');
        });
    });

    // 添加分类 - 对话框模式
    document.getElementById('showAddCatDialogBtn').addEventListener('click', showAddCatDialog);
    document.getElementById('confirmAddCatBtn').addEventListener('click', addCategory);
    document.getElementById('cancelAddCatBtn').addEventListener('click', hideAddCatDialog);
    document.getElementById('newCatName').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') addCategory();
        if (e.key === 'Escape') hideAddCatDialog();
    });

    // 点击模态框背景关闭
    document.querySelectorAll('.modal').forEach(m => {
        m.addEventListener('click', (e) => { if (e.target === m) m.classList.remove('show'); });
    });

    // 键盘快捷键 Ctrl+数字 打开对应书签
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key >= '1' && e.key <= '9') {
            const idx = parseInt(e.key) - 1;
            if (idx < bookmarks.length) window.open(bookmarks[idx].url, '_blank');
        }
    });
}

document.addEventListener('DOMContentLoaded', init);
</script>

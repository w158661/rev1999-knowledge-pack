# 16 · GitHub 写作技能蒸馏报告（2026 活跃项目）

> 蒸馏官视角：聚焦「反AI通用怪病」「角色一致性」「叙事一致性」三方面的可落地最佳实践。
> 数据采集时间：2026-08-10。所有 star 数 / 更新时间来自 GitHub API（未认证，可能有延迟）。
> 采集方法：GitHub Search API 5 组查询（claude skill writing / fiction writing prompt claude / creative writing ai skill / 小说写作 claude / novel writer llm agent），按 updated 排序取 2025-01 之后项目；README 与关键文件经 raw.githubusercontent 抓取原文。
> 诚实标注：查询 4（`小说写作+claude`）命中 API 速率限制未取回结果（已用其他中文项目补偿）；`denova` README 在 main 分支 404（实际默认分支为 master，已改取）；个别 raw 抓取超时重试后成功。

---

## 1. 项目总览表

| 项目 | 链接 | 最后更新 | Star | 类型 | 一句话 |
|---|---|---|---|---|---|
| MrGeDiao/shuorenhua（说人话） | https://github.com/MrGeDiao/shuorenhua | 2026-08-10 | 992 | Claude/Codex skill（中文去AI味） | 中文 AI 味清理 skill，带保真合同、场景分档、84 条盲测评测集 |
| iLearn-Lab/NovelClaw | https://github.com/iLearn-Lab/NovelClaw | 2026-08-09 | 361 | 长篇写作工作台（FastAPI+多Agent） | 动态记忆优先的长篇协作框架，会话/分镜/手稿/记忆库全可检视 |
| alfredxw/denova | https://github.com/alfredxw/denova | 2026-08-10 | 590 | Go 写作/互动叙事平台 | 小说创作+AI RPG 平台，资料库/Agent/Change Review/本地版本管理 |
| existential-birds/beagle | https://github.com/existential-birds/beagle | 2026-08-10 | 75 | Agent Skills 市场 | 含 review-ai-writing / humanize 写作检查技能（另有独立 humanize 库） |
| lza6/AIWriteX-Skills | https://github.com/lza6/AIWriteX-Skills | 2026-08-09 | 45 | OpenClaw Skill 集 | 7 阶段认知工作流 + 去AI化 + E-E-A-T 质量审计 |
| ARMANDSnow/make-ur-Agent-writer | https://github.com/ARMANDSnow/make-ur-Agent-writer | 2026-08-06 | 19 | 多Agent 小说续写流水线（Python） | Analyzer→辩论→规划→Writer→5+1 reviewer 的工业级续写管道 |
| xiaoyuCR7/long-novel-skill | https://github.com/xiaoyuCR7/long-novel-skill | 2026-08-10 | 3 | 通用网文创作 skill（Claude Code 等） | 长篇网文全流程：三级大纲/7 Gate去AI腔/人物防OOC/跨Agent审核 |
| Lucasli6833/slop-cop | https://github.com/Lucasli6833/slop-cop | 2026-08-10 | 3 | 散文审计 skill | 双轴（AI味+可读性）密度评分审计，45+150+33+35 模式目录 |
| Ghostproof-265/ghostproof-lite | https://github.com/Ghostproof-265/ghostproof-lite | 2026-07-11 | 2 | 免费编辑约束 prompt | 15 条让 AI 小说像人写的编辑铁律（完整引擎 265+ 规则） |
| newesp/novel-generator | https://github.com/newesp/novel-generator | 2026-07-31 | 2 | 本地小说工具（Tauri） | Planner/Writer/Critic/Editor 四角色多Agent + LLM Wiki + 版本管理 |
| jastfkjg/InkMind | https://github.com/jastfkjg/InkMind | 2026-06-01 | 2 | 小说写作工作台 | AI 助手悬浮面板：上下文感知、生成→预览→确认→落库 |
| lumitive/lumi-style | https://github.com/lumitive/lumi-style | 2026-08-10 | 1 | 写作风格 skill | 设计语言+文风打包为 skill：规则必须溯源到真实交付迭代 |
| RooseveltElias/human-voice | https://github.com/RooseveltElias/human-voice | 2026-08-10 | 1 | Claude 写作 skill | 基于学术写作经典+AI 模式目录，爬虫每日更新模式库 |
| gentilijuanmanuel/writing-skills | https://github.com/gentilijuanmanuel/writing-skills | 2026-07-07 | 1 | Claude Code skill 集 | John Gardner《小说艺术》批改框架：逐层批评、绝不代写 |
| eshaanjain26/no-ai-slop-humanizer | https://github.com/eshaanjain26/no-ai-slop-humanizer | 2026-08-09 | 0 | Claude skill | 合并 humanizer+no-ai-slop：32 模式 + Detect 模式 + 最小有效编辑 |
| douglaz/skills（voice-dna 等） | https://github.com/douglaz/skills | 2026-08-10 | 0 | 跨工具 skill 集 | voice-dna 人声强制、多审稿人循环、可测标准的工程化写作检查 |
| cantus-industries/agentic-writers-room | https://github.com/cantus-industries/agentic-writers-room | 2026-07-29 | 0 | 多Agent 写作系统案例 | 10+ Agent 四层架构：Bible 持久态/生成-验证分离/6 人设评审会 |
| kino-6/novelcraft-agent | https://github.com/kino-6/novelcraft-agent | 2026-04-27 | 0 | 本地 Ollama 续写管道 | Analyzer→Director→Skills→Writer→Polish 五段式小模型续写 |
| brian-caylor/StoryEngine_Template | https://github.com/brian-caylor/StoryEngine_Template | 2026-04-13 | 0 | 故事引擎模板 | 结构化故事引擎模板（大纲-场景-修订） |

---

## 2. 深度分析

### 2.1 MrGeDiao/shuorenhua（说人话）——中文反AI味标杆

**机制说明**
- **保真合同（Fidelity Contract）**：改稿前先划 `protected spans`（数字、版本、命令、路径、报错、引用原文、人名、责任归属），并记一份「事实关系账本」——谁对什么做了什么、数字修饰哪个对象。改完逐条对账。
- **场景分档**：`chat / status / docs / public-writing` 四场景各有默认力度（minimal / standard / aggressive）与处理策略；README、release note、论坛帖、issue 回复命中后进对应 Scene Pack。
- **Tier 分级**：Tier 1（默认替换：套话、黑话、谄媚）／Tier 2（聚集信号：同段 2-3 个渲染词才标）／Tier 3（全文密度信号：重要/关键/核心）。Tier 只描述命中强度，不等于改写力度。
- **scope 三档**：`structural`（自由删并重排）／`bounded`（长文默认：整句空话进「建议删除（待确认）」清单交用户拍板，防长文越改越短）／`in-place`（一句不删，只句内降调）。
- **两遍回读**：Pass 1 保真回读（protected spans 漂移/信息丢失/语域/术语/生硬断裂 + 分析-输出一致性）；Pass 2 Residual Audit 只查 5 件事（开场残留/总结残留/narrator 残留/空泛判断残留/节奏过匀）。
- **无源引用三模式**：`rewrite-safe`（删权威铺垫后不依赖来源可独立成立才保留，否则删整条）/ `audit-only`（不补来源、不装已证实）/ `rewrite-with-placeholder`（仅用户要求保留结构时）。
- **工程化评测**：84 条盲测、双模型判分、L1 硬约束 0 失败才可发布、误杀率 <10% 门槛；规则层 210+ 中文短语、96 条英文短语、20 类结构反模式。

**可借鉴点**
- 「先保信息，再谈风格」应写进任何去AI味 prompt 的第一行。
- 长文去味必须有「长度不缩水」合同（bounded/in-place），否则模型会越改越短。
- 禁止「删掉数字留下更泛断言」（把 p95 480→160ms 改成"明显降低"= 失败）。
- 误杀防护与改写同样重要：原句引用、命令、术语、责任主体默认保留。
- 用评测集+硬约束用例驱动规则迭代，而不是拍脑袋加词表。

### 2.2 xiaoyuCR7/long-novel-skill——网文全流程工业标准

**机制说明**
- **Iron Law 七铁律**：禁跳章节闭环、禁裸写正文（无章纲不写）、禁正文混元信息、禁一章清光主线（每章必留钩子+至少新增一个未解决问题）、禁越界加速（A/B/C 配额单章至多 1 项）、禁任意改主线（改纲须作者确认+级联）、不替作者做决定。
- **文件系统即记忆**：每本书一个工程目录（大纲/设定/正文/追踪/对标/参考资料），对话只负责创作，一切状态落盘。
- **三级大纲体系**：总纲（一句话主线+分卷规划+终局储备边界+红线）→ 卷纲（卷契约+剧情单元+情绪弧线+大纲锚点配额）→ 章纲（情节点+字数预算+钩子+A/B/C 配额预声明）。滚动补纲：一次只补一个剧情单元，已写区间锁定只增不改。
- **7 Gate 去AI腔**：Gate A 禁用词（仿佛/不禁/嘴角勾起/眼底闪过…白名单豁免）／Gate B 毒句式（不是A而是B/没有X只有Y/这一刻/带着…）／Gate C 心理告知（他很紧张→他的手在抖）／Gate D 节奏均匀（排比堆叠/段落齐整）／Gate E 对话腔调（遮名字认人）／Gate F 结尾升华（总结/点题/感慨）／Gate G 解释腔上帝感（她不知道的是/之所以…是因为/这意味着）。机器+人工各一遍；叙述/对话分域扫描；删除比例上限（轻度≤15%/中度≤25%/重度≤35%）；两遍式润色。
- **防OOC四防线**：人物卡写「不变量」（核心性格≤3词+行为示例、底线与恐惧、口癖与声线）／角色状态文件记「变量」（身份/能力/关系/近期变更，变化必须有因）／写前只提取「不知道就会写错」的信息（最小上下文）／写后更新+三问自查。
- **跨Agent审核协议**：每 10 章异源送审（优先不同模型→同源多会话→同会话降级），三维度报告（逻辑硬伤/阅读体验/去AI化），P0 立即改/P1 卷内改/P2 下次修订，单章最多 3 轮防死循环。
- **机器闸口**：check_text（7 Gate+字数+禁用词+伏笔超期）、rhythm_guard（A/B/C配额+事件冷却）、normalize_punct、style_fingerprint 对比文风锚；写完一章「机器闸口→自查清单→更新五追踪文件」，欠账门不过禁止写下一章。

**可借鉴点**
- 一致性不是靠提示词"记住"，而是靠目录结构+追踪文件+写前恢复流程（resume.py）。
- 「每章必留钩子+至少新增一个未解决问题」是防"一章清光主线"的硬规则。
- 心理告知外化表（告诉 vs 展示）是最有效的防AI味样例库。
- 删除上限+白名单防止过度去AI味（把正常描写误杀）。
- 异源审核是发现同源模型盲区的关键手段；降级路径要显式声明。

### 2.3 iLearn-Lab/NovelClaw——动态记忆长篇框架

**机制说明**
- **不以一次生成事件处理长篇**：会话（session）、分镜（storyboard）、手稿面（manuscript）、世界观/角色/风格面板、可编辑记忆库（memory banks）构成持续工作区。
- **可检视运行**：worker.log、progress.log、chapter 输出、下载件全部暴露。progress.log 事件序列：`global_outline`（总纲落盘）→ `chapter_outline_ready` → `chapter_plan` → `chapter_length_plan` → `memory_snapshot`（记忆快照刷新）→ `character_setting / world_setting`（设定记忆回写）。
- **记忆闭环**：每次生成后把角色/世界设定「写回」记忆库，下章从记忆恢复上下文，而不是靠对话续接。
- **人机协同**：作者持续把舵（steering），所有表面（手稿/分镜/记忆库）可编辑可检视。

**可借鉴点**
- 长篇写作工具的最低要求：每章产出「机器可读的状态快照」，供下一章加载。
- 记忆库必须可编辑（作者能修正 AI 记错的事实）。
- 把「生成-检视-回写」做成显式事件序列（progress log），而不是黑盒对话。

### 2.4 Lucasli6833/slop-cop——双轴散文审计

**机制说明**
- **双轴双判词**：AI-Slop 轴（读起来像不像 AI 写的：模式/词汇/格式/节奏）+ Comprehension 轴（冷读者能不能跟上：缩写轰炸/命名实体轰炸/电报体/可读性）。一个作品可以一轴过一轴挂。
- **密度评分**：`density = (H×3) + (M×1) + (L×0.25) / 每500词`；0-2 PASS / 2-5 LOW / 5-10 MEDIUM / 10-18 HIGH / 18+ CRITICAL。单次命中不是信号，密度才是。
- **致命tell清单**：词汇（delve/tapestry/underscore/leverage/harness）、句式（"It's not X, it's Y"否定翻转、"serves as a"系词回避、"-ing尾巴"、假范围"From small startups to global enterprises"）、声音（"Great question!"、"I hope this helps!"、"In today's fast-paced world"）、结构（In conclusion/Furthermore、throat-clearing、破折号 3+/500词、加粗开头bullet）。
- **校准原则**：文体调整（学术文允许 studies show；百科文易误报）、受众校准（FK 年级带 7-9 网页/6-8 营销/10-12 技术/12-16 学术）、复合触发器升级一档（100词窗口 3+ 未定义缩写、5+ 命名实体…）、uncanny valley（8+ 弱tell堆叠+burstiness<0.5 升级一档）。
- **sanded-prose 警报**：词表干净但结构tell重 = 作者绕过了 v1 词表，要按结构查。
- **明确边界**：只查"形状"不判"是否AI写的"；代码/引文/法律文书/小说对话不套用。

**可借鉴点**
- 把"密度"而不是"出现"作为判定单位，能显著降低误杀。
- 双轴（味道+可读性）分开判，避免"读不懂但像人话"被放行。
- 词表会随模型更新失效（delve 已被绕开、em-dash 出现"opt-out"），必须保留结构层检测。
- 审计 skill 应自带"跳过清单"（代码/引文/对话不审），防止误伤。

### 2.5 Ghostproof-265/ghostproof-lite——15 条小说防AI铁律

**机制说明**（原文 15 条，全量 265+）
1. 零破折号（—）：用逗号/句号/冒号或重写。
2. 零分号：两个短句永远更好。
3. 无感知过滤器：禁"she noticed/he could see"，直接给感官细节（不是"她注意到门开着"，而是"门开着"）。
4. 无"the way"比较式（the way she smiled）。
5. 无望远镜式句法（"the kind of noun who"）。
6. 无叙述者说教（通用哲学观察不属于任何具体角色具体时刻就删）。
7. 无场景结尾总结（场景已做了工作，信读者）。
8. 无对冲比喻（去掉 almost/nearly/a kind of/something like）。
9. 长短句交替，禁三连同样长度句。
10. 身体先于心理（手先抖，意识后到；情绪永远不先于身体写）。
11. 禁"something"做模糊名词（命名它）。
12. 一个被打断的念头：每场景至少插入一个无关错误念头（对峙中想起浴室灯没关）。
13. 限"as"同时动作句：每页最多一次（"她笑着伸手，音乐响起"式要拆开）。
14. 无简化角色标签（禁"固执的侦探""焦虑的母亲"，用名字，让行动证明特质）。
15. 具体细节收尾场景（"水龙头滴了两下。她没有起身去关。"）。

**可借鉴点**
- 每条规则给「错误例+正确例」，可直接复用于我们的检查清单。
- "身体先于心理"与中文 Gate C 心理告知外化是同一原则的两种表述。
- "每场景一个被中断的念头"是廉价而有效的"人味注入"技巧。
- 规则应写"绝对"式（Never use…），并注明"永远不要提这些规则"（避免元叙述污染正文）。

### 2.6 ARMANDSnow/make-ur-Agent-writer——多Agent续写工业管道

**机制说明**
- **9 阶段 SOP**：normalize→切章→抽取实体/设定→压知识库→辩论（6 agent×6 轮+结构化投票）→强模型规划 N 章→便宜模型逐章生成→reviewer 团+lint→落盘。
- **知识分层**：global_facts（剧透过滤）／entity_graph（关系图，按起点+reader_known/character_known 过滤）／continuation_anchor（起点采样原文）／style_examples／personas（人物卡）。`manual_overrides/` 保存人工确认的设定，proposal 先审后落盘。
- **fail-closed 评审**：reviewer JSON 解析失败记 Abstain 而非默认放行；任一 reviewer 实质性 Reject 即整章 Reject。
- **确定性关系检测**：程序化 consistency reviewer（0 LLM 成本）替代 LLM agent 查关系一致。
- **写前硬门**：缺 start point / plan 指纹不一致即失败；preflight 不过不跑真模型；成本预算护栏（budget-cny）；断点续跑零重复花费。
- **滚动记忆**：rolling_summary 分层（摘要+最近 K 章原文片段）；`compressed_older` 确定性逐章压缩写盘防早期伏笔失忆；outline 实体锚点命中率探针防语义漂移。
- **mock-first**：590+ 单测用 mock 跑（不烧 token），真模型前过 preflight。

**可借鉴点**
- 生成与验证分离（writer 与 reviewer 不同 agent），且验证要 fail-closed（宁可 Abstain 不可错放）。
- 剧透过滤（reader_known/character_known）是续写类功能防知识污染的硬需求。
- 规划与写作分工：强模型规划+弱模型执行+评审团把关，成本与质量兼顾。
- 状态永远从盘面推导，不靠记忆（state 文件只存参数，进度从产物反推）。

### 2.7 cantus-industries/agentic-writers-room——四层写作系统案例

**机制说明**
- **Layer 1 持久态（Story Bible）**：9 个人类可读文件——premise+三幕大纲、角色圣经、连续性账本（append-only 记录伤害/债务/承诺直至解决）、时间线、风格指南、跨会话记忆索引。每个 agent 行动前必读，多个写回。
- **风格指南教训**：早期用形容词（"少用破折号"），agent 不服从；改为「数字上限+完全禁令」（numeric caps and flat bans），由 editor **grep-and-count** 而非"判断"。
- **Layer 2 生产线**：作者下达按 beat 限定范围的章节任务→orchestrator 分解并按模型档位路由（起草用最强散文模型，审稿降一档省钱）→book-writer（spec-locked：永不改大纲、不发明情节，越界必须标记）→book-editor（只审不改，生成与验证分离、权限分离）→作者之声回读（人引导，反复出现的修改被提升进 writer 简报，让系统越来越不需要人）。
- **Layer 3 评审会**：6 个读者人设（历史现实/角色弧线/散文工艺/世界观/节奏张力/读者留存）并行审稿，每人设权重化 rubric 六维评分，产出共识矩阵而非 6 份相同意见；**评审与写作平台分离**（不同厂商不同失败模式）。评审结论不可溯源即无效；不完整的评审会永远不能给出通过（fail-loud）。
- **Layer 4 写作实验室**：本地服务器流式推送人设裁决，作者在真实渲染的章节上对照评审。

**可借鉴点**
- "生成器与验证器必须分离——最好分离平台"，写手不能审批自己的作品。
- 人类门（human gate）+ 回写循环（write-back）：被接受的修正回写 Bible，同一错误不会发两次。这是"自纠正"而非"自动化"。
- 不可测量的标准不自我执行——把所有规则转成数字上限与禁令，让编辑器去 grep。

### 2.8 eshaanjain26/no-ai-slop-humanizer——voice-preservation 编辑框架

**机制说明**
- 合并 blader/humanizer（Wikipedia《Signs of AI writing》25 模式）+ petergyang/no-ai-slop 的 7 模式=32 模式。
- **Detect 模式**：只点名模式+引原句+给几个词的改法，不重写不打分不猜"是不是AI写的"——点名即证据。
- **声音保留框架**：编辑前先识别 3-5 个声音信号；应用**最小有效编辑**（minimum effective edit）；每个听起来通用的句子过**可迁移测试**（portability test：这句话换任何人都成立吗？成立=填充词，删或变具体）。
- **新增 7 模式**：伪洞见铺垫（faux-insight setups）、冒号揭晓（colon reveals）、诠释性元话语（interpretive metadiscourse）、戏剧性碎片化、修辞设问、伪深刻收尾（fake-profound kickers）、总结复述结尾（summary-recap endings）。
- 最终核查清单（formal verification checklist）在交付前强制运行。

**可借鉴点**
- "最小有效编辑"原则可防止去AI味过度改写破坏个人风格。
- 可迁移测试是判断填充句的黄金标准。
- Detect/Audit 模式与 Edit 模式分离，让用户先诊断后决定。

### 2.9 douglaz/skills（voice-dna）——可机检的人声契约

**机制说明**
- Apply/Check 双模式；规则按"LLM 违反频率"排序，最常见的最靠前。
- **致命模式（fatal pattern）**："不是 X，是 Y"否定翻转——全篇出现 1 例即整篇不过审；AI 从营销文案学到这一招，否定不增加任何信息，直接陈述肯定句。
- **禁用词族**：死语言（delve/dive into/unpack/harness/leverage/utilize/landscape/realm/robust）、死过渡（furthermore/additionally/moreover/moving forward/at the end of the day）、互动诱饵（let that sink in/read that again/this changes everything）、AI 尬词（supercharge/unlock/future-proof/10x）。
- **Stop Slop 审计层**：假主体（data tells us…→我们读了数据发现…）、被动藏行为者、模糊宣言（the implications are significant→点名）、修辞脚手架（"Here's what I mean:"）、引语诱饵。
- **自检清单 10 条**：交付前逐条过（禁词/段落句数/破折号/缩略/开场信息量/否定翻转/假主体/被动/模糊重要性/脚手架），发现问题直接修，不报告用户。
- 声音规则本身克制：诚实含糊（I think/probably）、句首 So/But/And、括号插话是合法人味，不套用更严的通用反slop规则。

**可借鉴点**
- "否定翻转出现即整篇失败"这类单点否决规则可执行性最强。
- 自检清单在交付前自动执行（无需用户触发）。
- 反slop规则与声音规则分层（voice rules > generic anti-slop），避免互相冲突。

### 2.10 alfredxw/denova——资料库驱动的叙事一致性

**机制说明**
- **事实分层单真源**：历史事实以已提交的 Turn 为真源；当前可计算事实归 Actor State；稳定设定归资料库（角色/世界观/地点/势力/规则/物品）；未来意图归 director.md。Agent 通过有界回合历史检索找回早期事实，**不维护第二套可写真源**。
- **上下文管理**：模型上下文按来源、用途、大小上限组织，避免完整历史/日志/设定无界塞进对话。
- **Change Review**：Agent 修改在累计 Diff 中审阅、评论、撤销；基于本地 Git 版本管理+跨重启 Undo/Redo。
- **故事导演**：开局结合资料库安排舞台/角色/势力/线索/风险；每回合保证新信息/关系变化/压力/收益/代价/悬念；已保存 AI 回复可直接修正无需重生成。

**可借鉴点**
- 设定按"稳定度"分库（稳定设定/当前状态/历史事实/未来意图），每类一种管理方式。
- "不维护第二套可写真源"是防漂移的根本纪律（一切以提交产物为准）。
- 所有 AI 修改必须经过 Diff 审阅才能落库。

### 2.11 newesp/novel-generator（小说產生器）——四角色多Agent+知识图谱

**机制说明**
- **单 Writer 快速生成 / Planner / Writer / Critic / Editor 四角色高质量 Multi-Agent**。
- 书→大纲→角色→章节正文→版本→LLM Wiki→全文检索（SQLite FTS5）→知识图（Graph）。
- **Context Budget Manager**：Wiki 摘要 + pick-pages（按需挑页）+ 摘要质量检查，控制上下文预算。
- **不可变创作语言契约**：每本书创作语言建立后锁定，内建 prompt 按书语言选用，用户自定义 prompt 也不能覆盖语言契约。
- 创作语言与界面语言分离，题材/风格/章节节拍以稳定代码存储。

**可借鉴点**
- Critic/Editor 与 Writer 分离并纳入正式流程（非可选优化）。
- 知识以 Wiki+Graph 形式沉淀并可全文检索，而非依赖上下文拼接。
- 把"语言/风格契约"设为不可覆盖约束，防止多轮对话中漂移。

### 2.12 lumitive/lumi-style——规则溯源纪律

**机制说明**
- 每条规则追溯到真实交付迭代或读者评审（"nothing here was written from thin air"），防止拍脑袋规则。
- 术语红线（terminology red lines）、禁词表、标点纪律、数字纪律（number discipline）单文件集中。
- **symlink 而非 copy**：安装副本会静默落后于规则版本，链接保证单一版本真源。
- 机器可验证的 conformance 与"人读着有意图才算完成"区分——机械检查只证形式合规。

**可借鉴点**
- 规则库必须"有出处"：每条规则配来源（真实案例/读者反馈），否则会被推翻。
- 风格规则与交付物打包发布（规则引用的字体/图标/资产随包走）。
- 用固定任务套件+得分表跟踪跨 agent 的一致性（conformance 面板）。

---

## 3. 蒸馏出的「通用防AI怪病规则集」（60 条）

> 综合 shuorenhua、long-novel-skill、slop-cop、ghostproof-lite、humanizer/no-ai-slop、voice-dna、human-voice、agentic-writers-room 等全部项目。可直接用于我们技能的防幻觉/去AI味章节。

### A. 语言与词汇层（1-14）

1. 建立并维护禁用词表（中文一级：仿佛、似乎、不禁、不由得、一丝、眼底闪过、嘴角勾起、嘴角上扬、意味深长、若有所思、不容置疑、众所周知、值得一提的是、不得不、映入眼帘、心中暗道、沉声道、淡淡地说、脸色一变、身形一顿、目光如炬、目光深邃；英文：delve、tapestry、underscore、leverage、harness、utilize、landscape、realm、robust）。
2. 禁用词只能换成具体动作/细节描写，不能简单换成另一个形容词（禁"仿佛"→禁用一个近义词替代，要重写场景）。
3. 单点命中不是信号，密度才是信号：同段 2+（短段<100字）或 3+（长段≥100字）聚集才处理（Tier 2 规则）。
4. 高频"渲染词"（重要、关键、核心、提升；significant、innovative、effective）只在全文密度明显过高时处理（Tier 3），不逐处替换。
5. 白名单机制：术语、人名、专有名词、题名可豁免（.deslop-whitelist 文件，命中段子串在白名单中跳过）。
6. 禁"不是A，而是B"（最毒中文AI句式）：直接写后项，或改成动作/细节；英文版 "It's not X, it's Y" 出现 1 例即整篇不过审（voice-dna 单点否决）。
7. 禁"没有X，只有Y"万能对比、"这一刻，"起手式、"…，带着…"万能状语、"声音不大，却带着…"声音套话、"之所以…是因为"解释因果、"仿佛/犹如/宛若/如同"文言腔比喻。
8. 禁系词回避式（"serves as a"、"stands as a"、"boasts"），直接写是什么。
9. 禁假范围（"从初创到全球企业"式 false range："From small startups to global enterprises"）。
10. 禁"something"做模糊名词（"something shifted in her expression"→命名它）。
11. 修饰词清扫：名词前形容词/定语/副词/量词多余即删（"白色的药片"→"药片"，一次只用一个形容词）。
12. 重复语义四类必查：形容词重复（兴高采烈地笑着跑过来）、近义词重复（非常重要的关键问题）、含义重复（我好饿，肚子咕咕叫）、主语重复（上文"药扔了一地"，下文"地上的药"）。
13. 禁模糊对冲比喻：去掉"almost、nearly、a kind of、something like"，承诺意象（"almost like a physical weight"→"a physical weight"）。
14. 英文禁词族：死过渡（Furthermore/Additionally/Moreover/Moving forward/At the end of the day）、互动诱饵（Let that sink in/Read that again/This changes everything）、AI尬词（Supercharge/Unlock/Future-proof/10x your productivity）。

### B. 句式与结构层（15-26）

15. 禁否定翻转/二元对比骨架（不是X而是Y、与其X不如Y）：多数删前半句直接说 Y。
16. 禁过度平行/排比堆叠：打断连续排比（保留 1-2 个删其余）。
17. 禁"rule of three"三连排比机械套用（英文模式，规则三连）。
18. 禁同义替换循环（synonym cycling：同一句换个近义词重复）。
19. 禁望远镜式句法（"the kind of noun who"、"the sort of noun that"），直接展示。
20. 禁"the way"比较式（"the way she smiled"）。
21. 禁"-ing"尾巴论断（"X happened, demonstrating Y"，superficial -ing analyses）。
22. 禁冒号揭晓（colon reveals：前文吊胃口、冒号后揭晓的伪洞见句式）。
23. 禁诠释性元话语（interpretive metadiscourse："这里值得注意的是…"）。
24. 禁修辞脚手架（"Here's what I mean:"、"Think about it:"、"What if…"、"The rest of this essay explains…"）。
25. 禁修辞设问堆叠（rhetorical setups）。
26. 禁假洞见铺垫（faux-insight setups："Here's the part nobody's talking about"）。

### C. 叙述与视角层（27-38）

27. 心理告知外化（最重要的中文防AI味操作）：直接陈述情绪改为身体/动作展示——"他很紧张"→"他的手在抖"；"她很愤怒"→"她一把掀翻了桌子"。
28. 身体先于心理：身体反应先于意识处理（手先抖，然后才明白为什么）；永远不先写情绪后写身体。
29. 禁感知过滤器（perception filters）："她注意到""他看到""他听见""她感到""他观察"→直接给感官细节（"她注意到门开着"→"门开着"）。
30. 禁叙述者说教（narrator editorialising）：通用哲学观察不属于任何具体角色具体时刻就删（"Sometimes the hardest battles are the ones we fight inside ourselves"）。
31. 禁上帝剧透（"她不知道的是""殊不知""多年以后"、"little did she know"）。
32. 禁解释腔/安排感：删"之所以…是因为""这意味着""事实证明"，因果让读者自己拼；叙述者不得跳出解释、剧透、定性、升华。
33. 禁总结复述结尾（summary-recap endings）：场景结尾不再述情绪内容（"他明白了这意味着什么"）。
34. 禁伪深刻收尾（fake-profound kickers：一句话金句收尾升华）。
35. 禁结尾升华（Gate F）：删"这次经历让他成长了"式总结；用动作/场景收尾，不用感慨收尾。
36. 禁简化角色标签（"固执的侦探""焦虑的母亲"），用名字，让行动证明特质。
37. 场景结尾落在具体物理细节而非感受（"厨房水龙头滴了两下。她没有起身去关。"）。
38. 禁复述设定（说明文入侵）：设定只挂在动作/冲突/细节上；"如果删掉这段情节完全不受影响"的说明性段落就是设定复述，删。

### D. 节奏与形式层（39-47）

39. 长短句交替：禁连续三句相似长度；长句后跟短句，连续短句后放开（ghostproof 第 9 条；slop-cop 的 burstiness 指标）。
40. 段落长短交错：不要每段都 3-5 行；一段 1-2 句是默认，3 句是上限（voice-dna：段落超 4 句必拆）。
41. 标点纪律：零破折号或密度上限（3+/500 词=HIGH）；省略号/感叹号堆叠清掉；中文"……""——"改成动作、短句、换行；破折号/分号是 AI 用量的 3-5 倍。
42. 对话标签去膨胀："沉声道""淡淡地说"统一用"说"或删标签。
43. 对话加人味：口语化表达（嗯/哦/行吧）、适当打断、答非所问、用动作穿插对话、删解释性对话（角色不会把自己的动机说清楚）。
44. 声线差异检查（Gate E）：遮住名字能认出谁说的吗？认不出=危险，全员一个声是AI味重灾。
45. 每个场景至少插入一个被打断的念头（one thought, interrupted：对峙中想起浴室灯没关）——最廉价的"人味注入"。
46. 限"as"同时动作句（每页最多一次），中文对应限"一边…一边…/…着…"连用。
47. 允许轻微不对称与不完整句：偶尔用不完整句（口语感），不要每句信息完整、逻辑清晰、表达精准。

### E. 内容与事实保真层（48-55）

48. 保真合同第一条：数字与修饰对象一起保——删渲染词后数字必须原样在（p95 从 480ms 降到 160ms 不许概括成"明显降低"）。
49. 关系不许改写：潜力≠实现（"展示云原生架构的潜力"不能改成"采用云原生架构"）；先后关系、归属关系不得编造（"两个团队"不能扩成"换过两个团队"）。
50. 时间跨度不漂移："未来十年"不能缩成"未来几年"或糊成"未来"。
51. 抽象不许擅自具体化：原文只说"提升效率"，不能改成"省时间/降成本"；同义改写不得改变谓词方向、完成态、强度、效果类型。
52. 缺信息不许编：原文没给数据，允许更短更直白，但不补数字、工具名、来源、机构、年份、研究名称；宁可标注"原文缺具体依据"。
53. 无源引用三模式：`rewrite-safe`（删铺垫后能独立成立才保留）/ `audit-only`（点明缺来源，不装已证实）/ `rewrite-with-placeholder`（仅用户要求保留结构）；不要删掉数字后留下更泛的同向断言（删 40% 后说"会更快"=失败）。
54. 分析-输出一致性：判定"原文没有某对象/关系"后，输出里就不能出现该对象/关系；每个"X 做 Y/X 基于 Y"必须能在原文谓词中找到依据，不能靠同段共现推断。
55. 禁止用同段共现补关系：同段提到 AI 和写作工具，不能据此写成"AI 处理写作工具"。

### F. 流程与质检层（56-60）

56. 分级处理：轻度（禁用词≤5处/千字）只过词表+句式；中度（6-15处或连续3+句式）过 7 Gate；重度（>15处或 7 Gate 中 4+ 有问题）全文重写重点段。
57. 删除比例上限：轻度≤15%、中度≤25%、重度≤35%；超限分段处理并标注 [需复核]；删除前必须确认不含伏笔/钩子/角色特征/情节推进/必要信息。
58. 两遍式润色：第一遍逐段清模式；第二遍自审"这段哪里还明显像AI？"列出 3-5 条具体问题再改。
59. 改后回读两遍：Pass 1 保真回读（protected spans 漂移/信息丢失/语域统一/术语失真/生硬断裂+分析-输出一致性）；Pass 2 Residual Audit 只查 5 件（开场残留/总结残留/narrator 残留/空泛判断残留/节奏过匀），第二遍只允许轻量修正，不重写全文。
60. 质检必须 fail-loud + 可验证：机器可查的用脚本（grep-and-count、正则、密度计数），不可查的进人工清单；评审失败必须记录，不完整的评审永远不能给出通过；质量门禁产物落盘（gate report）供跨会话消费。

---

## 4. 蒸馏出的「角色一致性 / 记忆管理最佳实践」

### 4.1 角色卡的「不变量 / 变量」双层结构（long-novel-skill）

- **人物卡 = 不变量**：核心性格压到 3 个词以内、每个词配一条行为示例（"记仇"→谁踩过他他记在小本子上）；底线与恐惧（角色"绝不做什么""最怕什么"）是判断任何情节是否 OOC 的试金石；口癖与声线（口头禅、句式习惯、一段示例台词）。
- **角色状态文件 = 变量**：当前身份、当前能力、关键关系、近期变更。只追踪主要角色（出场≥3 次或有独立剧情线），路人不入表。
- **演进必须有因**：成长弧光允许人设演进，但必须事件驱动、逐章积累，不接受"为了这段剧情他刚好变了"。

### 4.2 OOC 四种典型与处置（防崩人设）

1. 行为 OOC（谨慎者无谋而动）
2. 语言 OOC（沉默者突然话痨、粗人突然引经据典）
3. 能力 OOC（实力随剧情需要伸缩且无成长交代）
4. 关系 OOC（宿敌无故信任、挚友无故疏远）
- 单章内发现：直接改行为与台词，不改人设卡。
- 多章后既成漂移：二选一——①回补：安排事件解释转变；②认账：修改更早章节（未发布部分）。
- 人物卡修订 = 改纲级联：同步检查未写章纲、伏笔台账、角色状态，一次改完波及面。

### 4.3 写前筛选：最小上下文纪律（long-novel-skill / make-ur-Agent-writer 共识）

- 写每章前只提取「不知道就会写错」的信息：本章出场角色各自当前状态（处境/能力/关系位置）、本章涉及的旧账（谁和谁有过节、谁知道什么秘密）、本章的世界约束。
- 与本章无关的背景不加载——上下文稀释是 OOC 的温床（模型会用错位信息填空）。
- 单章前置读取上限 4 文件（long-novel-skill）；NovelClaw 用"记忆快照"机制每次生成后刷新。

### 4.4 三问自查（写后必答）

1. 本章角色的关键选择，换到 TA 的底线和动机上说得通吗？
2. 本章的对话，遮住名字能认出是谁说的吗？
3. 角色间的关系距离，和上一章相比的变化有交代吗？

### 4.5 程序化关系一致性（make-ur-Agent-writer）

- 用确定性检测（deterministic_relations，0 LLM 成本）替代 LLM 查实体关系一致。
- entity_graph 带阅读者可见性标注（reader_known / character_known），续写时按 POV 过滤剧透。
- 写后 propose_entity_advance → 人工/自动 apply（带 min-confidence 阈值），状态变更与 plan 冲突时 dry-run 拦截。

### 4.6 连续性账本（agentic-writers-room）

- Append-only 记录角色的伤害、债务、承诺，每项追踪到解决——所有 agent 行动前读它，多个 agent 写回。
- 同一错误不会发两次：被接受的修正回写 Bible，未来每个草稿继承修复（write-back loop）。

### 4.7 记忆分层的工程纪律

| 层 | 内容 | 管理方式 | 来源 |
|---|---|---|---|
| 稳定设定 | 世界观/规则/人物底设 | 资料库/人物卡，仅人工或走级联可改 | denova / NovelClaw |
| 当前状态 | 身份/能力/关系/伤势 | 角色状态文件，每章回写+变更记录一行 | long-novel-skill |
| 历史事实 | 已发生的剧情 | 章节摘要+实体→章节索引（BM25 检索），改已提交章节=违规 | make-ur-Agent-writer |
| 未来意图 | 大纲/导演计划 | director.md / 大纲文件，改纲须级联 | denova / long-novel-skill |
| 跨会话记忆 | 学到的工作经验 | 记忆索引，可编辑 | NovelClaw / writers-room |

- 铁律：不维护第二套可写真源（一切以提交产物为准，进度从盘面推导）。
- 断更/换人恢复：读 总纲→卷纲→最近章纲→近10章摘要→角色状态→伏笔台账→节奏配额，这就是交接包。

---

## 5. 蒸馏出的「长文写作流程最佳实践」（大纲→写作→修订）

### 5.1 推荐总流程（综合 long-novel-skill / make-ur-Agent-writer / writers-room）

```
Phase 0 定位与加载：找书工程→读题材定位→恢复会话（最新章/门禁/追踪同步/伏笔超期）→有欠账先补账
Phase 1 开书：创意→题材定位→读者契约→世界观与人物卡→文风锚→敏感词表→总纲→首卷卷纲→首批章纲（5-10章停靠）
Phase 2 大纲分级：总纲（一句话主线+卷规划+终局储备边界）→卷纲（卷契约+剧情单元+锚点配额+情绪弧线）→章纲（情节点+字数预算+钩子+配额预声明）；滚动补纲，一次一个剧情单元，已写区间锁定
Phase 3 单章循环：欠账门→读章纲→最小上下文检索→压速记→写正文→机器闸口（7Gate/节奏/标点/文风）→自查清单→更新五追踪文件
Phase 4 审稿：章级（机器+人工清单）→卷级（多视角盲评/跨Agent审核 P0/P1/P2）
Phase 5 发布：按平台规则调格式/简介/标签；硬指标以官方公告为准
Phase 6 续写/断更恢复：resume 诊断→补追踪→重读近5章摘要+角色状态→续写
Phase 7 大修：冻结→改纲→圈定受影响章→逐章修订→追踪回写
```

### 5.2 大纲层规则

- **三级大纲各管一件事**：总纲管方向（全书锚，改动=重大决策须作者确认）、卷纲管结构（卷契约必须兑现，交不出=水了一卷）、章纲管执行（情节点带字数预算 Σ∈[目标, 目标×1.1]）。
- **大纲锚点配额**：卷内主线锚点 2-3 个、关系锚点 ≤2、秘密锚点 ≤2、高潮锚点 1（卷末）；锚点总数每卷 ≤6，锚点间隔 ≥3 章，不能连续两章集中爆发。
- **终局储备边界**：总纲标明终局前不能动用的底牌（终局真相/战力/关系）；每卷检查是否透支。
- **改纲级联**：改总纲→查各卷卷纲→未写章纲→伏笔台账→人物卡→终局储备；改卷纲→查未写章纲→伏笔埋收→锚点配额→档位分布；人物设定变更视同改纲。级联结果写进文件批注，"不留脑子里记得要改的账"。
- **A/B/C 配额**（节奏预算制）：A 主线实质推进 / B 关系决定升级 / C 核心秘密揭露，单章至多触发 1 项，同类冷却 2 章；快档章后必须是慢/中档；事件类型有独立冷却与 gentle_window。

### 5.3 单章写作循环细节

- **结构四拍**：承接→发展→结算→钩子。章首 10% 接住上章钩子；章尾必有钩子且下一章接得住。
- **章间衔接工艺**：上章钩子承诺的危机，本章前 30% 内兑现或推进（过 30% 没接=欺骗读者）；上章末人物/物件/信息在本章首合理位置（线索簿三查）；场景转换三问（在哪/过了多久/谁在场）；情绪无断崖（高能章后有余波小节）；呼应至少一处前文细节。
- **欠账门**：上一章门禁/追踪未清，禁止开写下一章（机器可验：--verify-prev）。
- **最小上下文**：文风锚→出场人物卡+状态→近 5-10 章摘要→伏笔台账🟡/🔴→本章世界观条目→敏感词代称；历史细节用实体索引定位章节后 Grep 原文，不凭印象写。
- **机器闸口序列**：标点归一化→7 Gate+字数+伏笔超期→节奏配额→文风指纹偏离检测（每 5-10 章一次）；FAIL 全部处理完才进下一步。

### 5.4 追踪五文件（每章必更新，缺一不可）

1. **章节摘要**（关键实体宁多勿漏；"承上/启下"两栏必填——这是断更恢复的依据）
2. **角色状态**（有变化的角色更新+变更记录一行）
3. **伏笔台账**（新埋登记🟡/回收销账✅/检查超期🔴）
4. **时间线**（明确时间推移时追加）
5. **节奏配额**（A/B/C 触发+事件类型+档位记录）

### 5.5 审稿与修订体系

- **章级 vs 卷级分工**：章级=单章机器闸口+人工清单（回答"这章有没有硬伤"）；卷级=多视角盲评（追读读者/新读者/平台编辑/同行作者，回答"这卷作为商品读者买账吗"）。
- **跨Agent审核（异源优先）**：路由表 Claude→Codex/GPT（异源最高）→同源新会话（中）→同会话切视角（低，须标注仅供参考）；每 10 章批量送审（盲审原则：不给大纲/人物卡/创作意图，防审核官被意图带偏）；三维度报告（逻辑硬伤：角色已死又出现/时间线错乱/主线矛盾/设定冲突/伏笔断线/能力越界；阅读体验：弃书点+追读动力+节奏+情绪断裂；去AI化：7 Gate 命中+文风漂移+毒句式）；P0 立即改才发/P1 卷内改/P2 下次修订。
- **防死循环**：单章最多 3 轮审核；连续 3 章"有条件通过"→强制人工介入（问题在纲/设定层）；同一批不原地重审，要第二意见就换路由。
- **评审团队**（writers-room）：评审与写作平台分离；6 人设并行+权重化 rubric；结论必须可溯源到人设+维度+原文摘录。
- **修订流程**（revision.md）：冻结→改纲→圈定受影响章→逐章修订→追踪回写；托管模式遇 P0 熔断停止，不继续写下一章。

### 5.6 质量度量与回归

- **质量基线**（long-novel-skill v6.1）：五维评测（AI味分数/平均句长/对话占比/节奏均衡度/门禁通过率），每 10 章对比基线检测退化趋势。
- **跨文件一致性守卫**：角色名一致性/时间线倒退/伏笔回收状态/追踪同步/字数连续性五项机器检查（static_check.py）。
- **七维质量评分**（AI腔/节奏/文风/情感/结构/对话/可读性）+ 趋势分析；质量评分脚本化、基线落盘，供后续章节对比。
- **成本与质量护栏**（make-ur-Agent-writer）：预算上限（budget-cny）、replan-every K 章、断点续跑零重复花费、审计账本记录每次调用。

---

## 6. 候选项目清单（10+）

| # | 项目 | 更新 | 一句话 |
|---|---|---|---|
| 1 | https://github.com/hardikpandya/stop-slop | 活跃（2026 引用） | 英文 AI slop 规则与评分框架，shuorenhua 官方推荐的英文对应物 |
| 2 | https://github.com/blader/humanizer | 活跃（2026 引用） | 英文 AI 模式分类 25 模式（源自 Wikipedia Signs of AI Writing） |
| 3 | https://github.com/petergyang/no-ai-slop | 2026 | Detect 模式+声音保留框架+7 模式，已并入 no-ai-slop-humanizer |
| 4 | https://github.com/conorbronsdon/avoid-ai-writing | 活跃 | AI 写作问题分类与严重度参考 |
| 5 | https://github.com/Raymondhou0917/speak-human-tw | 2026 | 繁体中文去 AI 味，覆盖电子报/社群贴文/销售页/客服信 |
| 6 | https://github.com/WenyuChiou/academic-writing-skills | 2026-08-10 | 学术写作 skill 集（12⭐，中文维护） |
| 7 | https://github.com/WILLOSCAR/research-units-pipeline-skills | 2026-08-10 | 研究写作流水线 skills（497⭐） |
| 8 | https://github.com/mchlpdmnt/genz-writer-skill | 2026-08-08 | Z 世代语气写作 skill |
| 9 | https://github.com/jeelbhalani02/claud-bookwriting-author-skill | 2026-05-25 | Claude 整本书写作作者 skill |
| 10 | https://github.com/cjdavis62/claude-creative-writing | 2026-05-30 | Claude 创意写作 skill |
| 11 | https://github.com/Cam3L1/ghost-skill | 2026-06-25 | 去"AI 味"写作 skill |
| 12 | https://github.com/pavelkudrna83/creative-writing-skill | 2026-06-19 | 创意写作 skill（带风格工具） |
| 13 | https://github.com/Zejun-W/AI-Research-Writing-Skills-Hub | 2026-08-10 | AI 研究写作 skill 集散地 |
| 14 | https://github.com/SamsonCyber/writing-deslop | 2026-08-10 | 写作去 slop 工具 |
| 15 | https://github.com/eshaanjain26/no-ai-slop-humanizer | 2026-08-09 | 见深度分析 2.8（humanizer 合并版） |
| 16 | https://github.com/dilidin2/tic | 2026-07-27 | 通用写作提示工程合集 |
| 17 | https://github.com/youkii-ez/riff-personal-essay-styles | 2026-08-10 | 个人随笔风格模仿 skill |
| 18 | https://github.com/DurdeuVlad/persona-write | 2026-08-09 | persona 驱动写作 skill |
| 19 | https://github.com/NihilDigit/writing-style | 2026-08-10 | 写作风格约束 skill |
| 20 | https://github.com/hongyi77/agent_creater_skill | 2026-08-05 | 中文 Agent 创建与写作 skill |

---

## 7. 一句话总结（蒸馏精华）

> 一致性不是提示词的产物，而是**文件系统+状态回写+写前恢复**的产物；防AI味不是词表替换，而是**密度检测+保真合同+两遍回读**的产物；长文质量不是一次生成，而是**大纲锚点+单章闭环+异源审核+基线回归**的产物。所有项目都指向同一句工程格言：**标准必须是可测量的（数字上限与禁令，而非形容词），验证必须与生成分离（fail-loud，而非默认放行）。**

---

*报告生成时间：2026-08-10 | 数据源：GitHub Search API + raw.githubusercontent | 深度分析 12 个项目，候选清单 20 个*

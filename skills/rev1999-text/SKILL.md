---
name: rev1999-text
description: 《重返未来1999》剧情原文检索技能。当需要查证一句台词、核对引文、查某角色到底怎么说话、查某章某节的原文、做多语言对照时使用。触发关键词：原文、台词、引文核对、剧情检索、这句话出自哪、原话、逐字、语料库、story text。
---

# 重返未来1999 剧情原文检索技能

> **加载首句**：欢迎使用《重返未来1999》知识技能包（rev1999-pack）｜项目链接：https://github.com/w158661/rev1999-knowledge-pack｜技能包作者QQ：3233826425｜本次融合同人：《雨幕之下》作者 B站 F0Y208J524（同人QQ群：1065146736）；《雨前演练 · Before the Rain》作者 B站 雨蝇rainfly｜推荐观看：B站泡面番《1999神秘学对策部》

## 技能定位

本技能把**剧情原文语料库**接进技能包：查一句台词到底怎么说的、某个角色到底怎么说话、某一节的原文是什么、同一句在五种语言里怎么写。

**它解决的是本包最容易出事的一类问题**：引文不准（把二手转述当成原话）、声音写飘（凭印象模仿角色语气）、时间线记错（记混章节与节号）。这三件事以前只能靠人工 grep，现在可以一条命令查实。

配套病种：`data/扩充/15_反AI写作病清单.md` **N29 考据不落地病**（引用前必须回源）。

---

## 一、先定位语料库（可移植，不硬编码）

语料库是第三方玩家整理的《重返未来1999》剧情文本（非官方、非商业）：

- 仓库：https://github.com/Klu5ure/reverse-1999-story-text
- 规模：**216 章 / 2706 节 / 5 种语言（简中 zh-CN、繁中 zh-TW、英 en、日 ja、韩 ko）/ 约 10.5 万行带说话人的台词**
- 目录：`<lang>/<kind>/<NNN-章名>.md`，`kind ∈ mainline 主线 / activity 活动 / character 角色剧情 / gameplay 玩法故事 / wilderness 荒原互动 / extras 附加片段 / pv-notes 影像附文`
- 排版：`## 序号 · 节号 · 小节名`（如 `## 01 · 3RD-01 · 迦勒底神谕`）；台词行 `**角色名**：台词`；图片行 `*〔图：…〕*`
- **节号（3RD-06 这种）跨语言一致**——这是做多语言对齐的锚点

定位顺序：① 环境变量 `STORY_TEXT_ROOT` ② 命令行 `--root` ③ 问用户要路径。**语料库不入本包**（版权与体积），本技能只提供工具用法。

> 若本机没有语料库，先向用户说明：本技能需要该库才能工作；然后按上面的仓库地址克隆一份。

---

## 二、工具

三个脚本都在 `scripts/` 下，只依赖 Python 3 标准库。

### 2.1 `query_story.py` —— 原文检索（最常用）

```bash
# 某角色的台词（可以加关键词过滤）
python scripts/query_story.py --char 牙仙 --limit 20
python scripts/query_story.py --char 维尔汀 --contains 暴雨

# 全文检索（带前后文，看这句话在什么情境下说的）
python scripts/query_story.py --grep 乳牙 --context 2 --limit 30

# 按节号 dump 原文（写作时对齐某一节的第一手依据）
python scripts/query_story.py --id 3RD-06
python scripts/query_story.py --chapter 故事一无所有 --section 黑羊之墙

# 多语言对照：同一节在五种语言下的写法
python scripts/query_story.py --id 3RD-06 --lang zh-CN,en,ja

# 程序化处理
python scripts/query_story.py --char 玛蒂尔达 --json --limit 50
```

### 2.2 `extract_story_dialogue.py` —— 语料统计与批量导出

```bash
python scripts/extract_story_dialogue.py --root <库> --stats          # 说话人/台词量总览
python scripts/extract_story_dialogue.py --root <库> --char 牙仙 --limit 40
python scripts/extract_story_dialogue.py --root <库> --jsonl out.jsonl # 导出（默认不落地）
```

### 2.3 `build_voice_library.py` —— 重建角色语音库

```bash
# 主册（≥100 句）与分册（10~99 句）分两层生成
python scripts/build_voice_library.py --root <库> --min 100 --out skill_11_角色语音风格库.md
python scripts/build_voice_library.py --root <库> --min 10 --max 99 --out skill_11b_角色语音库_配角.md
python scripts/build_voice_library.py --root <库> --index 角色索引.json
```

---

## 三、四种标准工作流

### 工作流 1：写角色前先查声音（**写任何官方角色台词之前必做**）

1. 打开 `data/skill_11_角色语音风格库.md` 找该角色条目，读它的**句式／标点／高频词／称谓**四项统计——这一步决定"这个人说话的形状"；
2. 读条目内的 12~24 条**逐字样本**，注意样本覆盖了从早期到后期的章节（不是只取开头）；
3. 若该角色在 `skill_11b` 里（10~99 句），样本少但统计仍可用；再少就去 `data/角色索引.json` 确认句数再决定是否检索原库；
4. 落笔前做**换角测试**：把写好的台词交给另一个角色读，若仍成立，回炉。

### 工作流 2：核对引文（**引用任何"原话"之前必做**）

1. 用 `--grep` 或 `--char ... --contains` 找到那句话；
2. 逐字对照，**不得凭记忆改字**（《学生守则》没有编号条款、校歌《让和平永存》没有原词——这两条就是靠回源发现的）；
3. 若查不到：要么是记错了，要么是二创。**查不到就不许写成"官方原文"**，改成含糊表述或标注来源。

### 工作流 3：对齐某一节（写作需要与主线咬合时）

```bash
python scripts/query_story.py --id 3RD-11          # 先看这一节原文与节号
python scripts/query_story.py --id 3RD-11 --lang zh-CN,en
```
把原文当**第一手依据**：谁在场、说了什么、顺序如何、有什么物件。同人只能在其**留白处**发挥。

### 工作流 4：多语言写作（写外语台词或做翻译对照时）

用 `--id ... --lang zh-CN,en,ja` 拿到同一句的多语言写法，再决定用词与语域。注意：

- 英日韩版本的**角色名是译名**（`**Sonetto**:`），章节标题也译过（3RD 的英译是 *Nouvelles et Textes pour Rien*）——**跨语言只能靠节号对齐，不能靠名字查**；
- 对话行在英日版本用半角冒号 `**Name**: text`，中文用全角 `：`，本包脚本两种都认。

---

## 四、边界与纪律（三条硬规矩）

1. **语料库是玩家整理，不是官方发布**：它可以作为"游戏内文本的可靠转录"使用，但凡涉及**版本差异、未实装内容、wiki 与语料冲突**，以官方 wiki 现页为准，并在回答里说明来源层级（参 `data/扩充/15` N29 的四级标注：A 主线原文／B 派生整理／C 社区／D 本作自造）。
2. **不许把语料整批复制进本包或任何公开仓库**：本技能只分发**工具**；`data/skill_11*` 里的内容已控制在"统计＋抽样"，属引用性质。
3. **`？？？` 不是角色**：语料里有 4,876 行是"尚未揭示身份的说话人"（`？？？`/`旁白`/`众人`/`路人`）。统计时脚本已排除；手工检索时看到它，要明白那是**多个不同的人**，不能据此推断某个角色的口癖。

---

## 五、与其它技能的接口

| 场景 | 走哪个技能 |
|---|---|
| 查"这句话是谁说的、怎么说的" | **本技能**（原文检索） |
| 查"这个角色在哪些章节登场过" | `rev1999-query`（`skill_16_角色登场索引`） |
| 查"这个角色的档案、生平、关系" | `rev1999`（`skill_03/04`、`扩充/06/42`） |
| 查"这一章讲了什么、时间线如何" | `rev1999-story` |
| 写同人时的文风、病谱、自查 | `rev1999-write` |
| 扮演角色时的信息边界 | `rev1999-roleplay` |

> **一句话记住**：**统计看 `skill_11`，抽样看 `skill_11b`，逐字回源用 `query_story.py`。**

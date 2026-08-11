#!/usr/bin/env python3
# 重返未来1999 搜索索引系统
# 构建倒排索引，支持精确搜索、模糊搜索、关联搜索

import os
import sys
import json
import pickle
import re
import hashlib
from collections import defaultdict
from pathlib import Path

# ============================================================
# Windows 控制台编码修复（强制 UTF-8 输出，避免 GBK 乱码/崩溃）
# ============================================================

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, Exception):
    pass


def _default_data_dir():
    """解析默认数据目录

    优先级:
      1. 环境变量 REV1999_DATA
      2. 脚本目录的 ../../data/ (规范约定)
      3. 脚本目录的 ../../../data/ (实际仓库布局)
    """
    env_data = os.environ.get("REV1999_DATA")
    if env_data:
        return env_data

    script_dir = Path(__file__).resolve().parent

    # 规范约定: ../../data/
    candidate = (script_dir / ".." / ".." / "data").resolve()
    if os.path.isdir(candidate):
        return str(candidate)

    # 实际仓库布局: ../../../data/ (scripts -> rev1999 -> skills -> rev1999-pack -> data)
    candidate = (script_dir / ".." / ".." / ".." / "data").resolve()
    if os.path.isdir(candidate):
        return str(candidate)

    # 兜底返回规范约定路径（即使不存在，由调用方报错）
    return str((script_dir / ".." / ".." / "data").resolve())


# ============================================================
# 中文分词模块
# ============================================================

_HAS_JIEBA = False
try:
    import jieba
    _HAS_JIEBA = True
except ImportError:
    pass

# 重返未来1999 专有名词词典（无论是否使用jieba都用于关键词匹配）
SPECIAL_TERMS = {
    "维尔汀", "十四行诗", "司辰", "暴雨", "神秘学家", "神秘术",
    "圣洛夫基金会", "重塑之手", "康斯坦丁", "Z女士", "勿忘我",
    "APPLe", "星锑", "红弩箭", "远旅", "夏利", "玛蒂尔达",
    "兔毛手袋", "苏芙比", "帕米埃", "坦南特", "玛丽莲", "柏林以东",
    "未锈铠", "皮克勒斯", "挖掘艺术", "新巴别塔", "玛格丽特",
    "槲寄生", "泥鯭的士", "五色月", "拉拉泉", "莉拉妮", "尼克·波顿",
    "婴儿蓝", "讣告人", "恐怖通", "弄臣", "吵闹鬼", "小丑",
    "爱兹拉", "37", "6", "210", "菲林士多", "喀嚓卡嚓",
    "伊索尔德", "卡卡尼亚", "葛天", "曲娘", "北方哨歌",
    "金铃子", "露西", "卡戎", "塞梅尔维斯", "纸信圈儿",
    "阿莱夫", "芭卡洛儿", "笃笃骨", "虚构集", "娜娜", "阿嚏",
    "洛佩拉", "狂想", "笃笃骨", "阿尔古斯", "冷周六",
    "莎丝比亚", "可莉丝", "洁西卡", "坎吉拉", "帕德拉",
    "海关", "手稿", "行至摩卢旁卡", "孤独之歌", "复乐园",
    "夜色温柔", "星", "此即明日", "远东", "绿湖噩梦",
    "UTTU", "闪魂", "鬃毛邮报", "人工梦游", "雨中悬想",
    "局外演绎", "沙盘解构", "恢奇牌儿", "律的调校",
    "荒原", "心相", "征集", "衣着", "物品", "第三扇门",
    "来亚什基", "乌卢鲁", "唐人街", "伊戈尔", "回声谣",
    "奠基石", "小瑞安侬", "拉莫纳", "无名者", "洛伦兹蝴蝶",
    "玛尔纱", "程和光", "鹭鸶剪", "复乐园", "漫漫长路",
    "远航", "他者的悲哀", "老虎的金黄", "洞穴的囚徒",
    "今夜星光灿烂", "忧郁的热带", "疯癫与文明", "行于漫漫长路上",
    "雷米特", "金杯", "大英",
    "手艺", "先驱", "教育", "科普", "和平",
    "基督教", "犹太", "苏联", "俄语", "西里尔",
    "白金", "金", "红", "蓝", "黄", "绿", "紫", "橙",
    "司辰", "显影", "采访", "箱中", "看门狗",
    "树", "河流", "森林", "石头", "风暴", "木材",
    "手", "手影", "帷幕", "井", "地形", "旋律",
    "回声", "鸟", "振翅", "反刍", "巢", "箭",
    "子弹", "花", "庭院", "写信", "火灾", "瘟疫",
    "泥", "柠檬", "苦涩", "云", "山", "扶桑", "彼岸",
    "宝箱", "魔精", "银", "卫兵", "钱", "代币",
    "佩枪", "梦", "筑城", "沉眠", "仪式", "咒语", "升阶",
    "拉普拉斯", "科算", "海特街", "37号",
    "霍夫曼", "露西", "卡森", "玛蒂尔达", "梅兰妮",
    "和平乌鲁", "鸭鸭", "新巴别塔", "野蛮反射",
    "马库斯", "罗蕾莱", "小梅斯梅尔", "阿夫西维",
    "丽莎", "路易斯", "塞西莉亚", "雾行者", "阿尔丹",
    "和平", "UTTU", "闪魂", "卡", "小径",
    "沙粒", "维拉", "黎明", "积雪", "天下有风",
    "焰光交汇", "曲香蒙求", "银线结", "夜间游戏",
    "关卡", "返还", "礼盒", "书", "报", "壶",
    "专用", "思想", "刚", "海", "田", "星",
    "公鸡", "船", "银", "杆", "灯", "轮", "塔",
    "尺", "福利", "放", "方向", "箱", "信", "书",
    "幕间", "自由", "平等", "博爱", "事件",
    "金", "啪", "咔", "掌", "观", "颂", "讲",
    "天才", "孩童", "读", "十五", "二十", "八十",
    "37", "6", "210", "9", "15", "20", "80",
    "军靴", "冰淇淋", "十字", "光环", "属", "猜想",
    "说", "游玩", "版本", "环", "志", "故",
    "对话", "图腾", "语言", "边", "木", "方",
    "第一章", "第二章", "第三章", "第四章", "第五章",
    "第六章", "第七章", "第八章", "序章", "编剧",
}

# 文件类型到目录名的映射
TYPE_DIR_MAP = {
    "character": {"角色", "角色列表"},
    "story": {"主线", "支线", "小径"},
    "world": {"世界观设定"},
    "system": {"征集", "心相", "鬃毛邮报", "律的调校", "荒原", "物品", "衣着", "雨中悬想", "第三扇门", "人工梦游", "恢奇牌儿", "沙盘解构", "收藏品", "局外演绎"},
    "event": {"活动", "轩事"},
}

# skill_ 文件前缀到类型的映射
SKILL_TYPE_MAP = {
    "skill_00": "general",           # 主索引
    "skill_01": "world",             # 世界观核心
    "skill_02": "story",             # 时间线与主线
    "skill_03": "character",         # 角色百科A
    "skill_04": "character",         # 角色百科B
    "skill_05": "event",             # 支线活动
    "skill_06": "system",            # 游戏系统
    "skill_07": "general",           # 文学风格与创作指南
    "skill_08": "world",             # 术语词典
    "skill_09": "general",           # 仿写与OC模板
    "skill_10": "world",             # 世界观深度解读
}

# 分析文件的类型映射
ANALYSIS_TYPE_MAP = {
    "analysis_世界观核心": "world",
    "analysis_主线剧情": "story",
    "analysis_小径世界观": "world",
    "analysis_支线写作深度": "general",
    "analysis_支线剧情": "story",
    "analysis_深层世界观": "world",
    "analysis_系统机制": "system",
    "analysis_角色数据": "character",
    "analysis_角色文学": "character",
    "analysis_轩事活动": "event",
}


# ============================================================
# 分词工具
# ============================================================

def get_tokenizer():
    """返回分词函数，根据环境自动选择"""
    if _HAS_JIEBA:
        # 加载专有名词到jieba词典
        for term in SPECIAL_TERMS:
            jieba.add_word(term, freq=100, tag="nz")
        return _jieba_tokenize
    else:
        return _simple_tokenize


def _jieba_tokenize(text):
    """使用jieba分词"""
    words = jieba.lcut(text)
    return [w.strip() for w in words if w.strip() and len(w.strip()) >= 1]


def _simple_tokenize(text):
    """无jieba时的降级方案：字符二元组 + 专有名词匹配（含中文停用字过滤）"""
    tokens = set()
    # 1. 匹配专有名词
    for term in SPECIAL_TERMS:
        if term in text:
            tokens.add(term)
    # 2. 中文部分：按标点/空格切分后，对每个词取一元组、二元组
    segments = re.split(r'[\s，。！？、；：""''（）【】《》\n\r\t,.!?;:\-()\[\]{}<>/]+', text)
    for seg in segments:
        if not seg:
            continue
        # 纯英文或数字直接保留
        if re.match(r'^[a-zA-Z0-9]+$', seg):
            if len(seg) >= 1:
                tokens.add(seg.lower())
        else:
            # 中文：按字符拆分一元和二元（过滤停用字）
            chars = list(seg)
            for c in chars:
                if c.strip() and c not in _STOP_CHARS:
                    tokens.add(c)
            for i in range(len(chars) - 1):
                bigram = chars[i] + chars[i + 1]
                if bigram.strip() and not (chars[i] in _STOP_CHARS and chars[i + 1] in _STOP_CHARS):
                    tokens.add(bigram)
    return list(tokens)


# 中文停用字（单字高频虚词，降低索引噪声）
_STOP_CHARS = set('的了在是和我与也都而或及于之其且以为等中上下里个有无不就又被把让从对到说吗呢啊吧这那')


# ============================================================
# 文件类型检测
# ============================================================

def detect_file_type(file_path, base_dir):
    """根据文件路径检测文件类型"""
    rel_path = os.path.relpath(file_path, base_dir)
    parts = rel_path.replace("\\", "/").split("/")

    # 检查子目录名
    for part in parts[:-1]:
        for ftype, dirs in TYPE_DIR_MAP.items():
            if part in dirs:
                return ftype

    # 检查文件名
    basename = os.path.basename(file_path)
    name_no_ext = os.path.splitext(basename)[0]

    # skill_ 文件
    for prefix, ftype in SKILL_TYPE_MAP.items():
        if name_no_ext.startswith(prefix):
            return ftype

    # analysis_ 文件
    for prefix, ftype in ANALYSIS_TYPE_MAP.items():
        if name_no_ext.startswith(prefix):
            return ftype

    return "general"


# ============================================================
# 倒排索引类
# ============================================================

class SearchIndex:
    """倒排索引搜索引擎"""

    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = _default_data_dir()

        self.data_dir = data_dir
        self.index_dir = os.path.join(data_dir, ".index")
        self.index_file = os.path.join(self.index_dir, "inverted_index.pkl")
        self.meta_file = os.path.join(self.index_dir, "meta.json")

        # 索引数据结构
        self.inverted_index = {}   # term -> [(file, line, context_before, line_text, context_after, file_type), ...]
        self.file_terms = {}       # file -> set of terms (用于TF计算)
        self.file_line_count = {}  # file -> total line count
        self.file_type_map = {}    # file -> file_type
        self.total_files = 0
        self.total_lines = 0

        self.tokenize = get_tokenizer()

    def _get_context(self, lines, idx, context_lines=2):
        """获取匹配行及上下文"""
        start = max(0, idx - context_lines)
        end = min(len(lines), idx + context_lines + 1)
        context_before = [l.rstrip("\n") for l in lines[start:idx]]
        line_text = lines[idx].rstrip("\n") if idx < len(lines) else ""
        context_after = [l.rstrip("\n") for l in lines[idx + 1:end]]
        return context_before, line_text, context_after

    def _scan_files(self):
        """扫描所有数据文件"""
        files = []
        if not os.path.isdir(self.data_dir):
            print(f"错误: 数据目录不存在 ({self.data_dir})", file=sys.stderr)
            return files

        for root, dirs, fnames in os.walk(self.data_dir):
            # 跳过索引目录
            if ".index" in dirs:
                dirs.remove(".index")
            for fname in fnames:
                if fname.endswith((".md", ".txt")):
                    fpath = os.path.join(root, fname)
                    files.append(fpath)

        files.sort()
        return files

    def build_index(self, data_dir=None):
        """构建完整的倒排索引"""
        if data_dir:
            self.data_dir = data_dir
            self.index_dir = os.path.join(data_dir, ".index")
            self.index_file = os.path.join(self.index_dir, "inverted_index.pkl")
            self.meta_file = os.path.join(self.index_dir, "meta.json")

        os.makedirs(self.index_dir, exist_ok=True)

        files = self._scan_files()
        if not files:
            print("未找到数据文件", file=sys.stderr)
            return False

        self.inverted_index = defaultdict(list)
        self.file_terms = defaultdict(set)
        self.file_line_count = {}
        self.file_type_map = {}

        tokenizer = self.tokenize
        total = len(files)

        for fi, fpath in enumerate(files):
            ftype = detect_file_type(fpath, self.data_dir)
            self.file_type_map[fpath] = ftype

            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                print(f"  跳过 {fpath}: {e}", file=sys.stderr)
                continue

            lines = content.split("\n")
            self.file_line_count[fpath] = len(lines)

            for li, line in enumerate(lines):
                line_stripped = line.strip()
                if not line_stripped:
                    continue

                terms = tokenizer(line_stripped)
                seen = set()
                context_before, line_text, context_after = self._get_context(lines, li)

                for term in terms:
                    if term in seen:
                        continue
                    seen.add(term)
                    self.file_terms[fpath].add(term)
                    entry = (fpath, li, context_before, line_text, context_after, ftype)
                    self.inverted_index[term].append(entry)

            if (fi + 1) % 100 == 0 or (fi + 1) == total:
                print(f"  索引进度: {fi + 1}/{total} 文件", file=sys.stderr)

        self.total_files = len(files)
        self.total_lines = sum(self.file_line_count.values())

        # 保存索引
        self._save_index()

        print(f"索引构建完成: {self.total_files} 文件, {self.total_lines} 行, {len(self.inverted_index)} 词条", file=sys.stderr)
        return True

    def _save_index(self):
        """保存索引到磁盘"""
        # 保存倒排索引 (pickle)
        with open(self.index_file, "wb") as f:
            pickle.dump({
                "inverted_index": dict(self.inverted_index),
                "file_terms": dict(self.file_terms),
                "file_line_count": self.file_line_count,
                "file_type_map": self.file_type_map,
            }, f, protocol=pickle.HIGHEST_PROTOCOL)

        # 保存元信息 (json)
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump({
                "total_files": self.total_files,
                "total_lines": self.total_lines,
                "total_terms": len(self.inverted_index),
                "has_jieba": _HAS_JIEBA,
                "data_dir": self.data_dir,
            }, f, ensure_ascii=False, indent=2)

    def _load_index(self):
        """从磁盘加载索引"""
        if not os.path.exists(self.index_file):
            return False

        try:
            with open(self.index_file, "rb") as f:
                data = pickle.load(f)
            self.inverted_index = data["inverted_index"]
            self.file_terms = data["file_terms"]
            self.file_line_count = data["file_line_count"]
            self.file_type_map = data["file_type_map"]
            self.total_files = len(self.file_terms)
            self.total_lines = sum(self.file_line_count.values())
            return True
        except Exception as e:
            print(f"加载索引失败: {e}", file=sys.stderr)
            return False

    def _compute_tfidf(self, term, file_path):
        """计算 term 在文件中的 TF-IDF 权重"""
        # TF: 当前文件中该词的出现次数
        entries = [e for e in self.inverted_index.get(term, []) if e[0] == file_path]
        tf = len(entries)
        if tf == 0:
            return 0.0

        # 归一化TF
        total_lines = self.file_line_count.get(file_path, 1)
        tf_norm = tf / max(total_lines, 1)

        # IDF: log(总文件数 / 包含该词的文件数)
        df = len(set(e[0] for e in self.inverted_index.get(term, [])))
        n = max(self.total_files, 1)
        idf = 1.0
        if df > 0:
            idf = max(0.1, (n / df) ** 0.5)

        return tf_norm * idf

    def search(self, query, filter_type="all", top_k=20):
        """执行搜索"""
        if not self.inverted_index:
            if not self._load_index():
                print("索引未构建，请先运行 build 命令", file=sys.stderr)
                return []

        query = query.strip()
        if not query:
            return []

        # 对查询分词
        query_terms = self.tokenize(query)
        if not query_terms:
            # 降级：直接按字符搜索
            query_terms = [c for c in query if c.strip()]

        if not query_terms:
            return []

        # 收集所有匹配的条目
        results = {}
        seen_entries = set()

        for term in query_terms:
            if term not in self.inverted_index:
                # 尝试拼音/近似匹配
                fuzzy_matches = self._fuzzy_match(term)
                for fterm in fuzzy_matches:
                    self._collect_entries(fterm, filter_type, results, seen_entries, query_terms)
                continue
            self._collect_entries(term, filter_type, results, seen_entries, query_terms)

        # 计算相关性得分并排序
        scored = []
        for entry_id, entry in results.items():
            fpath, line_num, ctx_before, line_text, ctx_after, ftype = entry
            score = 0.0

            # 1. 查询词在匹配行中的出现次数
            for qt in query_terms:
                count = line_text.lower().count(qt.lower())
                if count > 0:
                    score += count * 2.0
                    # 精确匹配加权
                    if qt in line_text:
                        score += 5.0

            # 2. 查询词在上下文中的出现
            context_text = " ".join(ctx_before + ctx_after)
            for qt in query_terms:
                if context_text.lower().count(qt.lower()) > 0:
                    score += 1.0

            # 3. TF-IDF 加权
            for qt in query_terms:
                if qt in self.inverted_index:
                    score += self._compute_tfidf(qt, fpath) * 3.0

            # 4. 完整查询词匹配加分
            if query in line_text:
                score += 10.0

            # 5. 行号小的优先级高（靠近文件开头）
            score += max(0, 1.0 - line_num / max(self.file_line_count.get(fpath, 1), 1))

            scored.append((score, entry))

        scored.sort(key=lambda x: (-x[0], x[1][1]))

        # 去重并取 top_k
        final = []
        seen_files_lines = set()
        for score, entry in scored:
            file_line_key = (entry[0], entry[1])
            if file_line_key in seen_files_lines:
                continue
            seen_files_lines.add(file_line_key)
            final.append((score, entry))
            if len(final) >= top_k:
                break

        return final

    def _collect_entries(self, term, filter_type, results, seen_entries, query_terms):
        """收集指定term的匹配条目"""
        for entry in self.inverted_index.get(term, []):
            fpath, line_num, ctx_before, line_text, ctx_after, ftype = entry

            if filter_type != "all" and ftype != filter_type:
                continue

            # 生成唯一ID
            entry_id = (fpath, line_num)
            if entry_id in seen_entries:
                continue
            seen_entries.add(entry_id)

            results[entry_id] = entry

    def _fuzzy_match(self, term):
        """模糊匹配：查找包含该term的索引词条"""
        if not term or len(term) < 1:
            return []

        matches = set()

        # 1. 子串匹配：索引词条包含查询词
        for idx_term in self.inverted_index:
            if len(idx_term) >= 2 and term in idx_term:
                matches.add(idx_term)
            elif len(term) >= 2 and idx_term in term:
                matches.add(idx_term)

        # 2. 拼音首字母匹配（如果term是英文）
        if re.match(r'^[a-zA-Z]+$', term):
            term_lower = term.lower()
            for idx_term in self.inverted_index:
                # 获取中文词的首字母拼音（简化版）
                pinyin_initials = "".join(
                    _get_pinyin_initials(c) for c in idx_term if "一" <= c <= "鿿"
                )
                if pinyin_initials and pinyin_initials.startswith(term_lower):
                    matches.add(idx_term)

        # 3. 单字符匹配：如果term只有一个char，找包含它的所有双语词
        if len(term) == 1 and "一" <= term <= "鿿":
            for idx_term in self.inverted_index:
                if len(idx_term) >= 2 and term in idx_term:
                    matches.add(idx_term)

        return list(matches)[:20]

    def search_related(self, query, top_k=15):
        """关联搜索：跨文件类型返回相关段落"""
        # 先做一次全类型搜索，取更多结果
        all_results = self.search(query, filter_type="all", top_k=top_k * 5)

        # 按文件类型分组
        grouped = defaultdict(list)
        file_types_used = set()

        for score, entry in all_results:
            fpath = entry[0]
            ftype = entry[5]
            if ftype not in file_types_used or len(grouped[ftype]) < 5:
                grouped[ftype].append((score, entry))
                file_types_used.add(ftype)

        # 按类型展平，每种类型至少取1条，最多5条
        result = []
        type_counts = defaultdict(int)
        type_order = ["character", "story", "world", "system", "event", "general"]

        for ftype in type_order:
            if ftype in grouped:
                entries = sorted(grouped[ftype], key=lambda x: -x[0])
                for score, entry in entries:
                    if type_counts[ftype] < 5 and len(result) < top_k:
                        result.append((score, entry))
                        type_counts[ftype] += 1

        # 如果还不够，补上剩余的
        if len(result) < top_k:
            remaining = [(s, e) for s, e in all_results if (s, e) not in result]
            result.extend(remaining[:top_k - len(result)])

        return result

    def update_index(self, file_path):
        """增量更新单个文件的索引"""
        if not self.inverted_index:
            if not self._load_index():
                print("索引未构建，请先运行 build 命令", file=sys.stderr)
                return False

        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}", file=sys.stderr)
            return False

        # 删除该文件的所有旧索引条目
        for term in list(self.inverted_index.keys()):
            self.inverted_index[term] = [
                e for e in self.inverted_index[term] if e[0] != file_path
            ]
            if not self.inverted_index[term]:
                del self.inverted_index[term]

        # 重新索引该文件
        ftype = detect_file_type(file_path, self.data_dir)
        self.file_type_map[file_path] = ftype

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            print(f"读取失败 {file_path}: {e}", file=sys.stderr)
            return False

        lines = content.split("\n")
        self.file_line_count[file_path] = len(lines)
        self.file_terms[file_path] = set()

        for li, line in enumerate(lines):
            line_stripped = line.strip()
            if not line_stripped:
                continue

            terms = self.tokenize(line_stripped)
            seen = set()
            context_before, line_text, context_after = self._get_context(lines, li)

            for term in terms:
                if term in seen:
                    continue
                seen.add(term)
                self.file_terms[file_path].add(term)
                entry = (file_path, li, context_before, line_text, context_after, ftype)
                if term not in self.inverted_index:
                    self.inverted_index[term] = []
                self.inverted_index[term].append(entry)

        self._save_index()
        print(f"已更新索引: {file_path}", file=sys.stderr)
        return True

    def stats(self):
        """显示索引统计信息"""
        if not self.inverted_index:
            if not self._load_index():
                print("索引未构建", file=sys.stderr)
                return

        # 按类型统计
        type_counts = defaultdict(int)
        type_files = defaultdict(set)
        for fpath, ftype in self.file_type_map.items():
            type_counts[ftype] += self.file_line_count.get(fpath, 0)
            type_files[ftype].add(fpath)

        print(f"数据目录: {self.data_dir}")
        print(f"索引目录: {self.index_dir}")
        print(f"分词引擎: {'jieba (精确分词)' if _HAS_JIEBA else '简单分词 (专有名词+二元组)'}")
        print(f"总文件数: {self.total_files}")
        print(f"总行数:   {self.total_lines}")
        print(f"词条数:   {len(self.inverted_index)}")
        print()
        print("文件类型分布:")
        for ftype in ["character", "story", "world", "system", "event", "general"]:
            if ftype in type_files:
                print(f"  {ftype:12s}: {len(type_files[ftype]):4d} 文件, {type_counts.get(ftype, 0):6d} 行")


# ============================================================
# 拼音首字母工具（简化版）
# ============================================================

_PINYIN_INITIALS = {
    "b": "玻", "p": "泼", "m": "摸", "f": "佛",
    "d": "得", "t": "特", "n": "讷", "l": "勒",
    "g": "哥", "k": "科", "h": "喝",
    "j": "基", "q": "欺", "x": "希",
    "zh": "知", "ch": "吃", "sh": "诗", "r": "日",
    "z": "资", "c": "雌", "s": "思",
    "y": "一", "w": "乌",
}

# 常用中文字符到拼音首字母的映射（简化版，覆盖大部分常用字）
_PINYIN_MAP = {}


def _build_pinyin_map():
    """构建中文字符到拼音首字母的映射（简化的静态映射）"""
    if _PINYIN_MAP:
        return
    # 一级汉字表（按拼音首字母分组）
    initials_map = {
        "a": "阿啊埃挨哎唉哀皑癌蔼矮艾碍爱隘鞍氨安俺按暗岸胺案肮昂盎凹敖熬翱袄傲奥懊澳",
        "b": "八巴扒拔跋靶把坝霸罢爸白柏百摆佰败拜稗斑班搬扳般颁板版扮拌伴瓣半办绊邦帮绑榜膀绑棒磅蚌镑傍谤苞胞包褒剥薄雹保堡饱宝抱报暴豹鲍爆杯碑悲卑北辈背贝钡倍狈备惫焙被奔苯本笨崩绷甭泵蹦迸逼鼻比鄙笔彼碧蓖蔽毕毙毖币庇痹闭敝弊必辟壁臂避陛鞭边编贬扁便变卞辨辩辫遍标彪膘表鳖憋别瘪彬斌濒滨宾摈兵冰柄丙秉饼炳病并玻菠播拨钵波博勃搏铂箔伯帛舶脖膊渤泊驳捕卜哺补埠不布步簿部怖",
        "c": "擦猜裁材才财睬踩采彩菜蔡餐参蚕残惭惨灿苍舱仓沧藏操糙槽曹草厕策侧册测层蹭插叉茬茶查碴搽察岔差诧拆柴豺搀掺蝉馋谗缠铲产阐颤昌猖场尝常长偿肠厂敞畅唱倡超抄钞朝嘲潮巢吵炒车扯撤掣彻澈郴臣辰尘晨忱沉陈趁衬撑称城橙成呈乘程惩澄诚承逞骋秤吃痴持匙池迟弛驰耻齿侈尺赤翅斥炽充冲虫崇宠抽酬畴踌稠愁筹仇绸瞅丑臭初出橱厨躇锄雏滁除楚础储矗搐触处揣川穿椽传船喘串疮窗幢床闯创吹炊捶锤垂春椿醇唇淳纯蠢戳绰疵茨磁雌辞慈瓷词此刺赐次聪葱囱匆从丛凑粗醋簇促蹿篡窜摧崔催脆瘁粹淬翠村存寸磋撮搓措挫错",
        "d": "搭达答瘩打大呆歹傣戴带殆代贷袋待逮怠耽担丹单郸掸胆旦氮但惮淡诞弹蛋当挡党荡档刀捣蹈倒岛祷导到稻悼道盗德得的蹬灯登等瞪凳邓堤低滴迪敌笛狄涤翟嫡抵底地蒂第帝弟递缔颠掂滇碘点典靛垫电佃甸店惦奠淀殿碉叼雕凋刁掉吊钓调跌爹碟蝶迭谍叠丁盯叮钉顶鼎锭定订丢东冬董懂动栋侗恫冻洞兜抖斗陡豆逗痘都督毒犊独读堵睹赌杜镀肚度渡妒端短锻段断缎堆兑队对墩吨蹲敦顿囤钝盾遁掇哆多夺垛躲朵跺舵剁惰堕",
        "e": "蛾峨鹅俄额讹蛾恶厄扼遏鄂饿恩而儿耳尔饵洱二贰",
        "f": "发罚筏伐乏阀法珐藩帆番翻樊矾钒繁凡烦反返范贩犯饭泛坊芳方肪房防妨仿访纺放菲非啡飞肥匪诽吠肺废沸费芬酚吩氛分纷坟焚汾粉奋份忿愤粪丰封枫蜂峰锋风疯烽逢冯缝讽奉凤佛否夫敷肤孵扶拂辐幅氟符伏俘服浮涪福袱弗甫抚辅俯釜斧脯腑府腐赴副覆赋复傅付阜父腹负富讣附妇缚咐",
        "g": "噶嘎该改概钙盖溉干甘杆柑竿肝赶感秆敢赣冈刚钢缸肛纲岗港杠篙皋高膏羔糕搞镐稿告哥歌搁戈鸽胳疙割革葛格蛤阁隔铬个各给根跟耕更庚羹耿梗工攻功恭龚供躬公宫弓巩汞拱贡共钩勾沟苟狗垢构购够辜菇咕箍估沽孤姑鼓古蛊骨谷股故顾固雇刮瓜剐寡挂褂乖拐怪棺关官冠观管馆罐惯灌贯光广逛瑰规圭硅归龟闺轨鬼诡癸桂柜跪贵刽辊滚棍锅郭国果裹过",
        "h": "哈骸孩海氦亥害骇酣憨邯韩含涵寒函喊罕翰撼捍旱憾悍焊汗汉夯杭航壕嚎豪毫郝好耗号浩呵喝荷菏核禾和何合盒阂河涸赫褐鹤贺嘿黑痕很狠恨哼亨横衡恒轰哄烘虹鸿洪宏弘红喉侯猴吼厚候后呼乎忽瑚壶葫胡蝴狐糊湖弧虎唬护互沪户花哗华猾滑画划化话槐徊怀淮坏欢环桓还缓换患唤痪豢焕涣宦幻荒慌黄磺蝗簧皇凰惶煌晃幌恍谎灰挥辉徽恢蛔回毁悔慧卉惠晦贿秽会烩汇讳诲绘荤昏婚魂浑混豁活伙火获或惑霍货祸",
        "j": "击圾基机畸稽积箕肌饥迹激讥鸡姬绩缉吉极棘辑籍集及急疾汲即嫉级挤几脊己蓟技冀季伎祭剂悸济寄寂计记既忌际妓继纪嘉枷夹佳家加荚颊贾甲钾假稼价架驾嫁歼监坚尖笺间煎兼肩艰奸缄茧检柬碱硷拣捡简俭剪减荐槛鉴践贱见键箭件健舰剑饯渐溅涧建僵姜将浆江疆蒋桨奖讲匠酱降蕉椒礁焦胶交郊浇骄娇嚼搅铰矫侥脚饺缴绞剿教酵轿较叫窖揭接皆秸街阶截劫节桔杰捷睫竭洁结解姐戒藉芥界借介疥诫届巾筋斤金今津襟紧锦仅谨进靳晋禁近烬浸尽劲荆兢茎睛晶鲸京惊精粳经井警景颈静境敬镜径痉靖竟竞净炯揪纠究玖韭久灸九酒厩救旧臼舅咎就疚鞠拘狙疽居驹菊局咀矩举沮聚拒据巨具距踞锯俱句惧炬剧捐鹃娟倦眷卷绢撅攫抉掘倔爵觉决诀绝均菌钧军君峻俊竣浚郡骏",
        "k": "喀咖卡咯开揩楷凯慨刊堪勘坎砍看康慷糠扛抗亢炕考拷烤靠坷苛柯棵磕颗科壳咳可渴克刻客课肯啃垦恳坑吭空恐孔控抠口扣寇枯哭窟苦酷库裤夸垮挎跨胯块筷侩快宽款匡筐狂框矿眶旷况亏盔岿窥葵奎魁馈愧溃坤昆捆困括扩廓阔",
        "l": "垃拉喇蜡腊辣啦莱来赖蓝婪栏拦篮阑兰澜谰揽览懒缆烂滥琅榔狼廊郎朗浪捞劳牢老佬姥酪烙涝勒乐雷镭蕾磊累儡垒擂肋类泪棱楞冷厘梨犁黎篱狸离漓理李里鲤礼莉荔吏栗丽厉励砾历利傈例俐痢立粒沥隶力璃哩俩联莲连镰廉怜涟帘敛脸链恋炼练粮凉梁粱良两辆量晾亮谅撩聊僚疗燎寥辽潦了撂镣廖料列裂烈劣猎琳林磷霖临邻鳞淋凛赁吝拎玲菱零龄铃伶羚凌灵陵岭领另令溜流榴琉馏留刘瘤柳龙聋咙笼窿隆垄拢陇楼娄搂篓漏陋芦卢颅庐炉掳卤鲁麓碌露路赂鹿潞禄录陆戮驴吕铝侣旅履屡缕虑氯律率滤绿峦挛孪滦卵乱掠略抡轮伦仑沦纶论萝螺罗逻锣箩骡裸落洛骆络",
        "m": "妈麻玛码蚂马骂嘛吗埋买麦卖迈脉瞒馒蛮满蔓曼慢漫谩芒茫盲氓忙莽猫茅锚毛矛铆卯茂冒帽貌贸么玫枚梅酶霉煤没眉媒镁每美昧寐妹媚门闷们萌蒙檬盟猛梦孟眯醚靡糜迷谜弥米秘觅泌蜜密幂棉眠绵冕免勉娩缅面苗描瞄藐秒渺庙妙蔑灭民抿皿敏悯闽明螟鸣铭名命谬摸摹蘑模膜磨摩魔抹末莫墨默沫漠寞陌谋牟某拇牡亩姆母墓暮幕募慕木目睦牧穆",
        "n": "拿哪呐钠那娜纳氖乃奶耐奈南男难囊挠脑恼闹淖呢馁内嫩能妮霓倪泥尼拟你匿腻逆溺蔫拈年碾撵捻念娘酿鸟尿捏聂孽啮镊镍涅您柠狞凝宁拧泞牛扭钮纽纽农浓奴努怒女暖虐疟挪懦糯诺",
        "o": "哦欧鸥殴藕呕偶沤",
        "p": "趴爬帕怕琶拍排牌徘湃派攀潘盘磐盼畔判叛乓庞旁耪胖抛咆刨炮袍跑泡呸胚培裴赔陪配佩沛喷盆砰烹彭蓬棚硼篷膨朋鹏捧碰坯砒霹批披劈琵毗啤脾疲皮匹痞僻屁譬篇偏片飘漂瓢票撇瞥拼频贫品聘乒坪苹萍平凭瓶评屏坡泼颇婆破魄迫粕剖扑铺仆莆葡菩蒲埔朴圃普浦谱曝瀑",
        "q": "期欺栖戚妻七凄漆柒沏其棋奇歧畦崎脐旗祈祁骑起岂乞企启契砌器气迄弃汽泣讫掐洽牵扦钎铅千迁签仟谦乾黔钱钳前潜遣浅谴堑嵌欠歉枪呛腔羌墙蔷强抢橇锹敲悄桥瞧乔侨巧鞘撬翘峭俏窍切茄且怯窃钦侵亲秦琴勤芹擒禽寝沁青轻氢倾卿清擎晴氰情顷请庆琼穷秋丘邱球求囚酋泅趋区蛆曲躯屈驱渠取娶龋去趣圈颧权醛泉全痊拳犬券劝缺炔瘸却鹊榷确雀裙群",
        "r": "然燃冉染瓤壤攘嚷让饶扰绕惹热壬仁人忍韧任认刃妊纫扔仍日戎茸蓉荣融熔溶容绒冗揉柔肉茹蠕儒孺如辱乳汝入褥软阮蕊瑞锐闰润若弱",
        "s": "撒洒萨腮鳃塞赛三叁伞散桑嗓丧搔骚扫嫂瑟色涩森僧莎砂杀刹沙纱傻啥煞筛晒珊苫杉山删煽衫闪陕擅赡膳善汕扇缮伤商赏晌上尚裳梢捎稍烧芍勺韶少哨邵绍奢赊蛇舌舍赦摄射慑涉社设砷申呻伸身深娠绅神沈审婶甚肾慎渗声生甥牲升绳省盛剩胜圣师失狮施湿诗尸虱十石拾时什食蚀实识史矢使屎驶始式示士世柿事拭誓逝势是嗜噬适仕侍释饰氏市恃室视试收手首守寿授售受瘦兽蔬枢梳殊抒输叔舒淑疏书赎孰熟薯暑曙署蜀黍鼠属术述树束戍竖墅庶数漱恕刷耍摔衰甩帅栓拴霜双爽谁水睡税吮瞬顺舜说硕朔烁丝撕嘶思私司死肆寺嗣四伺似饲巳松耸怂颂送宋讼诵搜艘擞嗽苏酥俗素速粟僳塑溯宿诉肃酸蒜算虽隋随绥髓碎岁穗遂隧祟孙损笋蓑梭唆缩琐索锁所",
        "t": "塌他它她塔獭挞蹋踏胎苔抬台泰酞太态汰坍摊贪瘫滩坛檀痰潭谭谈坦毯袒碳探叹炭汤塘搪堂棠膛唐糖倘躺淌趟烫掏涛滔绦萄桃逃淘陶讨套特藤腾疼誊梯剔踢锑提题蹄啼体替嚏惕涕剃屉天添填田甜恬舔腆挑条迢眺跳贴铁帖厅听烃汀廷停亭庭挺艇通桐酮同铜彤童桶捅筒统痛偷投头透凸秃突图徒途涂屠土吐兔湍团推颓腿蜕褪退吞屯臀拖托脱鸵陀驮驼椭妥拓挖",
        "w": "挖蛙蛙洼瓦袜歪外豌弯湾玩顽丸烷完碗挽晚皖惋宛婉万腕汪王亡枉网往旺望忘妄威巍微危韦违围唯惟为潍维苇萎委伟伪尾纬未蔚味畏胃喂魏位渭谓尉慰卫瘟温蚊文闻纹吻稳紊问嗡翁瓮挝蜗涡窝我斡卧握沃巫呜钨乌污诬屋无芜梧吾吴毋武五捂午舞伍侮坞戊雾晤物勿务悟误昔熙析西硒矽晰嘻吸锡牺稀息希悉膝夕惜熄烯溪汐犀檄袭席习媳喜铣洗系隙戏细瞎虾匣霞辖暇峡侠狭下厦夏吓掀锨先仙鲜纤咸贤衔舷闲涎弦嫌显险现献县腺馅羡宪陷限线相厢镶香箱襄湘乡翔祥详想响享项巷橡像向象肖硝霄削哮嚣销消宵淆晓小孝校肖啸笑效楔些歇蝎鞋协挟携邪斜胁谐写械卸蟹懈泄泻谢屑薪芯锌欣辛新忻心信衅星腥猩惺兴刑型形邢行醒幸杏性姓兄凶胸匈汹雄熊休修羞朽嗅锈秀袖绣墟戌需虚嘘须徐许蓄酗叙旭序畜恤絮婿绪续轩喧宣悬旋玄选癣眩绚靴薛学穴雪血勋熏循旬询寻驯巡殉汛训讯逊迅",
        "y": "压押鸦鸭呀丫芽牙蚜崖衙涯雅哑亚讶焉阉淹烟盐严研蜒岩延言颜阎炎沿奄掩眼衍演艳堰燕厌砚雁唁彦焰宴谚验殃央鸯秧杨扬佯疡羊洋阳氧仰痒养样漾腰妖瑶摇尧遥窑谣姚咬舀药要耀椰噎耶爷野冶也页掖业叶曳腋夜液一壹医揖铱依伊衣颐夷遗移仪胰疑沂宜姨彝椅蚁倚已乙矣以艺抑易邑屹亿役臆逸肄疫亦裔意毅忆义益溢诣议谊译异翼翌绎茵荫因殷音阴姻吟银淫寅饮尹引隐印英樱婴鹰应缨莹萤营荧蝇迎赢盈影颖硬映哟拥佣臃痈庸雍踊蛹咏泳涌永恿勇用幽优悠忧尤由邮铀犹油游酉有友右佑釉诱又幼迂淤于盂榆虞愚舆余俞逾鱼愉渝渔隅予娱雨与屿禹宇语羽玉域芋郁吁遇喻峪御愈欲狱育誉浴寓裕预豫驭鸳渊冤元垣袁原援辕园员圆猿源缘远苑愿怨院曰约越跃岳粤月悦阅耘云郧匀陨允运蕴酝晕韵孕",
        "z": "匝砸杂栽哉灾宰载再在咱攒暂赞赃脏葬遭糟凿藻枣早澡蚤躁噪造皂灶燥责择则泽贼怎增憎曾赠扎喳渣札轧铡闸眨栅榨咋乍炸诈摘斋宅窄债寨瞻毡詹粘沾盏斩辗展蘸栈占战站湛绽樟章彰漳张掌涨杖丈帐账仗胀瘴障招昭找沼赵照罩兆肇召遮折哲蛰辙者锗蔗这浙珍斟真甄砧臻贞针侦枕疹诊震振镇阵蒸挣睁征狰争怔整拯正政症郑证芝枝支吱蜘知肢脂汁之织职直植殖执值侄址指止趾只旨纸志挚掷至致置帜峙制智秩稚质炙痔滞治窒中盅忠钟衷终种肿重仲众舟周州洲诌粥轴肘帚咒皱宙昼骤珠株蛛朱猪诸诛逐竹烛煮拄瞩嘱主著柱助蛀贮铸筑住注祝驻抓爪拽专砖转撰赚篆桩庄装妆撞壮状椎锥追赘坠缀谆准捉拙卓桌琢茁酌着灼浊兹咨资姿滋淄孜紫仔籽滓子自渍字鬃棕踪宗综总纵邹走奏揍租足卒族祖诅阻组钻纂嘴醉最罪尊遵昨左佐柞做作坐座",
    }
    for initial, chars in initials_map.items():
        for c in chars:
            _PINYIN_MAP[c] = initial


def _get_pinyin_initials(char):
    """获取单个中文字符的拼音首字母"""
    if not _PINYIN_MAP:
        _build_pinyin_map()
    return _PINYIN_MAP.get(char, "")


# ============================================================
# 命令行接口
# ============================================================

def print_results(results, query, raw=False):
    """打印搜索结果"""
    if not results:
        print(f"没有找到与 '{query}' 相关的结果")
        return

    print(f"找到 {len(results)} 条结果 (查询: {query})")
    print()

    type_labels = {
        "character": "角色资料",
        "story": "剧情",
        "world": "世界观",
        "system": "游戏系统",
        "event": "活动",
        "general": "综合",
    }

    for i, (score, entry) in enumerate(results, 1):
        fpath, line_num, ctx_before, line_text, ctx_after, ftype = entry
        ftype_label = type_labels.get(ftype, ftype)
        rel_path = os.path.relpath(fpath, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        print(f"[{i}] (得分: {score:.2f}) [{ftype_label}] {rel_path}:{line_num + 1}")

        if raw:
            # 显示上下文
            for cl in ctx_before:
                print(f"  | {cl}")
            print(f"  >> {line_text}")
            for cl in ctx_after:
                print(f"  | {cl}")
            print()
        else:
            # 简洁模式：只显示匹配行，截断过长内容
            display = line_text[:120] + "..." if len(line_text) > 120 else line_text
            print(f"  {display}")
            print()


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python search_index.py build                   构建索引")
        print("  python search_index.py search <关键词> [选项]   搜索")
        print("  python search_index.py related <关键词>         关联搜索")
        print("  python search_index.py update <文件路径>       增量更新")
        print("  python search_index.py stats                   索引统计")
        print()
        print("选项:")
        print("  --datadir PATH  数据目录 (默认: 自动检测)")
        print("  --type TYPE   文件类型 (all/character/story/world/system/event)")
        print("  --top N       返回结果数量 (默认 20)")
        print("  --raw         显示完整上下文")
        print()
        print("示例:")
        print("  python search_index.py build")
        print('  python search_index.py search "维尔汀" --type character --top 10')
        print('  python search_index.py search "暴雨" --type world')
        print('  python search_index.py related "维尔汀"')
        print('  python search_index.py update "data/角色/某某.md"')
        return

    command = sys.argv[1]

    # 解析数据目录
    data_dir = ""
    args = sys.argv[2:]
    for i, a in enumerate(args):
        if a == "--datadir" and i + 1 < len(args):
            data_dir = args[i + 1]
            break
    if not data_dir:
        data_dir = os.environ.get("REV1999_DATA", "")
    if not data_dir:
        data_dir = _default_data_dir()

    index = SearchIndex(data_dir)

    if command == "build":
        print("构建倒排索引...")
        print(f"分词引擎: {'jieba' if _HAS_JIEBA else '简单分词（降级模式）'}")
        print(f"数据目录: {data_dir}")
        print()
        index.build_index()

    elif command == "search":
        if len(sys.argv) < 3:
            print("错误: 请指定搜索关键词", file=sys.stderr)
            return

        # 解析参数
        query = sys.argv[2]
        filter_type = "all"
        top_k = 20
        raw = False

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--type" and i + 1 < len(sys.argv):
                filter_type = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--top" and i + 1 < len(sys.argv):
                top_k = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--raw":
                raw = True
                i += 1
            else:
                i += 1

        results = index.search(query, filter_type=filter_type, top_k=top_k)
        print_results(results, query, raw=raw)

    elif command == "related":
        if len(sys.argv) < 3:
            print("错误: 请指定搜索关键词", file=sys.stderr)
            return

        query = sys.argv[2]
        print(f"关联搜索: {query}")
        print("=" * 60)
        results = index.search_related(query)
        print_results(results, query, raw=True)

    elif command == "update":
        if len(sys.argv) < 3:
            print("错误: 请指定文件路径", file=sys.stderr)
            return
        file_path = sys.argv[2]
        if not os.path.isabs(file_path):
            file_path = os.path.join(data_dir, file_path)
        index.update_index(file_path)

    elif command == "stats":
        index.stats()

    else:
        print(f"未知命令: {command}", file=sys.stderr)
        print("可用命令: build, search, related, update, stats", file=sys.stderr)


if __name__ == "__main__":
    main()
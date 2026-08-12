#!/usr/bin/env bash
# 重返未来1999 数据包查询脚本 (macOS/Linux)
# 用法: bash query.sh "关键词" [类型]
#   类型可选: all(默认) | character | world | story | stage | fan | skill
# 数据根自动推导: REV1999_DATA 环境变量 > 上级 data/ 目录 > 自身位置回溯
# 2026-08-12 升级:
#   - 组合词降级匹配: 整串 0 命中时按 空格/助词(UTF-8 助词表文件或内置列表)/属性后缀/角色名词典 拆分, OR 检索
#   - character/story/world 类型补齐 扩充/ 与 雨前精编/ 指定卷
#   - 结果排序: 命中词数多者优先 (台词/正文命中优先于目录名命中)
set -u
KEYWORD="${1:-}"
TYPE="${2:-all}"
if [ -z "$KEYWORD" ]; then
  echo "用法: query.sh \"关键词\" [类型]"
  echo "类型: all/character/world/story/stage/fan/skill"
  exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---- 数据根定位 ----
DATA_ROOT=""
if [ -n "${REV1999_DATA:-}" ] && [ -d "$REV1999_DATA" ]; then
  DATA_ROOT="$REV1999_DATA"
fi
if [ -z "$DATA_ROOT" ]; then
  for _ in 1 2 3 4; do
    if [ -f "$SCRIPT_DIR/data/skill_00_主索引.md" ]; then
      DATA_ROOT="$SCRIPT_DIR/data"
      break
    fi
    SCRIPT_DIR="$(dirname "$SCRIPT_DIR")"
  done
fi
if [ -z "$DATA_ROOT" ]; then
  echo "ERROR: 无法定位数据根 (设置 REV1999_DATA 或将本脚本放入 skills/rev1999/scripts/)" >&2
  exit 1
fi
echo "数据根: $DATA_ROOT"

# ---- 按类型选目录（character/story/world 已补齐 扩充/ 与 雨前精编/ 指定卷） ----
SEARCH=()
EXTRA=()
case "$TYPE" in
  character) SEARCH=("角色列表" "角色" "轩事" "造像" "主线" "雨前精编" "其他")
             EXTRA=("扩充/06_角色档案全量.md" "扩充/41_种族分类体系与角色归类.md" "扩充/42_全角色深度链接索引.md" "雨前精编/04_角色生平精编.md" "skill_03_角色百科A.md" "skill_04_角色百科B.md" "skill_11_角色语音风格库.md" "skill_16_角色登场索引.md") ;;
  world)     SEARCH=("世界观设定" "小径" "官方资料")
             EXTRA=("扩充/41_种族分类体系与角色归类.md" "扩充/07_世界观设定与地点百科.md") ;;
  story)     SEARCH=("主线" "支线" "活动" "剧情时间线" "第三扇门" "局外演绎" "雨前精编")
             EXTRA=("扩充/01_主线剧情深度全解.md" "扩充/02_支线剧情深度全解.md" "扩充/03_轩事剧情深度全解.md" "扩充/11_全剧情时间线总表.md" "扩充/27_新增数据冲突报告.md" "雨前精编/02_主线剧情精编.md" "雨前精编/03_支线剧情精编.md" "雨前精编/05_更新补充.md") ;;
  stage)     SEARCH=("战斗关卡")
             EXTRA=("扩充/34_战斗关卡汇总索引.md") ;;
  fan)       SEARCH=("同人参考" "雨前精编")
             EXTRA=("扩充/14_同人圈九味考据.md") ;;
  skill)     SEARCH=() ;;
  *)         SEARCH=() ;;
esac

ARGS=()
if [ "$TYPE" = "skill" ]; then
  :
elif [ ${#SEARCH[@]} -gt 0 ]; then
  for d in "${SEARCH[@]}"; do
    [ -d "$DATA_ROOT/$d" ] && ARGS+=("$DATA_ROOT/$d")
  done
else
  ARGS=("$DATA_ROOT")
fi
for e in "${EXTRA[@]}"; do
  [ -f "$DATA_ROOT/$e" ] && ARGS+=("$DATA_ROOT/$e")
done
if [ ${#ARGS[@]} -eq 0 ]; then echo "命中文件数: 0"; exit 0; fi

# ---- 整串扫描（normal 模式） ----
if [ "$TYPE" = "skill" ]; then
  WHOLE="$(find "$DATA_ROOT" -maxdepth 1 -type f \( -name "skill_*.md" -o -name "analysis_*.txt" \) -exec grep -HnF -- "$KEYWORD" {} + 2>/dev/null | grep -v "all_pages" | grep -v "其他活动")"
else
  WHOLE="$(grep -rnF --include="*.md" --include="*.txt" --exclude="all_pages.md" --exclude="*其他活动.md" -- "$KEYWORD" "${ARGS[@]}" 2>/dev/null)"
fi
if [ -n "$WHOLE" ]; then
  echo "$WHOLE" | head -n 20
  CNT="$(printf '%s\n' "$WHOLE" | grep -c .)"
  echo "命中文件数: $CNT (超出20条请换更精确关键词或加类型过滤)"
  exit 0
fi

# ---- 助词表（优先读 UTF-8 文件：脚本目录/数据根的 助词表.txt、连接词.txt；缺省用内置列表） ----
CONNECTIVES=("的" "了" "吗" "呢" "怎么" "什么" "是" "在" "和" "与" "及" "或" "吧" "啊" "呀" "啦" "着" "过" "被" "把" "让" "从" "向" "往" "于" "对" "给" "为")
for f in "$SCRIPT_DIR/助词表.txt" "$SCRIPT_DIR/连接词.txt" "$DATA_ROOT/助词表.txt"; do
  if [ -s "$f" ]; then
    CONNECTIVES=()
    while IFS= read -r ln; do
      ln="$(printf '%s' "$ln" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
      [ -n "$ln" ] && CONNECTIVES+=("$ln")
    done < "$f"
    break
  fi
done

ATTR=("生日" "登场" "香调" "种族" "语音" "配队" "阵容" "体系" "剧情" "背景" "关系" "年龄" "身高" "体重" "外貌" "性格" "经历" "结局" "台词" "技能" "强度" "版本" "立绘" "衣着" "攻略" "时间线" "故事" "身份" "能力" "喜好" "职业" "武器" "国籍" "档案" "解析" "汇总" "索引")

# ---- 角色名词典（文件名即词条的目录 + 扩充/06 档案标题 + 雨前精编/04 生平标题） ----
DICT=()
for d in 角色列表 世界观设定 其他 造像 衣着 配音 心相; do
  [ -d "$DATA_ROOT/$d" ] || continue
  for b in "$DATA_ROOT/$d"/*.md "$DATA_ROOT/$d"/*.txt; do
    [ -f "$b" ] || continue
    nm="$(basename "$b")"
    nm="${nm%.*}"
    nm="${nm%%_*}"; nm="${nm%%＿*}"; nm="${nm%%-*}"; nm="${nm%%—*}"
    LEN=${#nm}
    if [ "$LEN" -ge 2 ] && [ "$LEN" -le 8 ]; then DICT+=("$nm"); fi
  done
done
if [ -f "$DATA_ROOT/扩充/06_角色档案全量.md" ]; then
  while IFS= read -r nm; do
    LEN=${#nm}
    [ "$LEN" -ge 2 ] && [ "$LEN" -le 8 ] && DICT+=("$nm")
  done < <(grep -E '^## +[^ （(]+[（(][0-9]' "$DATA_ROOT/扩充/06_角色档案全量.md" | sed -E 's/^## +([^ （(]+).*/\1/')
fi
if [ -f "$DATA_ROOT/雨前精编/04_角色生平精编.md" ]; then
  while IFS= read -r nm; do
    case "$nm" in
      *剧情*|*档案*|*索引*|*目录*|*附录*|*梗概*) continue ;;
    esac
    LEN=${#nm}
    [ "$LEN" -ge 2 ] && [ "$LEN" -le 8 ] && DICT+=("$nm")
  done < <(grep -E '^## +' "$DATA_ROOT/雨前精编/04_角色生平精编.md" | sed -E 's/^## +([^ （(]+).*/\1/')
fi
DICT="$(printf '%s\n' "${DICT[@]}" | grep -v '^$' | sort -u)"

# ---- 关键词拆分：整串 > 空格 > 助词 > 属性后缀 > 角色名词典 ----
TERMS=("$KEYWORD")
IFS=' ' read -ra SP <<< "$KEYWORD"
for t in "${SP[@]}"; do [ -n "$t" ] && TERMS+=("$t"); done
MASKED="$KEYWORD"
for c in "${CONNECTIVES[@]}"; do
  [ -n "$c" ] || continue
  MASKED="$(printf '%s' "$MASKED" | sed "s/$c/|/g")"
done
IFS='|' read -ra PP <<< "$MASKED"
for t in "${PP[@]}"; do [ -n "$t" ] && TERMS+=("$t"); done
for aw in "${ATTR[@]}"; do
  if [[ "$KEYWORD" == *"$aw" ]] && [ "${#KEYWORD}" -gt "${#aw}" ]; then
    pre="${KEYWORD%$aw}"
    [ -n "$pre" ] && { TERMS+=("$pre"); TERMS+=("$aw"); }
  fi
done
while IFS= read -r nm; do
  [ -n "$nm" ] || continue
  if [ "${#nm}" -lt "${#KEYWORD}" ] && [[ "$KEYWORD" == *"$nm"* ]]; then
    TERMS+=("$nm")
    rest="${KEYWORD//$nm/|}"
    IFS='|' read -ra RP <<< "$rest"
    for t in "${RP[@]}"; do
      [ -n "$t" ] && [ "${#t}" -lt "${#KEYWORD}" ] && TERMS+=("$t")
    done
  fi
done <<< "$DICT"
TERMS="$(printf '%s\n' "${TERMS[@]}" | grep -v '^$' | sort -u)"
TERM_N="$(printf '%s\n' "$TERMS" | grep -c .)"
if [ "$TERM_N" -le 1 ]; then
  echo "命中文件数: 0 (无法拆分关键词，请换更精确的关键词)"
  exit 0
fi

echo "[组合词降级匹配] 关键词 '$KEYWORD' 整串 0 命中，拆分为: $(printf '%s' "$TERMS" | tr '\n' '|' | sed 's/|$//') (OR 任一命中即显示)"

# ---- OR 检索：各词 -l 取并集 ----
HITS=""
if [ "$TYPE" = "skill" ]; then
  while IFS= read -r t; do
    [ -n "$t" ] || continue
    HITS+=$'\n'"$(find "$DATA_ROOT" -maxdepth 1 -type f \( -name 'skill_*.md' -o -name 'analysis_*.txt' \) -exec grep -lF -- "$t" {} + 2>/dev/null)"
  done <<< "$TERMS"
else
  while IFS= read -r t; do
    [ -n "$t" ] || continue
    HITS+=$'\n'"$(grep -rlF --include='*.md' --include='*.txt' --exclude='all_pages.md' --exclude='*其他活动.md' -- "$t" "${ARGS[@]}" 2>/dev/null)"
  done <<< "$TERMS"
fi
HITS="$(printf '%s\n' "$HITS" | grep -v '^$' | sort -u)"
if [ -z "$HITS" ]; then
  echo "降级匹配仍无命中，请换更精确的关键词。"
  echo "命中文件数: 0"
  exit 0
fi

TARR=()
while IFS= read -r t; do [ -n "$t" ] && TARR+=("$t"); done <<< "$TERMS"

# ---- 每个命中文件统计命中词数（多者优先），并显示最具体命中词上下文 ----
OUT=""
while IFS= read -r f; do
  [ -f "$f" ] || continue
  n=0; mt=""; best="$KEYWORD"
  for t in "${TARR[@]}"; do
    if grep -qF -- "$t" "$f" 2>/dev/null; then
      n=$((n+1)); mt="${mt}+${t}"
      [ "${#t}" -gt "${#best}" ] && best="$t"
    fi
  done
  rel="${f#$DATA_ROOT/}"
  first="$(grep -m1 -F -- "$best" "$f" 2>/dev/null | sed 's/^[[:space:]]*//')"
  [ ${#first} -gt 200 ] && first="${first:0:200}...(截断)"
  OUT+=$'\n'"$n|$rel|${mt#+}|$first"
done <<< "$HITS"
printf '%s\n' "$OUT" | grep -v '^$' | sort -rn | head -n 20 | while IFS='|' read -r n rel mt first; do
  echo "[$rel] (命中词: $mt)"
  echo "  $first"
done
echo "命中文件数: $(printf '%s\n' "$OUT" | grep -v '^$' | wc -l | tr -d ' ') (组合词降级匹配, 超出20条请换更精确关键词或加类型过滤)"

# ---- stage 目录名兜底（正文 0 命中时才启用；台词/正文命中优先） ----
if [ "$TYPE" = "stage" ] && [ -d "$DATA_ROOT/战斗关卡" ]; then
  MATCHED="$(find "$DATA_ROOT/战斗关卡" -type d -name "*$KEYWORD*" 2>/dev/null)"
  if [ -n "$MATCHED" ]; then
    while IFS= read -r d; do
      echo "[${d#$DATA_ROOT/}] (目录名命中)"
      ls -1 "$d" | sed 's/^/  /'
    done <<< "$MATCHED"
  fi
fi

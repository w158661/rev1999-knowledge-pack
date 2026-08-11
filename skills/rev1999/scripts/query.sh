#!/usr/bin/env bash
# 重返未来1999 数据包查询脚本 (macOS/Linux)
# 用法: bash query.sh "关键词" [类型]
#   类型可选: all(默认) | character | world | story | stage | fan | skill
# 数据根自动推导: REV1999_DATA 环境变量 > 上级 data/ 目录 > 自身位置回溯
set -u
KEYWORD="${1:-}"
TYPE="${2:-all}"
if [ -z "$KEYWORD" ]; then
  echo "用法: query.sh \"关键词\" [类型]"
  echo "类型: all/character/world/story/stage/fan/skill"
  exit 1
fi

# ---- 数据根定位 ----
DATA_ROOT=""
if [ -n "${REV1999_DATA:-}" ] && [ -d "$REV1999_DATA" ]; then
  DATA_ROOT="$REV1999_DATA"
fi
if [ -z "$DATA_ROOT" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
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

# ---- stage 类型：目录名匹配（活动名/章节名 → 关卡目录清单） ----
STAGE_DIR="$DATA_ROOT/战斗关卡"
if [ "$TYPE" = "stage" ] && [ -d "$STAGE_DIR" ]; then
  MATCHED="$(find "$STAGE_DIR" -type d -name "*$KEYWORD*" 2>/dev/null)"
  if [ -n "$MATCHED" ]; then
    while IFS= read -r d; do
      echo "[${d#$DATA_ROOT/}]"
      ls -1 "$d" | sed 's/^/  /'
    done <<< "$MATCHED"
    exit 0
  fi
  IDX="$DATA_ROOT/扩充/34_战斗关卡汇总索引.md"
  if [ -f "$IDX" ] && grep -q "$KEYWORD" "$IDX"; then
    echo "[扩充/34_战斗关卡汇总索引.md 命中 '$KEYWORD' 的前缀映射]"
    grep "$KEYWORD" "$IDX" | sed 's/^/  /'
    exit 0
  fi
fi

# ---- 按类型选目录 ----
case "$TYPE" in
  character) SEARCH=("角色列表" "角色" "轩事" "造像" "主线" "雨前精编") ;;
  world)     SEARCH=("世界观设定" "小径" "官方资料") ;;
  story)     SEARCH=("主线" "支线" "活动" "剧情时间线" "第三扇门" "局外演绎" "雨前精编") ;;
  stage)     SEARCH=("战斗关卡") ;;
  fan)       SEARCH=("同人参考" "雨前精编") ;;
  skill)     SEARCH=() ;;
  *)         SEARCH=() ;;
esac

if [ "$TYPE" = "skill" ]; then
  find "$DATA_ROOT" -maxdepth 1 -type f \( -name "skill_*.md" -o -name "analysis_*.txt" \) -exec grep -Hn -- "$KEYWORD" {} + | grep -v "all_pages" | head -n 40
elif [ ${#SEARCH[@]} -gt 0 ]; then
  ARGS=()
  for d in "${SEARCH[@]}"; do
    [ -d "$DATA_ROOT/$d" ] && ARGS+=("$DATA_ROOT/$d")
  done
  if [ ${#ARGS[@]} -eq 0 ]; then echo "命中文件数: 0"; exit 0; fi
  grep -rn --include="*.md" --include="*.txt" --exclude="all_pages.md" "$KEYWORD" "${ARGS[@]}" | head -n 40
else
  grep -rn --include="*.md" --include="*.txt" --exclude="all_pages.md" "$KEYWORD" "$DATA_ROOT" | head -n 40
fi

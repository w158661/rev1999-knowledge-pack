# 重返未来1999 数据包查询脚本 (Windows PowerShell)
# 用法: powershell -ExecutionPolicy Bypass -File query.ps1 "关键词" [类型]
#   类型可选: all(默认) | character | world | story | stage | fan | skill
# 数据根自动推导: REV1999_DATA 环境变量 > 上级 data/ 目录 > 自身位置回溯
$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$keyword = if ($args.Count -gt 0) { $args[0] } else { $null }
$type = if ($args.Count -gt 1) { $args[1] } else { 'all' }
if (-not $keyword) { Write-Host "用法: query.ps1 `"关键词`" [类型]"; Write-Host "类型: all/character/world/story/stage/fan/skill"; exit 1 }

# ---- 数据根定位 ----
$dataRoot = $null
if ($env:REV1999_DATA -and (Test-Path $env:REV1999_DATA)) { $dataRoot = $env:REV1999_DATA }
if (-not $dataRoot) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    for ($i = 0; $i -lt 4; $i++) {
        $cand = Join-Path $scriptDir 'data'
        if (Test-Path (Join-Path $cand 'skill_00_主索引.md')) { $dataRoot = $cand; break }
        $scriptDir = Split-Path -Parent $scriptDir
    }
}
if (-not $dataRoot) {
    $probe = Get-ChildItem -Path $PWD.Path -Recurse -Filter 'skill_00_主索引.md' -Depth 4 -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($probe) { $dataRoot = $probe.DirectoryName }
}
if (-not $dataRoot) { Write-Host 'ERROR: 无法定位数据根 (设置 REV1999_DATA 或将本脚本放入 skills/rev1999/scripts/)'; exit 1 }
Write-Host "数据根: $dataRoot"

$targets = $null
$skillOnly = $false
switch ($type) {
    'character' { $targets = @('角色列表','角色','轩事','造像','主线','雨前精编') }
    'world'     { $targets = @('世界观设定','小径','官方资料') }
    'story'     { $targets = @('主线','支线','活动','剧情时间线','第三扇门','局外演绎','雨前精编') }
    'stage'     { $targets = @('战斗关卡') }
    'fan'       { $targets = @('同人参考','雨前精编') }
    'skill'     { $skillOnly = $true }
    default     { $targets = $null }
}

# ---- stage 类型：目录名匹配（活动名/章节名 → 关卡目录清单） ----
if ($type -eq 'stage') {
    $stageRoot = Join-Path $dataRoot ([string][char]0x6218 + [string][char]0x6597 + [string][char]0x5173 + [string][char]0x5361)
    if (Test-Path $stageRoot) {
        $matched = Get-ChildItem $stageRoot -Directory | Where-Object { $_.Name -like "*$keyword*" }
        if (-not $matched) { $matched = Get-ChildItem $stageRoot -Recurse -Directory | Where-Object { $_.Name -like "*$keyword*" } }
        foreach ($m in $matched) {
            Write-Host "[$($m.FullName.Substring($dataRoot.Length + 1))]"
            Get-ChildItem $m.FullName -File | ForEach-Object { Write-Host "  $($_.Name)" }
        }
        if ($matched) { exit 0 }
    }
    $idxFile = Join-Path (Join-Path $dataRoot ([string][char]0x6269 + [string][char]0x5145)) '34_战斗关卡汇总索引.md'
    if (Test-Path $idxFile) {
        $idxText = [System.IO.File]::ReadAllText($idxFile, [System.Text.Encoding]::UTF8)
        if ($idxText.Contains($keyword)) {
            Write-Host "[扩充/34_战斗关卡汇总索引.md 命中 '$keyword' 的前缀映射]"
            $lines = $idxText -split "`n"
            foreach ($ln in $lines) { if ($ln.Contains($keyword)) { Write-Host "  $($ln.Trim())" } }
            exit 0
        }
    }
}

$files = @()
if ($skillOnly) {
    $files += Get-ChildItem $dataRoot -File | Where-Object { $_.Name -like 'skill_*.md' -or $_.Name -like 'analysis_*.txt' }
}
elseif ($targets) {
    foreach ($t in $targets) {
        $p = Join-Path $dataRoot $t
        if (Test-Path $p) { $files += Get-ChildItem $p -Recurse -File -Include *.md,*.txt -ErrorAction SilentlyContinue }
    }
} else {
    $files += Get-ChildItem $dataRoot -File | Where-Object { $_.Extension -in '.md', '.txt' }
    Get-ChildItem $dataRoot -Directory | ForEach-Object { $files += Get-ChildItem $_.FullName -Recurse -File -Include *.md,*.txt -ErrorAction SilentlyContinue }
}
$files = $files | Where-Object { $_.Name -notlike 'all_pages.md' }

$hit = 0
foreach ($f in $files) {
    try {
        $c = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
        if ($c.Contains($keyword)) {
            $hit++
            $rel = $f.FullName.Substring($dataRoot.Length + 1)
            Write-Host "[$rel]"
            $lines = $c -split "`n"
            for ($i = 0; $i -lt $lines.Count; $i++) {
                if ($lines[$i].Contains($keyword)) {
                    $s = [Math]::Max(0, $i - 1); $e = [Math]::Min($lines.Count - 1, $i + 1)
                    for ($j = $s; $j -le $e; $j++) {
                        $t = $lines[$j].Trim()
                        if ($t) { Write-Host "  $t" }
                    }
                    break
                }
            }
            if ($hit -ge 20) { Write-Host "...(已达20条上限)"; break }
        }
    } catch {}
}
Write-Host "命中文件数: $hit"

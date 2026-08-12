# 重返未来1999 数据包查询脚本 (Windows PowerShell)
# 用法: powershell -ExecutionPolicy Bypass -File query.ps1 "关键词" [类型]
#   类型可选: all(默认) | character | world | story | stage | fan | skill
# 数据根自动推导: REV1999_DATA 环境变量 > 上级 data/ 目录 > 自身位置回溯
# 2026-08-12 升级:
#   - 组合词降级匹配: 整串 0 命中时按 空格/助词(UTF-8 助词表文件或内置列表)/属性后缀/角色名词典 拆分, OR 检索
#   - character/story/world 类型补齐 扩充/ 与 雨前精编/ 指定卷
#   - 结果排序: 命中词数多者优先 (台词/正文命中优先于目录名命中)
$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$keyword = if ($args.Count -gt 0) { $args[0] } else { $null }
$type = if ($args.Count -gt 1) { $args[1] } else { 'all' }
if (-not $keyword) { Write-Host "用法: query.ps1 `"关键词`" [类型]"; Write-Host "类型: all/character/world/story/stage/fan/skill"; exit 1 }

$myScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# ---- 数据根定位 ----
$dataRoot = $null
if ($env:REV1999_DATA -and (Test-Path $env:REV1999_DATA)) { $dataRoot = $env:REV1999_DATA }
if (-not $dataRoot) {
    $scriptDir = $myScriptDir
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

# ---- 类型目标表（character/story/world 已补齐 扩充/ 与 雨前精编/ 指定卷） ----
$targets = $null
$skillOnly = $false
$extraFiles = @()
$kchong = Join-Path $dataRoot '扩充'
$kqian = Join-Path $dataRoot '雨前精编'
switch ($type) {
    'character' {
        $targets = @('角色列表','角色','轩事','造像','主线','雨前精编','其他')
        $extraFiles += @(
            (Join-Path $kchong '06_角色档案全量.md'),
            (Join-Path $kchong '41_种族分类体系与角色归类.md'),
            (Join-Path $kchong '42_全角色深度链接索引.md'),
            (Join-Path $kqian '04_角色生平精编.md'),
            (Join-Path $dataRoot 'skill_03_角色百科A.md'),
            (Join-Path $dataRoot 'skill_04_角色百科B.md'),
            (Join-Path $dataRoot 'skill_11_角色语音风格库.md'),
            (Join-Path $dataRoot 'skill_16_角色登场索引.md')
        )
    }
    'world' {
        $targets = @('世界观设定','小径','官方资料')
        $extraFiles += @(
            (Join-Path $kchong '41_种族分类体系与角色归类.md'),
            (Join-Path $kchong '07_世界观设定与地点百科.md')
        )
    }
    'story' {
        $targets = @('主线','支线','活动','剧情时间线','第三扇门','局外演绎','雨前精编')
        $extraFiles += @(
            (Join-Path $kchong '01_主线剧情深度全解.md'),
            (Join-Path $kchong '02_支线剧情深度全解.md'),
            (Join-Path $kchong '03_轩事剧情深度全解.md'),
            (Join-Path $kchong '11_全剧情时间线总表.md'),
            (Join-Path $kchong '27_新增数据冲突报告.md'),
            (Join-Path $kqian '02_主线剧情精编.md'),
            (Join-Path $kqian '03_支线剧情精编.md'),
            (Join-Path $kqian '05_更新补充.md')
        )
    }
    'stage' {
        $targets = @('战斗关卡')
        $extraFiles += (Join-Path $kchong '34_战斗关卡汇总索引.md')
    }
    'fan'   {
        $targets = @('同人参考','雨前精编')
        $extraFiles += (Join-Path $kchong '14_同人圈九味考据.md')
    }
    'skill' { $skillOnly = $true }
    default { $targets = $null }
}

# ---- 文件清单 ----
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
foreach ($ef in $extraFiles) { if (Test-Path $ef) { $files += Get-Item $ef } }
$files = $files | Where-Object { $_.Name -notlike 'all_pages.md' -and $_.Name -notlike '*其他活动.md' } | Sort-Object FullName -Unique

# ---- 助词表（优先读 UTF-8 文件：脚本目录/数据根的 助词表.txt、连接词.txt；缺省用内置列表） ----
function Get-Connectives {
    $cand = @(
        (Join-Path $myScriptDir '助词表.txt'),
        (Join-Path $myScriptDir '连接词.txt'),
        (Join-Path $dataRoot '助词表.txt')
    )
    foreach ($p in $cand) {
        if (Test-Path $p) {
            $list = @()
            foreach ($ln in [System.IO.File]::ReadAllLines($p, [System.Text.Encoding]::UTF8)) {
                $t = $ln.Trim()
                if ($t) { $list += $t }
            }
            if ($list.Count -gt 0) { return $list }
        }
    }
    return @('的','了','吗','呢','怎么','什么','是','在','和','与','及','或','吧','啊','呀','啦','着','过','被','把','让','从','向','往','于','对','给','为')
}

$attrWords = @('生日','登场','香调','种族','语音','配队','阵容','体系','剧情','背景','关系','年龄','身高','体重','外貌','性格','经历','结局','台词','技能','强度','版本','立绘','衣着','攻略','时间线','故事','身份','能力','喜好','职业','武器','国籍','档案','解析','汇总','索引')

# ---- 角色名词典（文件名即词条的目录 + 扩充/06 档案标题 + 雨前精编/04 生平标题） ----
function Build-NameDict {
    $names = [System.Collections.Generic.HashSet[string]]::new()
    foreach ($d in @('角色列表','世界观设定','其他','造像','衣着','配音','心相')) {
        $p = Join-Path $dataRoot $d
        if (Test-Path $p) {
            foreach ($f in Get-ChildItem $p -File -ErrorAction SilentlyContinue) {
                $nm = ($f.BaseName -split '[＿_\-—]')[0].Trim()
                if ($nm.Length -ge 2 -and $nm.Length -le 8 -and $nm -notmatch '[\s#*|\[\]]') { [void]$names.Add($nm) }
            }
        }
    }
    $f06 = Join-Path (Join-Path $dataRoot '扩充') '06_角色档案全量.md'
    if (Test-Path $f06) {
        foreach ($ln in [System.IO.File]::ReadAllLines($f06, [System.Text.Encoding]::UTF8)) {
            if ($ln -match '^##\s+([^\s（(]{1,8})[（(]\s*\d') { [void]$names.Add($Matches[1]) }
        }
    }
    $f04 = Join-Path (Join-Path $dataRoot '雨前精编') '04_角色生平精编.md'
    if (Test-Path $f04) {
        foreach ($ln in [System.IO.File]::ReadAllLines($f04, [System.Text.Encoding]::UTF8)) {
            if ($ln -match '^##\s+([^\s（(]{1,8})') {
                $nm = $Matches[1]
                if ($nm -notmatch '[\s#*|\[\]]' -and $nm -notmatch '剧情|档案|索引|目录|附录|梗概') { [void]$names.Add($nm) }
            }
        }
    }
    return $names
}

# ---- 关键词拆分：整串 > 空格 > 助词 > 属性后缀 > 角色名词典 ----
function Split-Keywords {
    param([string]$kw, [string[]]$conn, [string[]]$dict, [string[]]$attr)
    $terms = [System.Collections.Generic.List[string]]::new()
    $terms.Add($kw)
    foreach ($t in ($kw -split '\s+')) { $t = $t.Trim(); if ($t) { $terms.Add($t) } }
    $masked = $kw
    foreach ($c in ($conn | Sort-Object Length -Descending)) { $masked = $masked.Replace($c, '|') }
    foreach ($t in ($masked -split '\|')) { $t = $t.Trim(); if ($t) { $terms.Add($t) } }
    foreach ($aw in $attr) {
        if ($kw.Length -gt $aw.Length -and $kw.EndsWith($aw)) {
            $pre = $kw.Substring(0, $kw.Length - $aw.Length)
            if ($pre) { $terms.Add($pre); $terms.Add($aw) }
        }
    }
    foreach ($nm in ($dict | Sort-Object Length -Descending)) {
        if ($nm.Length -lt $kw.Length -and $kw.Contains($nm)) {
            $terms.Add($nm)
            foreach ($rest in ($kw.Replace($nm, '|') -split '\|')) {
                $rest = $rest.Trim()
                if ($rest -and $rest.Length -lt $kw.Length) { $terms.Add($rest) }
            }
        }
    }
    $seen = [System.Collections.Generic.HashSet[string]]::new()
    $out = [System.Collections.Generic.List[string]]::new()
    foreach ($t in $terms) {
        $t = $t.Trim()
        if ($t -and $seen.Add($t)) { $out.Add($t) }
    }
    return $out
}

# ---- 全文扫描：OR 匹配，记录命中词数与上下文 ----
function Invoke-Scan {
    param([object[]]$fs, [string[]]$terms, [string]$root)
    $hits = @()
    foreach ($f in $fs) {
        try {
            $c = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
            $matched = @()
            foreach ($t in $terms) { if ($c.Contains($t)) { $matched += $t } }
            if ($matched.Count -gt 0) {
                $best = ($matched | Sort-Object Length -Descending | Select-Object -First 1)
                $rel = $f.FullName.Substring($root.Length + 1)
                $lines = $c -split "`n"
                $ctx = @()
                for ($i = 0; $i -lt $lines.Count; $i++) {
                    if ($lines[$i].Contains($best)) {
                        $s = [Math]::Max(0, $i - 1); $e = [Math]::Min($lines.Count - 1, $i + 1)
                        for ($j = $s; $j -le $e; $j++) {
                            $t = $lines[$j].Trim()
                            if ($t.Length -gt 200) { $t = $t.Substring(0, 200) + "...(截断)" }
                            if ($t) { $ctx += $t }
                        }
                        break
                    }
                }
                $hits += [PSCustomObject]@{ Rel = $rel; Count = $matched.Count; Terms = $matched; Ctx = $ctx }
            }
        } catch {}
    }
    return $hits
}

# ---- 主流程 ----
$terms = @($keyword)
$degraded = $false
$hits = @(Invoke-Scan $files $terms $dataRoot)
if ($hits.Count -eq 0) {
    $conn = Get-Connectives
    $dict = Build-NameDict
    $terms = @(Split-Keywords $keyword $conn $dict $attrWords)
    if ($terms.Count -gt 1) {
        $degraded = $true
        Write-Host "[组合词降级匹配] 关键词 '$keyword' 整串 0 命中，拆分为: $($terms -join ' | ') (OR 任一命中即显示)"
        $hits = @(Invoke-Scan $files $terms $dataRoot)
    }
}
$hits = @($hits | Sort-Object @{Expression = { $_.Count }; Descending = $true }, @{Expression = { $_.Rel } })

$shown = 0
foreach ($h in $hits) {
    $shown++
    if ($shown -gt 20) { Write-Host "...(共超过20条命中，仅显示前20条)"; break }
    $tag = ''
    if ($degraded) { $tag = " (命中词: $($h.Terms -join '+'))" }
    Write-Host "[$($h.Rel)]$tag"
    foreach ($ln in $h.Ctx) { Write-Host "  $ln" }
}

# ---- stage 目录名兜底（正文 0 命中时才启用；台词/正文命中优先） ----
if ($hits.Count -eq 0 -and $type -eq 'stage') {
    $stageRoot = Join-Path $dataRoot '战斗关卡'
    if (Test-Path $stageRoot) {
        $matched = Get-ChildItem $stageRoot -Directory | Where-Object { $_.Name -like "*$keyword*" }
        if (-not $matched) { $matched = Get-ChildItem $stageRoot -Recurse -Directory | Where-Object { $_.Name -like "*$keyword*" } }
        foreach ($m in $matched) {
            Write-Host "[$($m.FullName.Substring($dataRoot.Length + 1))] (目录名命中)"
            Get-ChildItem $m.FullName -File | ForEach-Object { Write-Host "  $($_.Name)" }
        }
    }
}

if ($hits.Count -eq 0) {
    if ($degraded) { Write-Host "降级匹配仍无命中，请换更精确的关键词。" }
    Write-Host "命中文件数: 0"
} else {
    Write-Host "命中文件数: $($hits.Count)$(if ($degraded) { ' (组合词降级匹配)' } else { '' }) (超出20条请换更精确关键词或加类型过滤)"
}

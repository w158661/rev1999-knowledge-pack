<#
.SYNOPSIS
    rev1999 知识技能包 —— 安装到本机 DSH（DeepSeek Harness）
.DESCRIPTION
    做三件事：
      1. 把 skills/rev1999* 镜像到 $DSH_HOME/skills/（DSH 的用户级技能根，所有项目可见）
      2. 把 data/ 镜像到 $DSH_HOME/rev1999-pack/data/（可用 -Junction 改成目录联接，不占空间）
      3. 把用户环境变量 REV1999_DATA 指向该数据根，并跑一次端到端自检
    镜像用 robocopy /MIR，会删除目标里多出来的文件，所以别往这两个目录里手工放东西。
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File install-dsh.ps1
    powershell -ExecutionPolicy Bypass -File install-dsh.ps1 -DshHome D:\dsh -Junction
    powershell -ExecutionPolicy Bypass -File install-dsh.ps1 -SkillsOnly
#>
param(
    [string]$DshHome = $(if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $env:USERPROFILE ".dsh" }),
    [switch]$Junction,
    [switch]$SkillsOnly,
    [switch]$SkipVerify,
    [switch]$NoEnv
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$PackRoot  = Split-Path -Parent $MyInvocation.MyCommand.Path
$SrcSkills = Join-Path $PackRoot "skills"
$SrcData   = Join-Path $PackRoot "data"
$DstSkills = Join-Path $DshHome "skills"
$DstData   = Join-Path $DshHome "rev1999-pack\data"

Write-Host "=== rev1999 知识技能包 -> DSH 安装 ==="
Write-Host "包根    : $PackRoot"
Write-Host "DSH_HOME: $DshHome"
Write-Host ""

# ---------- 0. 源校验 ----------
if (-not (Test-Path (Join-Path $SrcData "skill_00_主索引.md"))) {
    Write-Host "错误: $SrcData 不是有效数据根（缺少 skill_00_主索引.md）" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path (Join-Path $SrcSkills "rev1999\SKILL.md"))) {
    Write-Host "错误: $SrcSkills 下找不到 rev1999/SKILL.md" -ForegroundColor Red
    exit 1
}

if (-not $SkipVerify) {
    $vp = Join-Path $PackRoot "scripts\verify_pack.py"
    if ((Test-Path $vp) -and (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host ">>> 安装前校验 (verify_pack.py) ..."
        & python $vp | Select-Object -Last 6
        if ($LASTEXITCODE -ne 0) {
            Write-Host "verify_pack 未通过，已中止安装（-SkipVerify 可强制）" -ForegroundColor Red
            exit 1
        }
        Write-Host ""
    }
}

# ---------- 1. 同步技能 ----------
New-Item -ItemType Directory -Path $DstSkills -Force | Out-Null
$skillDirs = Get-ChildItem -LiteralPath $SrcSkills -Directory | Where-Object { $_.Name -like "rev1999*" }
Write-Host (">>> 同步技能到 $DstSkills （" + $skillDirs.Count + " 个）")
foreach ($d in $skillDirs) {
    $dst = Join-Path $DstSkills $d.Name
    robocopy $d.FullName $dst /MIR /XD __pycache__ /XF *.pyc *.pyo /R:1 /W:1 /NFL /NDL /NJH /NJS /NP /NS /NC | Out-Null
    if ($LASTEXITCODE -ge 8) { Write-Host ("    失败: " + $d.Name + " (robocopy " + $LASTEXITCODE + ")") -ForegroundColor Red; exit 1 }
    Write-Host ("    - " + $d.Name)
}

# ---------- 2. 同步数据 ----------
if ($SkillsOnly) {
    Write-Host ""
    Write-Host "已指定 -SkillsOnly，跳过数据同步。"
} else {
    $parent = Split-Path -Parent $DstData
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    $isLink = (Get-Item -LiteralPath $DstData -Force -ErrorAction SilentlyContinue).LinkType
    if ($isLink) {
        Write-Host ""
        Write-Host (">>> 目标是链接 (" + $isLink + ")，先拆除")
        cmd /c rmdir "$DstData"
    }
    if ($Junction) {
        Write-Host ""
        Write-Host (">>> 建立目录联接: $DstData -> $SrcData")
        cmd /c mklink /J "$DstData" "$SrcData" | Out-Null
        if (-not (Test-Path (Join-Path $DstData "skill_00_主索引.md"))) { Write-Host "联接建立失败" -ForegroundColor Red; exit 1 }
    } else {
        Write-Host ""
        Write-Host (">>> 镜像数据到 $DstData （145MB 左右，稍等）")
        robocopy $SrcData $DstData /MIR /XD .index __pycache__ /XF *.pyc /R:1 /W:1 /NFL /NDL /NJH /NJS /NP /NS /NC | Out-Null
        if ($LASTEXITCODE -ge 8) { Write-Host ("数据镜像失败 (robocopy " + $LASTEXITCODE + ")") -ForegroundColor Red; exit 1 }
        $c = (Get-ChildItem -LiteralPath $DstData -Recurse -File | Measure-Object).Count
        Write-Host ("    已同步 " + $c + " 个文件")
    }
}

# ---------- 3. 设置环境变量 ----------
if ((-not $SkillsOnly) -and (-not $NoEnv)) {
    Write-Host ""
    $want = $DstData
    $cur  = [Environment]::GetEnvironmentVariable("REV1999_DATA", "User")
    if ($cur -eq $want) {
        Write-Host "REV1999_DATA 已是 $want，跳过"
    } else {
        Write-Host (">>> 设置用户环境变量 REV1999_DATA: " + $(if ($cur) { $cur } else { "(未设置)" }) + " -> $want")
        [Environment]::SetEnvironmentVariable("REV1999_DATA", $want, "User")
    }
    $env:REV1999_DATA = $want
}

# ---------- 4. 端到端自检 ----------
Write-Host ""
Write-Host ">>> 端到端自检"
$installed = Join-Path $DstSkills "rev1999\scripts\query.ps1"
if (Test-Path $installed) {
    $out = & powershell -ExecutionPolicy Bypass -File $installed "维尔汀" character 2>&1
    $head = $out | Select-Object -First 3
    $head | ForEach-Object { Write-Host ("    " + $_) }
    $hit = ($out | Select-String -Pattern "命中文件数" | Select-Object -First 1).Line
    Write-Host ("    " + $hit)
    if ($hit -match "命中文件数: 0") { Write-Host "自检失败：0 命中" -ForegroundColor Red; exit 1 }
    Write-Host "    自检通过 ✓" -ForegroundColor Green
} else {
    Write-Host "    未找到已安装的 query.ps1，跳过" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== 安装完成 ==="
Write-Host ("技能: " + $DstSkills)
if (-not $SkillsOnly) { Write-Host ("数据: " + $DstData) }
Write-Host "DSH 会通过 chokidar 监听技能根，通常无需重启即可生效；若当前会话看不到，重开一个会话即可。"

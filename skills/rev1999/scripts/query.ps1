# 重返未来1999 数据查询脚本 (Windows PowerShell 版)
# 用法: .\query.ps1 <关键词> [文件类型]
# 文件类型: all(默认), character, story, system, world, event, stage, related
# 与 query.sh 功能等价，供 Windows 环境使用。

param(
    [Parameter(Mandatory=$true)][string]$Keyword,
    [string]$Type = "all"
)

$ErrorActionPreference = "SilentlyContinue"

# 数据路径: 优先 REV1999_DATA 环境变量，否则包内路径
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackageData = (Resolve-Path (Join-Path $ScriptDir "..\..\..")).Path + "\data"
if ($env:REV1999_DATA -and (Test-Path -LiteralPath $env:REV1999_DATA)) {
    $Base = $env:REV1999_DATA
} else {
    $Base = $PackageData
}

if (-not (Test-Path -LiteralPath $Base)) {
    Write-Host "错误: 数据目录不存在 ($Base)" -ForegroundColor Red
    Write-Host "请设置环境变量 REV1999_DATA 指向数据目录"
    Write-Host "  [Environment]::SetEnvironmentVariable('REV1999_DATA', 'C:\path\to\rev1999-pack\data', 'User')"
    exit 1
}

function Search-In($Paths, $Label, $Max = 50) {
    if (-not $Paths) { return }
    $hits = @()
    foreach ($p in $Paths) {
        if (Test-Path -LiteralPath $p) {
            $hits += Select-String -Path $p -Pattern $Keyword -Encoding UTF8 | Select-Object -First $Max
        }
    }
    if ($hits.Count -gt 0) {
        Write-Host "--- $Label ---" -ForegroundColor Cyan
        $hits | Select-Object -First $Max | ForEach-Object {
            $line = $_.Line
            if ($line.Length -gt 200) { $line = $line.Substring(0, 200) + "..." }
            Write-Host ("{0}:{1}: {2}" -f (Split-Path $_.Path -Leaf), $_.LineNumber, $line)
        }
    }
}

$q = [regex]::Escape($Keyword)

switch ($Type) {
    "character" {
        Write-Host "=== 搜索角色资料: $Keyword ===" -ForegroundColor Yellow
        Search-In @("$Base\角色", "$Base\角色列表") "角色原始数据"
        Search-In @("$Base\skill_03_角色百科A.md", "$Base\skill_04_角色百科B.md") "角色百科"
        Search-In @("$Base\扩充\06_角色档案全量.md", "$Base\扩充\05_角色故事文学深度全解.md") "扩充卷(权威)"
        Search-In @("$Base\雨前精编\04_角色生平精编.md") "雨前精编(权威)"
    }
    "story" {
        Write-Host "=== 搜索剧情: $Keyword ===" -ForegroundColor Yellow
        Search-In @("$Base\主线", "$Base\支线", "$Base\轩事") "剧情原始数据"
        Search-In @("$Base\skill_02_时间线与主线.md", "$Base\skill_05_支线活动.md") "知识文档"
        Search-In @("$Base\扩充\01_主线剧情深度全解.md", "$Base\扩充\02_支线剧情深度全解.md", "$Base\扩充\03_轩事剧情深度全解.md", "$Base\扩充\11_全剧情时间线总表.md") "扩充卷(深度)"
        Search-In @("$Base\雨前精编\02_主线剧情精编.md", "$Base\雨前精编\03_支线剧情精编.md") "雨前精编(权威)"
    }
    "system" {
        Write-Host "=== 搜索游戏系统: $Keyword ===" -ForegroundColor Yellow
        Search-In @("$Base\征集", "$Base\心相", "$Base\鬃毛邮报", "$Base\雨中悬想", "$Base\人工梦游") "系统原始数据"
        Search-In @("$Base\skill_06_游戏系统.md") "知识文档"
        Search-In @("$Base\扩充\08_系统机制深度全解.md") "扩充卷(深度)"
    }
    "world" {
        Write-Host "=== 搜索世界观: $Keyword ===" -ForegroundColor Yellow
        Search-In @("$Base\世界观设定", "$Base\小径", "$Base\第三扇门") "世界观原始数据"
        Search-In @("$Base\skill_01_世界观核心.md", "$Base\skill_08_术语词典.md") "知识文档"
        Search-In @("$Base\扩充\07_世界观设定与地点百科.md", "$Base\扩充\13_九味风格总纲.md") "扩充卷(深度)"
        Search-In @("$Base\雨前精编\01_世界观与组织.md") "雨前精编(权威)"
    }
    "event" {
        Write-Host "=== 搜索活动: $Keyword ===" -ForegroundColor Yellow
        Search-In @("$Base\轩事", "$Base\活动", "$Base\UTTU", "$Base\版本") "活动原始数据"
        Search-In @("$Base\skill_05_支线活动.md") "知识文档"
        Search-In @("$Base\扩充\04_活动版本深度全解.md") "扩充卷(深度)"
    }
    "stage" {
        Write-Host "=== 搜索战斗关卡: $Keyword ===" -ForegroundColor Yellow
        Search-In @("$Base\战斗关卡\*.md", "$Base\战斗关卡\*\*.md", "$Base\战斗关卡\*\*\*.md") "战斗关卡原始数据" 30
        Search-In @("$Base\扩充\34_战斗关卡汇总索引.md", "$Base\扩充\28_*.md", "$Base\扩充\29_*.md", "$Base\扩充\30_*.md", "$Base\扩充\31_*.md", "$Base\扩充\32_*.md", "$Base\扩充\33_*.md") "关卡深度索引(扩充28~34)" 30
    }
    "related" {
        Write-Host "=== 关联搜索: $Keyword ===" -ForegroundColor Yellow
        foreach ($dir in @("角色", "角色列表", "主线", "支线", "世界观设定", "小径", "雨前精编", "扩充", "战斗关卡")) {
            $hits = @()
            $pat = Join-Path $Base ($dir + '\*.md')
            if (Test-Path $pat) {
                $hits += Select-String -Path $pat -Pattern $Keyword -Encoding UTF8 | Select-Object -First 3
            }
            $nested = Join-Path $Base ($dir + '\*\*.md')
            if (Test-Path $nested) {
                $hits += Select-String -Path $nested -Pattern $Keyword -Encoding UTF8 | Select-Object -First 3
            }
            if ($hits.Count -gt 0) {
                Write-Host "--- $dir ---" -ForegroundColor Cyan
                $hits | Select-Object -ExpandProperty Path -Unique | ForEach-Object { Write-Host (Split-Path $_ -Leaf) }
            }
        }
    }
    default {
        Write-Host "=== 全面搜索: $Keyword ===" -ForegroundColor Yellow
        Search-In @((Get-ChildItem -LiteralPath $Base -Filter "skill_*.md" | ForEach-Object { $_.FullName })) "知识文档" 40
        Search-In @("$Base\角色", "$Base\角色列表") "角色数据" 15
        Search-In @("$Base\主线", "$Base\支线") "剧情数据" 15
        Search-In @("$Base\世界观设定", "$Base\小径") "世界观数据" 15
        Search-In @("$Base\雨前精编\*.md", "$Base\扩充\*.md") "扩充卷(深度)" 25
        Search-In @("$Base\战斗关卡\*.md", "$Base\战斗关卡\*\*.md", "$Base\战斗关卡\*\*\*.md") "战斗关卡" 15
    }
}

Write-Host "=== 搜索完成 ===" -ForegroundColor Green

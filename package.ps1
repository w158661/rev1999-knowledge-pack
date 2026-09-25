<#
.SYNOPSIS
    rev1999 知识技能包 —— 纯净打包脚本
.DESCRIPTION
    把本包打成可直接分发/上传的 zip，自动排除以下内容：
      .git/  __pycache__/  *.pyc  *.pyo  data/.index/  *.zip  *.log
      .vscode/  .idea/  Thumbs.db  .DS_Store  desktop.ini
    打包前默认先跑 scripts/verify_pack.py（-SkipVerify 可跳过）。
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File package.ps1
    powershell -ExecutionPolicy Bypass -File package.ps1 -OutDir D:\dist -Version 2.9.0
#>
param(
    [string]$OutDir = [Environment]::GetFolderPath("Desktop"),
    [string]$Version = "2.9.0",
    [switch]$SkipVerify,
    [switch]$KeepStaging
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$PackRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseName = "rev1999-knowledge-pack-v$Version"
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }
$ZipPath = Join-Path $OutDir "$BaseName.zip"

Write-Host "=== rev1999 纯净打包 ===" 
Write-Host "包根: $PackRoot"
Write-Host "输出: $ZipPath"

# ---------- 1. 校验 ----------
if (-not $SkipVerify) {
    $vp = Join-Path $PackRoot "scripts\verify_pack.py"
    if (Test-Path $vp) {
        Write-Host ""
        Write-Host ">>> 运行 verify_pack.py ..."
        $py = Get-Command python -ErrorAction SilentlyContinue
        if ($py) {
            & python $vp
            if ($LASTEXITCODE -ne 0) {
                Write-Host "verify_pack.py 未通过（退出码 $LASTEXITCODE），已中止打包。加 -SkipVerify 可强制打包。" -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "未找到 python，跳过校验（可用 -SkipVerify 显式跳过）" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "已跳过 verify_pack 校验"
}

# ---------- 2. 暂存目录 ----------
$StageRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("rev1999_pack_" + [Guid]::NewGuid().ToString("N").Substring(0, 8))
$Stage = Join-Path $StageRoot $BaseName
New-Item -ItemType Directory -Path $Stage -Force | Out-Null

$ExcludeDirs  = @(".git", "__pycache__", ".index", ".vscode", ".idea")
$ExcludeFiles = @("*.pyc", "*.pyo", "*.zip", "*.log", "Thumbs.db", ".DS_Store", "desktop.ini")

function Copy-Filtered {
    param([string]$Src, [string]$Dst)
    New-Item -ItemType Directory -Path $Dst -Force | Out-Null
    foreach ($d in Get-ChildItem -LiteralPath $Src -Directory -Force) {
        if ($ExcludeDirs -contains $d.Name) { continue }
        Copy-Filtered -Src $d.FullName -Dst (Join-Path $Dst $d.Name)
    }
    foreach ($f in Get-ChildItem -LiteralPath $Src -File -Force) {
        $skip = $false
        foreach ($pat in $ExcludeFiles) { if ($f.Name -like $pat) { $skip = $true; break } }
        if ($skip) { continue }
        Copy-Item -LiteralPath $f.FullName -Destination (Join-Path $Dst $f.Name) -Force
    }
}

Write-Host ""
Write-Host ">>> 复制文件（已排除 .git / __pycache__ / *.pyc / data/.index 等）..."
Copy-Filtered -Src $PackRoot -Dst $Stage

$stageFiles = (Get-ChildItem -LiteralPath $Stage -Recurse -File -Force | Measure-Object).Count
$stageSize  = (Get-ChildItem -LiteralPath $Stage -Recurse -File -Force | Measure-Object -Property Length -Sum).Sum
Write-Host ("    文件数: {0} / 未压缩 {1:N1} MB" -f $stageFiles, ($stageSize / 1MB))

# ---------- 3. 压缩 ----------
if (Test-Path $ZipPath) { Remove-Item -LiteralPath $ZipPath -Force }
Add-Type -AssemblyName System.IO.Compression | Out-Null
Add-Type -AssemblyName System.IO.Compression.FileSystem | Out-Null
Write-Host ""
Write-Host ">>> 压缩中（条目名统一 / 分隔，兼容 macOS/Linux 解压）..."
# 不要用 ZipFile::CreateFromDirectory：.NET Framework 在 Windows 上会写入反斜杠条目名，
# macOS/Linux 解压时会把整棵树摊平成一堆带反斜杠的怪文件名。这里手工建条目并强制 / 分隔。
$fs = [System.IO.File]::Open($ZipPath, [System.IO.FileMode]::Create)
try {
    $archive = [System.IO.Compression.ZipArchive]::new($fs, [System.IO.Compression.ZipArchiveMode]::Create)
    try {
        $baseLen = $Stage.Length + 1
        foreach ($f in Get-ChildItem -LiteralPath $Stage -Recurse -File -Force) {
            $rel = $f.FullName.Substring($baseLen).Replace("\", "/")
            $entryName = "$BaseName/$rel"
            $null = [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $f.FullName, $entryName, [System.IO.Compression.CompressionLevel]::Optimal)
        }
        $archive.Dispose()
    } catch { $archive.Dispose(); throw }
} finally { $fs.Dispose() }

# ---------- 4. 清理与报告 ----------
if (-not $KeepStaging) { Remove-Item -LiteralPath $StageRoot -Recurse -Force -ErrorAction SilentlyContinue }
else { Write-Host "暂存目录保留于: $StageRoot" }

$zip = Get-Item -LiteralPath $ZipPath
$hash = (Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256).Hash
Write-Host ""
Write-Host "=== 打包完成 ==="
Write-Host ("输出: {0}" -f $zip.FullName)
Write-Host ("大小: {0:N2} MB" -f ($zip.Length / 1MB))
Write-Host ("SHA256: {0}" -f $hash)

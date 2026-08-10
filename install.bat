@echo off
chcp 65001 >nul
REM ============================================================
REM rev1999 知识技能包 安装脚本 (Windows 版)
REM 用法: install.bat [目标目录]
REM 默认目标: .claude\skills\ (当前项目)
REM 使用前请确认当前目录为 rev1999-pack
REM ============================================================
setlocal enabledelayedexpansion

set "PACKAGE_DIR=%~dp0"
set "PACKAGE_DIR=%PACKAGE_DIR:~0,-1%"
set "TARGET_DIR=%~1"
if "%TARGET_DIR%"=="" set "TARGET_DIR=%PACKAGE_DIR%\..\.claude\skills"
set "DATA_DIR=%PACKAGE_DIR%\data"

echo === 安装 rev1999 知识技能包 ===
echo 包目录: %PACKAGE_DIR%
echo 目标:   %TARGET_DIR%
echo 数据:   %DATA_DIR%

if not exist "%DATA_DIR%" (
    echo 错误: 数据目录不存在 "%DATA_DIR%"
    exit /b 1
)

if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

echo.
echo ^>^>^> 安装技能...
xcopy /e /i /q /y "%PACKAGE_DIR%\skills\*" "%TARGET_DIR%\" >nul
echo     已安装:
for /d %%d in ("%TARGET_DIR%\rev1999*") do echo     - %%~nxd

echo.
echo ^>^>^> 配置数据路径...
echo 请手动设置用户环境变量 REV1999_DATA（Windows 10/11）:
echo.
echo   setx REV1999_DATA "%DATA_DIR%"
echo.
echo 或在 PowerShell 中执行:
echo   [Environment]::SetEnvironmentVariable('REV1999_DATA', '%DATA_DIR%', 'User')
echo.

echo === 安装完成 ===
echo.
echo 使用方式:
echo   /rev1999           - 综合知识库
echo   /rev1999-roleplay  - 角色扮演
echo   /rev1999-oc        - OC创作
echo   /rev1999-team      - 队伍搭配
echo   /rev1999-story     - 剧情时间线
echo   /rev1999-query     - 数据快速查询
echo   /rev1999-write     - 写作辅助
echo   /rev1999-newbie    - 新手引导
echo.
echo 数据查询 (Windows):
echo   powershell -ExecutionPolicy Bypass -File "%PACKAGE_DIR%\skills\rev1999\scripts\query.ps1" "暴雨" world
echo   powershell -ExecutionPolicy Bypass -File "%PACKAGE_DIR%\skills\rev1999\scripts\query.ps1" "维尔汀" all
echo.
echo 说明: 数据目录仅需复制技能，数据文件可保留原位，通过 REV1999_DATA 指向。
endlocal

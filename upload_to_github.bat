@echo off
chcp 65001 >nul
echo ========================================
echo Wazuh Hunter Agent - GitHub 上傳腳本
echo ========================================
echo.

echo [1/6] 檢查 Git 安裝...
git --version >nul 2>&1
if errorlevel 1 (
    echo Git 未安裝！
    echo.
    echo 請先安裝 Git:
    echo 1. 下載: https://git-scm.com/download/win
    echo 2. 安裝後重新執行此腳本
    pause
    exit /b 1
)
echo Git 已安裝
echo.

echo [2/6] 初始化 Git 倉庫...
if not exist .git (
    git init
    echo Git 倉庫已初始化
) else (
    echo Git 倉庫已存在
)
echo.

echo [3/6] 添加文件到 Git...
git add .
echo 文件已添加
echo.

echo [4/6] 提交變更...
git commit -m "初始提交: 實作 Wazuh 威脅獵捕代理程式"
echo 變更已提交
echo.

echo [5/6] 設置 GitHub 遠端倉庫...
git remote remove origin 2>nul
git remote add origin https://github.com/kuobrian0102/wazuh_hunter_agent.git
echo 遠端倉庫已設置
echo.

echo [6/6] 設置主分支...
git branch -M main
echo 主分支已設置為 main
echo.

echo ========================================
echo 準備完成！
echo ========================================
echo.
echo 下一步操作:
echo.
echo 1. 在 GitHub 建立新倉庫:
echo    https://github.com/new
echo    - Repository name: wazuh_hunter_agent
echo    - 選擇 Public 或 Private
echo    - 不要勾選 'Initialize with README'
echo.
echo 2. 推送程式碼到 GitHub:
echo    git push -u origin main
echo.
echo 注意: 推送時需要 GitHub 認證
echo    - 使用 Personal Access Token
echo    - 或使用 GitHub CLI: gh auth login
echo.
echo ========================================
pause



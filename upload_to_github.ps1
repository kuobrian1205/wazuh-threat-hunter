# Wazuh Hunter Agent - 自動上傳到 GitHub 腳本
# 用戶名: kuobrian0102
# 倉庫名: wazuh_hunter_agent

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Wazuh Hunter Agent - GitHub 上傳腳本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 檢查 Git 是否安裝
Write-Host "[1/6] 檢查 Git 安裝..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    Write-Host "✓ Git 已安裝: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git 未安裝！" -ForegroundColor Red
    Write-Host ""
    Write-Host "請先安裝 Git:" -ForegroundColor Yellow
    Write-Host "1. 下載: https://git-scm.com/download/win" -ForegroundColor Cyan
    Write-Host "2. 安裝後重新執行此腳本" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "或使用以下指令手動上傳:" -ForegroundColor Yellow
    Write-Host "  git init" -ForegroundColor White
    Write-Host "  git add ." -ForegroundColor White
    Write-Host "  git commit -m '初始提交: 實作 Wazuh 威脅獵捕代理程式'" -ForegroundColor White
    Write-Host "  git remote add origin https://github.com/kuobrian0102/wazuh_hunter_agent.git" -ForegroundColor White
    Write-Host "  git branch -M main" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
    exit 1
}

# 初始化 Git 倉庫（如果還沒初始化）
Write-Host ""
Write-Host "[2/6] 初始化 Git 倉庫..." -ForegroundColor Yellow
if (-not (Test-Path .git)) {
    git init
    Write-Host "✓ Git 倉庫已初始化" -ForegroundColor Green
} else {
    Write-Host "✓ Git 倉庫已存在" -ForegroundColor Green
}

# 檢查是否有未提交的變更
Write-Host ""
Write-Host "[3/6] 檢查文件狀態..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "發現以下變更:" -ForegroundColor Cyan
    git status --short
} else {
    Write-Host "✓ 沒有未提交的變更" -ForegroundColor Green
}

# 添加所有文件
Write-Host ""
Write-Host "[4/6] 添加文件到 Git..." -ForegroundColor Yellow
git add .
Write-Host "✓ 文件已添加" -ForegroundColor Green

# 提交
Write-Host ""
Write-Host "[5/6] 提交變更..." -ForegroundColor Yellow
$commitMessage = "初始提交: 實作 Wazuh 威脅獵捕代理程式

- 實作威脅獵捕核心功能
- 支援多種威脅檢測（可疑IP、暴力破解、權限提升等）
- 完整的測試覆蓋
- GitHub Actions CI 配置"
git commit -m $commitMessage
Write-Host "✓ 變更已提交" -ForegroundColor Green

# 設置遠端倉庫
Write-Host ""
Write-Host "[6/6] 設置 GitHub 遠端倉庫..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/kuobrian0102/wazuh_hunter_agent.git"

# 檢查遠端是否已設置
$existingRemote = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0) {
    if ($existingRemote -eq $remoteUrl) {
        Write-Host "✓ 遠端倉庫已設置" -ForegroundColor Green
    } else {
        Write-Host "! 遠端倉庫已設置但 URL 不同，更新中..." -ForegroundColor Yellow
        git remote set-url origin $remoteUrl
        Write-Host "✓ 遠端倉庫 URL 已更新" -ForegroundColor Green
    }
} else {
    git remote add origin $remoteUrl
    Write-Host "✓ 遠端倉庫已添加" -ForegroundColor Green
}

# 設置主分支名稱
Write-Host ""
Write-Host "設置主分支..." -ForegroundColor Yellow
git branch -M main 2>&1 | Out-Null
Write-Host "✓ 主分支已設置為 main" -ForegroundColor Green

# 提示用戶推送
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "準備完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 在 GitHub 建立新倉庫:" -ForegroundColor Cyan
Write-Host "   https://github.com/new" -ForegroundColor White
Write-Host "   - Repository name: wazuh_hunter_agent" -ForegroundColor White
Write-Host "   - 選擇 Public 或 Private" -ForegroundColor White
Write-Host "   - 不要勾選 'Initialize with README'" -ForegroundColor White
Write-Host ""
Write-Host "2. 推送程式碼到 GitHub:" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "注意: 推送時需要 GitHub 認證" -ForegroundColor Yellow
Write-Host "   - 使用 Personal Access Token (推薦)" -ForegroundColor White
Write-Host "   - 或使用 GitHub CLI: gh auth login" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan



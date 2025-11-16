# 快速上傳到 GitHub 指南

## 用戶名: kuobrian0102
## 倉庫名: wazuh_hunter_agent

## 方法 1: 使用自動化腳本（推薦）

### 如果已安裝 Git：

**Windows PowerShell:**
```powershell
.\upload_to_github.ps1
```

**Windows CMD:**
```cmd
upload_to_github.bat
```

### 如果未安裝 Git：

1. 下載並安裝 Git: https://git-scm.com/download/win
2. 重新開啟終端機
3. 執行上述腳本

## 方法 2: 手動執行指令

### 步驟 1: 安裝 Git（如果還沒安裝）
下載: https://git-scm.com/download/win

### 步驟 2: 在專案目錄執行

```bash
# 初始化
git init

# 添加文件
git add .

# 提交
git commit -m "初始提交: 實作 Wazuh 威脅獵捕代理程式"

# 連接 GitHub（先建立倉庫）
git remote add origin https://github.com/kuobrian0102/wazuh_hunter_agent.git

# 設置主分支
git branch -M main

# 推送
git push -u origin main
```

## 步驟 3: 在 GitHub 建立倉庫

1. 前往: https://github.com/new
2. Repository name: `wazuh_hunter_agent`
3. Description: `可離線分析 Wazuh Alerts 的 Python 威脅獵捕代理程式`
4. 選擇 **Public** 或 **Private**
5. **不要**勾選 "Initialize this repository with a README"
6. 點擊 **Create repository**

## 步驟 4: 認證（推送時需要）

### 選項 A: Personal Access Token（推薦）

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. 選擇權限: `repo` (全部)
4. 生成並複製 token
5. 推送時，用戶名輸入 `kuobrian0102`，密碼輸入 token

### 選項 B: GitHub CLI

```bash
# 安裝 GitHub CLI
winget install GitHub.cli

# 登入
gh auth login

# 然後就可以直接推送
git push -u origin main
```

## 完成後

推送成功後，前往 https://github.com/kuobrian0102/wazuh_hunter_agent 查看你的倉庫！

GitHub Actions 會自動執行 CI 測試。



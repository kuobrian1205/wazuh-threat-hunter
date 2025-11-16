# 如何將專案上傳到 GitHub

## 前置需求

1. **安裝 Git**
   - 下載：https://git-scm.com/download/win
   - 安裝後重新開啟終端機

2. **建立 GitHub 帳號**
   - 前往：https://github.com
   - 註冊並登入

## 步驟 1: 初始化 Git 倉庫

在專案目錄中執行：

```bash
# 初始化 Git 倉庫
git init

# 設定使用者資訊（如果還沒設定過）
git config --global user.name "你的名字"
git config --global user.email "你的email@example.com"
```

## 步驟 2: 添加文件並提交

```bash
# 查看有哪些文件會被加入
git status

# 添加所有文件
git add .

# 提交（第一次提交）
git commit -m "初始提交: 實作 Wazuh 威脅獵捕代理程式"
```

## 步驟 3: 在 GitHub 建立新倉庫

1. 登入 GitHub
2. 點擊右上角的 **+** → **New repository**
3. 填寫資訊：
   - Repository name: `wazuh_hunter_agent`（或你喜歡的名稱）
   - Description: `可離線分析 Wazuh Alerts 的 Python 威脅獵捕代理程式`
   - 選擇 **Public** 或 **Private**
   - **不要**勾選 "Initialize this repository with a README"（因為我們已經有文件了）
4. 點擊 **Create repository**

## 步驟 4: 連接本地倉庫到 GitHub

GitHub 會顯示指令，執行：

```bash
# 添加遠端倉庫（將 YOUR_USERNAME 和 REPO_NAME 替換成你的）
git remote add origin https://github.com/YOUR_USERNAME/wazuh_hunter_agent.git

# 或使用 SSH（如果你有設定 SSH key）
# git remote add origin git@github.com:YOUR_USERNAME/wazuh_hunter_agent.git

# 查看遠端倉庫設定
git remote -v
```

## 步驟 5: 推送程式碼到 GitHub

```bash
# 推送主分支到 GitHub
git branch -M main
git push -u origin main
```

如果使用 `master` 分支：
```bash
git branch -M master
git push -u origin master
```

## 步驟 6: 驗證

前往你的 GitHub 倉庫頁面，應該可以看到所有文件都已經上傳了！

## 後續更新

之後如果有修改，使用以下指令更新：

```bash
# 查看修改
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "描述你的修改"

# 推送到 GitHub
git push
```

## 建立 Pull Request (PR)

如果這是作業或協作專案：

1. 在 GitHub 上點擊 **Pull requests** 標籤
2. 點擊 **New pull request**
3. 選擇你的分支
4. 填寫 PR 描述
5. 提交 PR

CI 會自動執行測試！

## 常見問題

### Q: 推送時要求輸入帳號密碼？
A: 使用 Personal Access Token 代替密碼：
   - GitHub → Settings → Developer settings → Personal access tokens → Generate new token
   - 選擇 `repo` 權限
   - 複製 token 作為密碼使用

### Q: 如何更新 .gitignore 後忽略已追蹤的文件？
A: 
```bash
git rm -r --cached .
git add .
git commit -m "更新 .gitignore"
```

### Q: 如何查看提交歷史？
A: `git log`

### Q: 如何撤銷最後一次提交？
A: `git reset --soft HEAD~1`（保留修改）

## 快速指令參考

```bash
# 初始化
git init
git add .
git commit -m "初始提交"

# 連接 GitHub
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 推送
git branch -M main
git push -u origin main
```


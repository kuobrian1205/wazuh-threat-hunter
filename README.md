# Wazuh 威脅獵捕代理程式

一個可離線分析 Wazuh Alerts 的 Python 威脅獵捕代理程式，用於檢測可疑行為和安全威脅。

## 功能特色

- 📊 **離線分析**：無需連接 Wazuh 伺服器，可直接分析本地 JSON 格式的 alerts
- 🔍 **多種威脅檢測**：
  - 可疑 IP 地址檢測
  - 暴力破解嘗試檢測
  - 權限提升嘗試檢測
  - 異常用戶行為檢測
  - 高風險規則觸發檢測
- 📈 **數據分析**：使用 pandas 進行高效的數據分析和統計
- ✅ **完整測試**：包含完整的單元測試，確保程式碼品質

## 安裝

### 需求

- Python 3.9+
- pip

### 安裝步驟

1. 克隆專案：
```bash
git clone <repository-url>
cd wazuh_hunter_agent
```

2. 建立虛擬環境（建議）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```python
from src.hunter import hunt_threats

# 分析指定目錄中的 Wazuh alerts
result = hunt_threats('data/')

# 查看摘要
print(result['summary'])

# 查看發現的威脅
for finding in result['findings']:
    print(finding)
```

### 進階使用

```python
from src.hunter import ThreatHunter
from src.data_loader import load_alerts

# 載入 alerts
alerts = load_alerts('data/')

# 創建威脅獵捕代理程式
hunter = ThreatHunter(alerts)

# 執行分析
findings = hunter.analyze()

# 獲取摘要
summary = hunter.get_summary()
print(summary)
```

## 數據格式

Wazuh alerts 應為 JSON Lines 格式（每行一個 JSON 物件），範例：

```json
{"timestamp": "2024-06-01T08:15:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"}
{"timestamp": "2024-06-01T09:10:32Z", "rule": {"id": "5503"}, "srcip": "192.168.1.45", "user": "bob"}
```

## 測試

執行所有測試：

```bash
pytest tests/ -v
```

執行特定測試：

```bash
pytest tests/test_hunter.py -v
pytest tests/test_data_loader.py -v
```

## 專案結構

```
wazuh_hunter_agent/
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # 載入 Wazuh alerts
│   └── hunter.py           # 威脅獵捕核心邏輯
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py # 數據載入測試
│   ├── test_hunter.py      # 威脅獵捕測試
│   └── test_a.py           # 額外測試
├── data/
│   └── sample_alerts.json  # 範例數據
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI 配置
├── requirements.txt        # Python 依賴
└── README.md              # 本文件
```

## CI/CD

專案使用 GitHub Actions 進行持續整合，支援多個 Python 版本（3.9, 3.10, 3.11, 3.12）。

CI 會自動執行：
- 單元測試
- 程式碼覆蓋率檢查

## 威脅檢測類型

### 1. 可疑 IP 檢測 (suspicious_ip)
- 檢測來自 localhost 但非系統用戶的活動
- 檢測大量來自私有 IP 的活動

### 2. 暴力破解檢測 (potential_brute_force)
- 檢測同一 IP 對同一用戶的多次登入嘗試（≥3 次）

### 3. 權限提升檢測 (privileged_user_activity)
- 檢測 admin、root、administrator 等特權用戶的活動

### 4. 異常用戶行為 (anomalous_user_behavior)
- 檢測活動次數異常高的用戶（超過平均值 2 倍）

### 5. 高風險規則 (high_risk_rule_triggered)
- 檢測觸發高風險安全規則的 alerts（如規則 ID: 1002, 31104）

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 授權

[請在此添加授權資訊]

## 作者

[請在此添加作者資訊]



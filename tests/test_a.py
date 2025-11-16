import os
import tempfile
import json
from src.data_loader import load_alerts

def test_load_alerts_empty_directory():
    """測試空目錄的情況"""
    with tempfile.TemporaryDirectory() as temp_dir:
        alerts = load_alerts(temp_dir)
        assert isinstance(alerts, list)
        assert len(alerts) == 0

def test_load_alerts_multiple_files():
    """測試從多個檔案載入警報"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # 建立第一個測試檔案
        file1_path = os.path.join(temp_dir, "alerts1.json")
        alert1 = {"timestamp": "2024-06-01T08:15:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"}
        with open(file1_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(alert1) + "\n")
        
        # 建立第二個測試檔案
        file2_path = os.path.join(temp_dir, "alerts2.json")
        alert2 = {"timestamp": "2024-06-01T09:10:32Z", "rule": {"id": "5503"}, "srcip": "192.168.1.45", "user": "bob"}
        with open(file2_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(alert2) + "\n")
        
        alerts = load_alerts(temp_dir)
        assert isinstance(alerts, list)
        assert len(alerts) == 2
        assert alerts[0]["user"] == "alice"
        assert alerts[1]["user"] == "bob"


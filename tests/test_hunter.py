"""
威脅獵捕代理程式的測試
"""
import os
import tempfile
import json
import pytest
from src.hunter import ThreatHunter, hunt_threats


def test_threat_hunter_empty_alerts():
    """測試空 alerts 的情況"""
    hunter = ThreatHunter([])
    findings = hunter.analyze()
    assert findings == []
    summary = hunter.get_summary()
    assert summary['total_alerts'] == 0
    assert summary['total_findings'] == 0


def test_threat_hunter_suspicious_ip():
    """測試可疑 IP 檢測"""
    alerts = [
        {"timestamp": "2024-06-01T08:15:00Z", "rule": {"id": "5503"}, "srcip": "127.0.0.1", "user": "alice"},
        {"timestamp": "2024-06-01T09:10:32Z", "rule": {"id": "5503"}, "srcip": "127.0.0.1", "user": "bob"}
    ]
    hunter = ThreatHunter(alerts)
    findings = hunter.analyze()
    
    # 應該檢測到可疑 IP
    suspicious_ip_findings = [f for f in findings if f['type'] == 'suspicious_ip']
    assert len(suspicious_ip_findings) > 0


def test_threat_hunter_brute_force():
    """測試暴力破解檢測"""
    alerts = [
        {"timestamp": "2024-06-01T08:15:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"},
        {"timestamp": "2024-06-01T08:16:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"},
        {"timestamp": "2024-06-01T08:17:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"},
        {"timestamp": "2024-06-01T08:18:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"}
    ]
    hunter = ThreatHunter(alerts)
    findings = hunter.analyze()
    
    # 應該檢測到可能的暴力破解
    brute_force_findings = [f for f in findings if f['type'] == 'potential_brute_force']
    assert len(brute_force_findings) > 0


def test_threat_hunter_privilege_escalation():
    """測試權限提升檢測"""
    alerts = [
        {"timestamp": "2024-06-01T08:15:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "admin"},
        {"timestamp": "2024-06-01T09:10:32Z", "rule": {"id": "5503"}, "srcip": "192.168.1.45", "user": "root"}
    ]
    hunter = ThreatHunter(alerts)
    findings = hunter.analyze()
    
    # 應該檢測到特權用戶活動
    privilege_findings = [f for f in findings if f['type'] == 'privileged_user_activity']
    assert len(privilege_findings) > 0


def test_threat_hunter_high_risk_rules():
    """測試高風險規則檢測"""
    alerts = [
        {"timestamp": "2024-06-01T08:15:00Z", "rule": {"id": "1002"}, "srcip": "192.168.1.23", "user": "alice"},
        {"timestamp": "2024-06-01T09:10:32Z", "rule": {"id": "31104"}, "srcip": "192.168.1.45", "user": "bob"}
    ]
    hunter = ThreatHunter(alerts)
    findings = hunter.analyze()
    
    # 應該檢測到高風險規則
    high_risk_findings = [f for f in findings if f['type'] == 'high_risk_rule_triggered']
    assert len(high_risk_findings) > 0


def test_threat_hunter_anomalous_behavior():
    """測試異常用戶行為檢測"""
    alerts = []
    # 創建一個異常活躍的用戶（20 筆記錄）
    for i in range(20):
        alerts.append({
            "timestamp": f"2024-06-01T08:{i:02d}:00Z",
            "rule": {"id": "5503"},
            "srcip": "192.168.1.23",
            "user": "suspicious_user"
        })
    # 其他用戶各 1 筆
    alerts.append({"timestamp": "2024-06-01T09:00:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.45", "user": "normal_user1"})
    alerts.append({"timestamp": "2024-06-01T09:01:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.46", "user": "normal_user2"})
    
    hunter = ThreatHunter(alerts)
    findings = hunter.analyze()
    
    # 應該檢測到異常用戶行為
    anomalous_findings = [f for f in findings if f['type'] == 'anomalous_user_behavior']
    assert len(anomalous_findings) > 0


def test_hunt_threats_function():
    """測試 hunt_threats 函數"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # 建立測試檔案
        file_path = os.path.join(temp_dir, "alerts.json")
        alert1 = {"timestamp": "2024-06-01T08:15:00Z", "rule": {"id": "1002"}, "srcip": "127.0.0.1", "user": "admin"}
        alert2 = {"timestamp": "2024-06-01T09:10:32Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"}
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(alert1) + "\n")
            f.write(json.dumps(alert2) + "\n")
        
        result = hunt_threats(temp_dir)
        
        assert 'summary' in result
        assert 'findings' in result
        assert result['summary']['total_alerts'] == 2
        assert isinstance(result['findings'], list)


def test_threat_hunter_summary():
    """測試分析摘要"""
    alerts = [
        {"timestamp": "2024-06-01T08:15:00Z", "rule": {"id": "1002"}, "srcip": "127.0.0.1", "user": "admin"},
        {"timestamp": "2024-06-01T09:10:32Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"}
    ]
    hunter = ThreatHunter(alerts)
    hunter.analyze()
    summary = hunter.get_summary()
    
    assert summary['total_alerts'] == 2
    assert 'findings_by_severity' in summary
    assert 'findings_by_type' in summary
    assert isinstance(summary['findings_by_severity'], dict)
    assert isinstance(summary['findings_by_type'], dict)


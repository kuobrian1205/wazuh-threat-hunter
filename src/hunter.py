"""
Wazuh 威脅獵捕代理程式
用於離線分析 Wazuh Alerts 並檢測可疑行為
"""
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from src.data_loader import load_alerts


class ThreatHunter:
    """威脅獵捕代理程式主類別"""
    
    def __init__(self, alerts: List[Dict[str, Any]]):
        """
        初始化威脅獵捕代理程式
        
        Args:
            alerts: Wazuh alerts 列表
        """
        self.alerts = alerts
        self.df = None
        self.findings = []
        
    def analyze(self) -> List[Dict[str, Any]]:
        """
        執行威脅獵捕分析
        
        Returns:
            發現的威脅列表
        """
        if not self.alerts:
            return []
        
        # 將 alerts 轉換為 DataFrame 以便分析
        self.df = pd.DataFrame(self.alerts)
        
        # 執行各種威脅檢測
        self._detect_suspicious_ips()
        self._detect_brute_force_attempts()
        self._detect_privilege_escalation()
        self._detect_anomalous_user_behavior()
        self._detect_high_risk_rules()
        
        return self.findings
    
    def _detect_suspicious_ips(self):
        """檢測可疑 IP 地址"""
        if 'srcip' not in self.df.columns:
            return
        
        # 檢測來自 localhost 但非系統用戶的活動
        localhost_alerts = self.df[
            (self.df['srcip'] == '127.0.0.1') & 
            (self.df['user'] != 'www-data')
        ]
        
        if len(localhost_alerts) > 0:
            self.findings.append({
                'type': 'suspicious_ip',
                'severity': 'medium',
                'description': f'檢測到來自 localhost 的可疑活動 ({len(localhost_alerts)} 筆)',
                'count': len(localhost_alerts),
                'details': localhost_alerts[['timestamp', 'srcip', 'user', 'rule']].to_dict('records')
            })
        
        # 檢測來自私有 IP 範圍的異常活動
        private_ip_ranges = ['10.', '172.16.', '192.168.']
        private_alerts = self.df[
            self.df['srcip'].str.startswith(tuple(private_ip_ranges), na=False)
        ]
        
        if len(private_alerts) > 10:
            self.findings.append({
                'type': 'excessive_private_ip_activity',
                'severity': 'low',
                'description': f'檢測到大量來自私有 IP 的活動 ({len(private_alerts)} 筆)',
                'count': len(private_alerts)
            })
    
    def _detect_brute_force_attempts(self):
        """檢測暴力破解嘗試"""
        if 'user' not in self.df.columns or 'srcip' not in self.df.columns:
            return
        
        # 統計每個 IP 對每個用戶的嘗試次數
        user_ip_counts = self.df.groupby(['srcip', 'user']).size()
        
        # 檢測同一 IP 對同一用戶的多次嘗試（可能是暴力破解）
        suspicious_attempts = user_ip_counts[user_ip_counts >= 3]
        
        if len(suspicious_attempts) > 0:
            self.findings.append({
                'type': 'potential_brute_force',
                'severity': 'high',
                'description': f'檢測到可能的暴力破解嘗試 ({len(suspicious_attempts)} 個 IP-用戶組合)',
                'count': len(suspicious_attempts),
                'details': suspicious_attempts.to_dict()
            })
    
    def _detect_privilege_escalation(self):
        """檢測權限提升嘗試"""
        if 'user' not in self.df.columns:
            return
        
        # 檢測 admin 或 root 用戶的活動
        admin_users = ['admin', 'root', 'administrator']
        admin_alerts = self.df[self.df['user'].isin(admin_users)]
        
        if len(admin_alerts) > 0:
            self.findings.append({
                'type': 'privileged_user_activity',
                'severity': 'medium',
                'description': f'檢測到特權用戶活動 ({len(admin_alerts)} 筆)',
                'count': len(admin_alerts),
                'users': admin_alerts['user'].unique().tolist()
            })
    
    def _detect_anomalous_user_behavior(self):
        """檢測異常用戶行為"""
        if 'user' not in self.df.columns or 'timestamp' not in self.df.columns:
            return
        
        # 統計每個用戶的活動次數
        user_counts = self.df['user'].value_counts()
        
        # 檢測異常活躍的用戶（活動次數超過平均值的 2 倍，且至少需要 2 個不同的用戶）
        if len(user_counts) >= 2:
            mean_activity = user_counts.mean()
            threshold = mean_activity * 2
            
            anomalous_users = user_counts[user_counts > threshold]
            
            if len(anomalous_users) > 0:
                self.findings.append({
                    'type': 'anomalous_user_behavior',
                    'severity': 'medium',
                    'description': f'檢測到異常活躍的用戶 ({len(anomalous_users)} 個)',
                    'count': len(anomalous_users),
                    'users': anomalous_users.to_dict()
                })
    
    def _detect_high_risk_rules(self):
        """檢測高風險規則"""
        if 'rule' not in self.df.columns:
            return
        
        # 提取規則 ID
        rule_ids = self.df['rule'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
        
        # 定義高風險規則 ID（這些是常見的安全相關規則）
        high_risk_rules = ['1002', '31104']  # 可以根據實際需求擴展
        
        high_risk_alerts = self.df[rule_ids.isin(high_risk_rules)]
        
        if len(high_risk_alerts) > 0:
            self.findings.append({
                'type': 'high_risk_rule_triggered',
                'severity': 'high',
                'description': f'檢測到高風險規則觸發 ({len(high_risk_alerts)} 筆)',
                'count': len(high_risk_alerts),
                'rule_ids': rule_ids[rule_ids.isin(high_risk_rules)].unique().tolist()
            })
    
    def get_summary(self) -> Dict[str, Any]:
        """
        獲取分析摘要
        
        Returns:
            分析摘要字典
        """
        if not self.df is None and len(self.df) > 0:
            return {
                'total_alerts': len(self.alerts),
                'total_findings': len(self.findings),
                'findings_by_severity': self._count_by_severity(),
                'findings_by_type': self._count_by_type()
            }
        return {
            'total_alerts': 0,
            'total_findings': 0,
            'findings_by_severity': {},
            'findings_by_type': {}
        }
    
    def _count_by_severity(self) -> Dict[str, int]:
        """統計各嚴重程度的發現數量"""
        severity_counts = {}
        for finding in self.findings:
            severity = finding.get('severity', 'unknown')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        return severity_counts
    
    def _count_by_type(self) -> Dict[str, int]:
        """統計各類型的發現數量"""
        type_counts = {}
        for finding in self.findings:
            finding_type = finding.get('type', 'unknown')
            type_counts[finding_type] = type_counts.get(finding_type, 0) + 1
        return type_counts


def hunt_threats(directory_path: str) -> Dict[str, Any]:
    """
    從目錄載入 alerts 並執行威脅獵捕分析
    
    Args:
        directory_path: 包含 Wazuh alerts JSON 文件的目錄路徑
        
    Returns:
        包含分析結果和發現的字典
    """
    # 載入 alerts
    alerts = load_alerts(directory_path)
    
    # 創建威脅獵捕代理程式並執行分析
    hunter = ThreatHunter(alerts)
    findings = hunter.analyze()
    summary = hunter.get_summary()
    
    return {
        'summary': summary,
        'findings': findings
    }


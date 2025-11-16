#!/usr/bin/env python3
"""
Wazuh 威脅獵捕代理程式使用範例
"""
import json
from src.hunter import hunt_threats, ThreatHunter
from src.data_loader import load_alerts


def example_1_simple_usage():
    """範例 1: 最簡單的使用方式"""
    print("=" * 60)
    print("範例 1: 簡單使用 - 直接分析目錄")
    print("=" * 60)
    
    # 分析 data/ 目錄中的 alerts
    result = hunt_threats('data/')
    
    # 顯示摘要
    print("\n[分析摘要]")
    print(json.dumps(result['summary'], indent=2, ensure_ascii=False))
    
    # 顯示發現的威脅
    print(f"\n[發現 {len(result['findings'])} 個威脅]")
    for i, finding in enumerate(result['findings'], 1):
        print(f"\n{i}. {finding['type']} (嚴重程度: {finding['severity']})")
        print(f"   描述: {finding['description']}")
        if 'count' in finding:
            print(f"   數量: {finding['count']}")


def example_2_advanced_usage():
    """範例 2: 進階使用方式"""
    print("\n" + "=" * 60)
    print("範例 2: 進階使用 - 自訂分析")
    print("=" * 60)
    
    # 載入 alerts
    alerts = load_alerts('data/')
    print(f"\n[載入了 {len(alerts)} 筆 alerts]")
    
    # 創建威脅獵捕代理程式
    hunter = ThreatHunter(alerts)
    
    # 執行分析
    findings = hunter.analyze()
    
    # 獲取摘要
    summary = hunter.get_summary()
    
    # 顯示詳細資訊
    print("\n[分析摘要]")
    print(f"  總 alerts 數: {summary['total_alerts']}")
    print(f"  發現威脅數: {summary['total_findings']}")
    print(f"  按嚴重程度分類: {summary['findings_by_severity']}")
    print(f"  按類型分類: {summary['findings_by_type']}")
    
    # 顯示每個發現的詳細資訊
    if findings:
        print("\n[詳細發現]")
        for i, finding in enumerate(findings, 1):
            print(f"\n  {i}. 【{finding['type']}】")
            print(f"     嚴重程度: {finding['severity']}")
            print(f"     描述: {finding['description']}")
            if 'details' in finding:
                print(f"     詳細資訊: {len(finding['details'])} 筆記錄")


def example_3_custom_alerts():
    """範例 3: 使用自訂 alerts"""
    print("\n" + "=" * 60)
    print("範例 3: 自訂 alerts 分析")
    print("=" * 60)
    
    # 創建自訂 alerts
    custom_alerts = [
        {"timestamp": "2024-06-01T08:15:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"},
        {"timestamp": "2024-06-01T08:16:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"},
        {"timestamp": "2024-06-01T08:17:00Z", "rule": {"id": "5503"}, "srcip": "192.168.1.23", "user": "alice"},
        {"timestamp": "2024-06-01T08:18:00Z", "rule": {"id": "1002"}, "srcip": "127.0.0.1", "user": "admin"}
    ]
    
    print(f"\n[使用 {len(custom_alerts)} 筆自訂 alerts]")
    
    # 分析
    hunter = ThreatHunter(custom_alerts)
    findings = hunter.analyze()
    
    print(f"\n[發現 {len(findings)} 個威脅]")
    for finding in findings:
        print(f"  - {finding['type']}: {finding['description']}")


if __name__ == "__main__":
    import sys
    import io
    # 設定 UTF-8 編碼以支援中文和特殊字符
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("Wazuh 威脅獵捕代理程式使用範例\n")
    
    # 執行範例
    example_1_simple_usage()
    example_2_advanced_usage()
    example_3_custom_alerts()
    
    print("\n" + "=" * 60)
    print("範例執行完成！")
    print("=" * 60)


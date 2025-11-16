#!/usr/bin/env python3
"""
Wazuh 威脅獵捕代理程式 - 命令列執行腳本
用法: python run_hunter.py [目錄路徑]
"""
import sys
import json
from src.hunter import hunt_threats


def main():
    # 取得目錄路徑（預設為 data/）
    directory = sys.argv[1] if len(sys.argv) > 1 else 'data/'
    
    print(f"正在分析目錄: {directory}")
    print("=" * 60)
    
    try:
        # 執行威脅獵捕分析
        result = hunt_threats(directory)
        
        # 顯示摘要
        summary = result['summary']
        print(f"\n[分析結果]")
        print(f"總 alerts 數: {summary['total_alerts']}")
        print(f"發現威脅數: {summary['total_findings']}")
        
        if summary['findings_by_severity']:
            print(f"\n[按嚴重程度分類]")
            for severity, count in summary['findings_by_severity'].items():
                print(f"  {severity}: {count} 個")
        
        if summary['findings_by_type']:
            print(f"\n[按類型分類]")
            for ftype, count in summary['findings_by_type'].items():
                print(f"  {ftype}: {count} 個")
        
        # 顯示發現的威脅
        findings = result['findings']
        if findings:
            print(f"\n[詳細威脅列表]")
            print("=" * 60)
            for i, finding in enumerate(findings, 1):
                print(f"\n{i}. 【{finding['type']}】")
                print(f"   嚴重程度: {finding['severity']}")
                print(f"   描述: {finding['description']}")
                if 'count' in finding:
                    print(f"   數量: {finding['count']}")
                if 'details' in finding and finding['details']:
                    print(f"   詳細記錄數: {len(finding['details'])}")
        else:
            print("\n[未發現威脅]")
        
        print("\n" + "=" * 60)
        print("分析完成！")
        
    except Exception as e:
        print(f"\n[錯誤] 執行失敗: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()



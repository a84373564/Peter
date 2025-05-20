# eco_sandbox_reporter.py - 沙盤模擬報表整合器（從 sandbox_results 讀取）

import os
import json

RESULT_DIR = "/mnt/data/Peter/sandbox_results"

def load_results():
    records = []
    for file in os.listdir(RESULT_DIR):
        if not file.endswith(".json"):
            continue
        path = os.path.join(RESULT_DIR, file)
        try:
            with open(path, "r") as f:
                result = json.load(f)
                records.append({
                    "name": file,
                    "symbol": result.get("symbol", "N/A"),
                    "profit": result.get("profit", 0),
                    "drawdown": result.get("max_drawdown", 0),
                    "loss_trades": result.get("loss_trades", 0),
                    "pass": result.get("sandbox_pass", False)
                })
        except:
            continue
    return records

def print_report(records):
    print("=== 沙盤模擬總結（模組排行）===\n")
    sorted_records = sorted(records, key=lambda x: x["profit"], reverse=True)
    for i, r in enumerate(sorted_records, 1):
        status = "✓" if r["pass"] else "x"
        print(f"{i:>2}. {r['name']:<30}｜{r['symbol']:>8}｜獲利: {r['profit']:>6.2f}｜DD: {r['drawdown']:<5.2f}｜虧損: {r['loss_trades']}｜結果: {status}")

if __name__ == "__main__":
    results = load_results()
    if not results:
        print("[!] 找不到任何沙盤結果（sandbox_results 為空）")
    else:
        print_report(results)

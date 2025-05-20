# eco_sandbox_reporter.py - 王者沙盤報表升級版（只顯示 elite_pool Top 10）

import os
import json

RESULT_DIR = "/mnt/data/Peter/sandbox_results"
ELITE_PATH = "/mnt/data/Peter/elite_pool.json"

def load_elite_names():
    if not os.path.exists(ELITE_PATH):
        return []
    with open(ELITE_PATH, "r") as f:
        data = json.load(f)
    return [m["name"] for m in data if "name" in m]

def load_results():
    records = []
    elite_names = load_elite_names()
    for file in os.listdir(RESULT_DIR):
        if not file.endswith(".json") or file not in elite_names:
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
                    "rounds": result.get("rounds", 0),
                    "win_rate": result.get("win_rate", 0),
                    "pass": result.get("sandbox_pass", False)
                })
        except:
            continue
    return records

def print_report(records):
    print("=== 王者沙盤模擬報表（只列 elite_pool Top 10）===\n")
    sorted_records = sorted(records, key=lambda x: x["profit"], reverse=True)[:10]
    for i, r in enumerate(sorted_records, 1):
        status = "✓" if r["pass"] else "x"
        print(f"{i:>2}. {r['name']:<32}｜{r['symbol']:<10}｜獲利: {r['profit']:>6.2f}｜DD: {r['drawdown']:<5.2f}｜勝率: {r['win_rate']*100:>5.1f}%｜虧損: {r['loss_trades']}｜回合: {r['rounds']}｜{status}")

if __name__ == "__main__":
    results = load_results()
    if not results:
        print("[!] 找不到任何沙盤結果（或 elite_pool 為空）")
    else:
        print_report(results)

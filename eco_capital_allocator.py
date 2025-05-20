# eco_sandbox_reporter.py - 沙盤模擬報表整合器

import os
import json

MODULE_DIR = "/mnt/data/Peter/modules"

def extract_sandbox(mod):
    result = mod.get("sandbox_result", {})
    return {
        "name": mod.get("name", "N/A"),
        "symbol": mod.get("symbol", "N/A"),
        "profit": result.get("total_profit", 0),
        "win_rate": result.get("win_rate", 0),
        "rounds": result.get("rounds", 0)
    }

def load_modules():
    records = []
    for file in os.listdir(MODULE_DIR):
        if not file.endswith(".json"):
            continue
        path = os.path.join(MODULE_DIR, file)
        try:
            with open(path, "r") as f:
                mod = json.load(f)
                if "sandbox_result" in mod:
                    records.append(extract_sandbox(mod))
        except:
            continue
    return records

def print_report(records):
    print("=== 沙盤模擬總結（模組排行）===\n")
    sorted_records = sorted(records, key=lambda x: x["profit"], reverse=True)
    for i, r in enumerate(sorted_records, 1):
        print(f"{i:>2}. {r['name']}｜{r['symbol']:>8}｜獲利: {r['profit']:>6.2f} USDT｜勝率: {r['win_rate']*100:>5.1f}%｜回合數: {r['rounds']}")

if __name__ == "__main__":
    modules = load_modules()
    if not modules:
        print("[!] 找不到任何含 sandbox_result 的模組。")
    else:
        print_report(modules)

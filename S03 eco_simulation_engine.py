# Peter Project - S03 模擬引擎 eco_simulation_engine.py

import os
import json
import random

MODULE_DIR = "/mnt/data/Peter/modules"

def simulate_module(module):
    # 模擬邏輯（目前為簡化版，後續可接真實歷史數據）
    result = {
        "win_rate": round(random.uniform(0.4, 0.9), 3),
        "profit": round(random.uniform(-10, 30), 2),
        "sharpe": round(random.uniform(0.1, 3.5), 3),
        "drawdown": round(random.uniform(0.5, 5.0), 2)
    }
    result["score"] = round(result["win_rate"] * 20 + result["sharpe"] * 10 - result["drawdown"], 2)

    # 模擬歷史交易紀錄
    history = [{"entry": "2024-01-01", "exit": "2024-01-05", "profit": result["profit"] / 3} for _ in range(3)]

    return result, history

def process_module_file(file_path):
    with open(file_path, "r") as f:
        mod = json.load(f)

    result, history = simulate_module(mod)

    mod.update(result)
    mod["history"] = history
    mod["score"] = result["score"]

    with open(file_path, "w") as f:
        json.dump(mod, f, indent=2)

    print(f"[✓] 模擬完成：{os.path.basename(file_path)}｜Score = {mod['score']}")

def main():
    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for file in files:
        process_module_file(os.path.join(MODULE_DIR, file))

if __name__ == "__main__":
    main()

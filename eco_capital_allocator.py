# S12 - 資金分配模組 eco_capital_allocator.py

import os
import json

MODULE_DIR = "/mnt/data/Peter/modules"
LOG_PATH = "/mnt/data/Peter/logs/s12_allocator.log"

# 分級對照表
ALLOC_MAP = {
    "A+": 250,
    "A": 150,
    "B": 100,
    "C": 30,
    "F": 0
}

def classify(score, sharpe, drawdown):
    if score >= 35 and sharpe >= 2.0 and drawdown <= 2:
        return "A+"
    elif score >= 25 and sharpe >= 1.5 and drawdown <= 3:
        return "A"
    elif score >= 15 and sharpe >= 1.0:
        return "B"
    elif score >= 8:
        return "C"
    else:
        return "F"

def process_module(path):
    with open(path, "r") as f:
        mod = json.load(f)

    score = mod.get("score", 0)
    sharpe = mod.get("sharpe", 0)
    drawdown = mod.get("drawdown", 10)
    classification = classify(score, sharpe, drawdown)
    new_capital = ALLOC_MAP[classification]

    mod["capital"] = new_capital
    mod.setdefault("log", []).append(f"[S12] 分級 {classification} → 資金 {new_capital}")

    with open(path, "w") as f:
        json.dump(mod, f, indent=2)

    return mod["name"], classification, new_capital

def run_allocation():
    os.makedirs(MODULE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    result_lines = []

    for file in os.listdir(MODULE_DIR):
        if not file.endswith(".json"):
            continue
        path = os.path.join(MODULE_DIR, file)
        try:
            name, level, capital = process_module(path)
            result_lines.append(f"{name} → {level} → {capital}")
        except Exception as e:
            result_lines.append(f"[!] 失敗：{file} → {e}")

    with open(LOG_PATH, "w") as logf:
        logf.write("\n".join(result_lines))

if __name__ == "__main__":
    run_allocation()

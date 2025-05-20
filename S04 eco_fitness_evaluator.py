# Peter Project - S04 模組適應度評估器 eco_fitness_evaluator.py

import os
import json

MODULE_DIR = "/mnt/data/Peter/modules"

def evaluate_module(mod):
    try:
        score = mod.get("score", None)
        sharpe = mod.get("sharpe", None)
        drawdown = mod.get("drawdown", None)

        if score is None or sharpe is None or drawdown is None:
            return "[!] 缺乏評估指標，跳過"

        if score < 10 or sharpe < 0.5 or drawdown > 5.0:
            mod["genetics"]["lifespan"] = 0
            return "[X] 淘汰（低績效 or 高風險）"
        else:
            return "[✓] 通過，進入下一階段"

    except Exception as e:
        return f"[!] 模組錯誤：{e}"

def process_module_file(file_path):
    with open(file_path, "r") as f:
        mod = json.load(f)

    result = evaluate_module(mod)

    with open(file_path, "w") as f:
        json.dump(mod, f, indent=2)

    print(f"{os.path.basename(file_path)} → {result}")

def main():
    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for file in files:
        process_module_file(os.path.join(MODULE_DIR, file))

if __name__ == "__main__":
    main()

# Peter Project - S02 模組建構者 eco_module_builder.py

import os
import json
import random
from datetime import datetime

TASK_PATH = "/mnt/data/Peter/task_spec.json"
OUTPUT_DIR = "/mnt/data/Peter/modules"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_task():
    with open(TASK_PATH, "r") as f:
        return json.load(f)

def create_module(symbol, capital, lineage_tag):
    timestamp = int(datetime.utcnow().timestamp())
    module_name = f"mod_{symbol}_{timestamp}.json"
    module_path = os.path.join(OUTPUT_DIR, module_name)

    module = {
        "name": module_name,
        "symbol": symbol,
        "capital": capital,
        "run": {
            "entry_logic": "rsi < 30",
            "exit_logic": "rsi > 70"
        },
        "log": [],
        "score": None,
        "history": [],
        "genetics": {
            "lifespan": 10,
            "fitness": 0,
            "mutation_bias": round(random.uniform(0.1, 0.5), 2),
            "reproduction_chance": round(random.uniform(0.2, 0.8), 2),
            "lineage": lineage_tag
        }
    }

    with open(module_path, "w") as f:
        json.dump(module, f, indent=2)

    print(f"[✓] 模組建立完成：{module_name}")
    return module_name

def main():
    task = load_task()
    symbols = task["symbols"][:task["target_count"]]
    capital = task["max_capital"] / len(symbols)
    lineage_tag = f"L0_{task['task_id']}"

    for symbol in symbols:
        create_module(symbol, round(capital, 2), lineage_tag)

if __name__ == "__main__":
    main()

# Peter Project - S06 繁殖引擎 eco_reproduction_engine.py

import os
import json
import random
import time
from datetime import datetime

MODULE_DIR = "/mnt/data/Peter/modules"

def mutate_value(value, factor=0.1, min_val=0, max_val=1):
    delta = random.uniform(-factor, factor)
    mutated = value + delta
    return round(max(min(mutated, max_val), min_val), 2)

def generate_child(mod, child_id):
    parent_name = mod["name"]
    symbol = mod["symbol"]
    timestamp = int(time.time())
    child_name = f"mod_{symbol}_{timestamp}_{child_id}.json"
    child_path = os.path.join(MODULE_DIR, child_name)

    child = {
        "name": child_name,
        "symbol": symbol,
        "capital": mod["capital"],
        "run": mod["run"].copy(),
        "log": [],
        "score": None,
        "history": [],
        "genetics": {
            "lifespan": mutate_value(mod["genetics"]["lifespan"], 2, 5, 20),
            "fitness": 0,
            "mutation_bias": mutate_value(mod["genetics"]["mutation_bias"]),
            "reproduction_chance": mutate_value(mod["genetics"]["reproduction_chance"]),
            "lineage": f"{mod['genetics']['lineage']}→{parent_name}"
        }
    }

    with open(child_path, "w") as f:
        json.dump(child, f, indent=2)

    print(f"[+] 子代模組建立：{child_name}")
    return child_name

def reproduce_module(file_path):
    with open(file_path, "r") as f:
        mod = json.load(f)

    if mod["genetics"].get("lifespan", 0) <= 0:
        print(f"[×] {mod['name']} 已死亡，跳過")
        return

    score = mod.get("score", 0)
    chance = mod["genetics"].get("reproduction_chance", 0.5)
    if score > 15 and random.random() < chance:
        for i in range(random.randint(1, 2)):
            generate_child(mod, i+1)
    else:
        print(f"[-] 未繁殖：{mod['name']}（score={score}, chance={chance})")

def main():
    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for file in files:
        reproduce_module(os.path.join(MODULE_DIR, file))

if __name__ == "__main__":
    main()

# S12 強化版 - 極限王者制資金分配 eco_capital_allocator.py

import os
import json

MODULE_DIR = "/mnt/data/Peter/modules"
LOG_PATH = "/mnt/data/Peter/logs/s12_allocator.log"
TOTAL_CAPITAL = 70.0  # 你實際可用資金

def get_score(mod):
    return mod.get("score", -999)

def load_modules():
    modules = []
    for file in os.listdir(MODULE_DIR):
        if not file.endswith(".json"):
            continue
        path = os.path.join(MODULE_DIR, file)
        try:
            with open(path, "r") as f:
                data = json.load(f)
            modules.append((file, data))
        except:
            continue
    return modules

def assign_winner(modules):
    modules_sorted = sorted(modules, key=lambda x: get_score(x[1]), reverse=True)
    results = []

    for i, (file, mod) in enumerate(modules_sorted):
        if i == 0:
            mod["capital"] = TOTAL_CAPITAL
            msg = f"[S12] 王者 → {file} → 資金 {TOTAL_CAPITAL}"
        else:
            mod["capital"] = 0
            msg = f"[S12] 非王者 → {file} → 資金歸零"
        mod.setdefault("log", []).append(msg)

        # Save updated module
        with open(os.path.join(MODULE_DIR, file), "w") as f:
            json.dump(mod, f, indent=2)

        results.append(msg)
    return results

def run_allocator():
    os.makedirs(MODULE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    modules = load_modules()
    results = assign_winner(modules)
    with open(LOG_PATH, "w") as f:
        f.write("\n".join(results))

if __name__ == "__main__":
    run_allocator()

# Peter Project - S05 模組執行代理器 eco_execution_agent.py

import os
import json
import random
from datetime import datetime, timedelta

MODULE_DIR = "/mnt/data/Peter/modules"

def generate_fake_rsi_data(days=30):
    return [random.randint(10, 90) for _ in range(days)]

def simulate_run_logic(rsi_data, entry_cond, exit_cond):
    trades = []
    in_position = False
    entry_day = None

    for i, rsi in enumerate(rsi_data):
        if not in_position and eval(entry_cond.replace("rsi", str(rsi))):
            entry_day = i
            in_position = True
        elif in_position and eval(exit_cond.replace("rsi", str(rsi))):
            trades.append({
                "entry": f"2024-01-{str(entry_day + 1).zfill(2)}",
                "exit": f"2024-01-{str(i + 1).zfill(2)}",
                "profit": round(random.uniform(-5, 10), 2)
            })
            in_position = False
    return trades

def execute_module(file_path):
    with open(file_path, "r") as f:
        mod = json.load(f)

    if mod["genetics"].get("lifespan", 0) <= 0:
        print(f"[×] {mod['name']} 已死亡，跳過")
        return

    entry_logic = mod["run"].get("entry_logic", "rsi < 30")
    exit_logic = mod["run"].get("exit_logic", "rsi > 70")
    rsi_data = generate_fake_rsi_data()

    trades = simulate_run_logic(rsi_data, entry_logic, exit_logic)

    mod["log"].append({
        "run_time": datetime.utcnow().isoformat(),
        "entry_logic": entry_logic,
        "exit_logic": exit_logic,
        "trades": trades
    })

    with open(file_path, "w") as f:
        json.dump(mod, f, indent=2)

    print(f"[✓] 執行完畢：{mod['name']}，交易數：{len(trades)}")

def main():
    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for file in files:
        execute_module(os.path.join(MODULE_DIR, file))

if __name__ == "__main__":
    main()

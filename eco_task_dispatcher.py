# eco_task_dispatcher.py
import json
import os
import random
from datetime import datetime

# 設定輸出目錄
TASK_PATH = "/mnt/data/omega/tasks"
os.makedirs(TASK_PATH, exist_ok=True)

def generate_task_spec():
    task = {
        "timestamp": datetime.utcnow().isoformat(),
        "target_symbols": random.sample(["BTCUSDT", "ETHUSDT", "SOLUSDT", "OPUSDT", "XRPUSDT"], 3),
        "max_capital_usdt": random.randint(200, 1000),
        "volatility_threshold": round(random.uniform(1.5, 5.0), 2),
        "risk_tolerance": random.choice(["low", "medium", "high"]),
        "strategy_goal": random.choice(["short_term_profit", "controlled_drawdown", "momentum_exploit"]),
        "generation_tag": f"G{random.randint(1, 50)}"
    }

    with open(f"{TASK_PATH}/task_spec.json", "w") as f:
        json.dump(task, f, indent=2, ensure_ascii=False)

    print("[任務派送器] 已產生任務規格書：task_spec.json")

if __name__ == "__main__":
    generate_task_spec()

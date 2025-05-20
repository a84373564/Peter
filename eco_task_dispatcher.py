# eco_task_dispatcher.py
# S01：任務派遣者 – 根據資金與市場條件自動產生挑戰任務

import os
import json
import random
import requests
from datetime import datetime

KEY_PATH = "/mnt/data/hello/mexc_keys.json"
OUTPUT_PATH = "/mnt/data/hello/task_spec.json"

def get_top_symbols(limit=5):
    try:
        resp = requests.get("https://api.mexc.com/api/v3/ticker/24hr")
        data = resp.json()
        sorted_data = sorted(data, key=lambda x: float(x["quoteVolume"]), reverse=True)
        symbols = [d["symbol"] for d in sorted_data if d["symbol"].endswith("USDT")]
        return symbols[:limit]
    except Exception as e:
        print(f"[!] 抓取熱門幣失敗：{e}")
        return []

def load_capital():
    capital_path = "/mnt/data/hello/capital_tracker.json"
    try:
        with open(capital_path, "r") as f:
            return json.load(f).get("USDT", 100)
    except:
        return 100  # 預設資金

def create_task_spec():
    symbols = get_top_symbols()
    capital = load_capital()
    task = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbols": symbols,
        "max_capital": capital,
        "volatility_threshold": round(random.uniform(0.8, 1.5), 2),
        "target_count": random.randint(3, 5),
        "task_id": f"task_{int(datetime.utcnow().timestamp())}"
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(task, f, indent=2)
    print(f"[✓] 任務已建立：{OUTPUT_PATH}")
    return task

if __name__ == "__main__":
    task = create_task_spec()
    print(task)

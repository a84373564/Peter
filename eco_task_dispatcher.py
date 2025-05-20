# Peter Project - S01 任務派遣者 eco_task_dispatcher.py

import os
import json
import random
import requests
from datetime import datetime

KEY_PATH = "/mnt/data/Peter/mexc_keys.json"
OUTPUT_PATH = "/mnt/data/Peter/task_spec.json"

def get_top_symbols(limit=5):
    try:
        resp = requests.get("https://api.mexc.com/api/v3/ticker/24hr")
        data = resp.json()
        sorted_data = sorted(data, key=lambda x: float(x["quoteVolume"]), reverse=True)
        symbols = [d["symbol"] for d in sorted_data if d["symbol"].endswith("USDT")]
        return symbols[:limit]
    except Exception as e:
        print(f"[!] 熱門幣抓取失敗：{e}")
        return []

def load_capital():
    try:
        with open(KEY_PATH, "r") as f:
            keys = json.load(f)
        # 真實應用可接入 HMAC 簽名驗證，這裡簡化為手動資金
        print("[✓] 測試版本使用固定資金：70.51 USDT")
        return 70.51
    except Exception as e:
        print(f"[!] 金額讀取失敗，改用預設資金 70：{e}")
        return 70

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
    print(f"[✓] 任務建立成功：{OUTPUT_PATH}")
    return task

if __name__ == "__main__":
    task = create_task_spec()
    print(task)

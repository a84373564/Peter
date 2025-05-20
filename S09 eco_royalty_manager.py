# Peter Project - S09 王者模組管理器 eco_royalty_manager.py

import os
import json

MODULE_DIR = "/mnt/data/Peter/modules"
ELITE_PATH = "/mnt/data/Peter/elite_pool.json"

def is_elite(mod):
    return (
        mod.get("score", 0) >= 20 and
        mod.get("sharpe", 0) >= 1.0 and
        mod.get("drawdown", 10) <= 5 and
        mod.get("genetics", {}).get("lifespan", 0) > 0
    )

def process_module(file_path):
    try:
        with open(file_path, "r") as f:
            mod = json.load(f)

        if is_elite(mod):
            mod["is_elite"] = True
            with open(file_path, "w") as f:
                json.dump(mod, f, indent=2)
            return mod["name"]
        else:
            return None
    except Exception as e:
        print(f"[!] 解析失敗：{file_path} → {e}")
        return None

def main():
    elite_list = []
    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for file in files:
        result = process_module(os.path.join(MODULE_DIR, file))
        if result:
            elite_list.append(result)

    with open(ELITE_PATH, "w") as f:
        json.dump({"elite": elite_list}, f, indent=2)

    print(f"[✓] 王者模組封存完成，共 {len(elite_list)} 個 → elite_pool.json")

if __name__ == "__main__":
    main()

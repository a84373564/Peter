# Peter Project - S07 模組清理器 eco_cleaner.py

import os
import json

MODULE_DIR = "/mnt/data/Peter/modules"

def is_dead(mod):
    lifespan = mod.get("genetics", {}).get("lifespan", 1)
    return isinstance(lifespan, (int, float)) and lifespan <= 0

def is_self_destruct(mod):
    score = mod.get("score", 0)
    return isinstance(score, (int, float)) and score < -20

def is_corrupted(mod):
    score = mod.get("score", None)
    return not mod.get("history") and not mod.get("log") and score is None

def clean_module(file_path):
    try:
        with open(file_path, "r") as f:
            mod = json.load(f)

        if is_dead(mod):
            os.remove(file_path)
            print(f"[X] 清除死亡模組：{os.path.basename(file_path)}")
        elif is_self_destruct(mod):
            os.remove(file_path)
            print(f"[X] 清除自爆模組：{os.path.basename(file_path)}")
        elif is_corrupted(mod):
            os.remove(file_path)
            print(f"[X] 清除無效模組：{os.path.basename(file_path)}")
        else:
            print(f"[✓] 保留模組：{os.path.basename(file_path)}")

    except Exception as e:
        print(f"[!] 清理錯誤：{file_path} → {e}")

def main():
    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for file in files:
        clean_module(os.path.join(MODULE_DIR, file))

if __name__ == "__main__":
    main()

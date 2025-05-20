# Peter Project - S07.5 自動欄位防呆檢查器 auto_schema_guard.py

import os
import json

MODULE_DIR = "/mnt/data/Peter/modules"

required_root = ["name", "symbol", "capital", "run", "genetics"]
required_run = ["entry_logic", "exit_logic"]
required_genetics = ["lifespan", "fitness", "mutation_bias", "reproduction_chance", "lineage"]

def validate_module(mod, filename):
    errors = []

    for field in required_root:
        if field not in mod:
            errors.append(f"缺少 root 欄位：{field}")

    if "run" in mod:
        for field in required_run:
            if field not in mod["run"]:
                errors.append(f"缺少 run 欄位：{field}")

    if "genetics" in mod:
        for field in required_genetics:
            if field not in mod["genetics"]:
                errors.append(f"缺少 genetics 欄位：{field}")

    if errors:
        print(f"[!] 模組 {filename} 欄位錯誤：")
        for err in errors:
            print(f"    - {err}")
    else:
        print(f"[✓] 模組 {filename} 結構完整")

def main():
    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for file in files:
        try:
            with open(os.path.join(MODULE_DIR, file), "r") as f:
                mod = json.load(f)
            validate_module(mod, file)
        except Exception as e:
            print(f"[X] 無法解析 {file}：{e}")

if __name__ == "__main__":
    main()

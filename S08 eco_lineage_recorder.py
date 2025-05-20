import os
import json

MODULE_DIR = "/mnt/data/Peter/modules"
OUTPUT_PATH = "/mnt/data/Peter/lineage_map.json"

def extract_lineage(mod):
    return mod.get("genetics", {}).get("lineage", "unknown")

def build_lineage_map():
    lineage_map = {}

    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for file in files:
        try:
            with open(os.path.join(MODULE_DIR, file), "r") as f:
                mod = json.load(f)

            lineage = extract_lineage(mod)
            if lineage not in lineage_map:
                lineage_map[lineage] = []

            lineage_map[lineage].append(mod["name"])
        except Exception as e:
            print(f"[!] 解析錯誤：{file} → {e}")

    with open(OUTPUT_PATH, "w") as f:
        json.dump(lineage_map, f, indent=2)

    print(f"[✓] 血統地圖已建立：{OUTPUT_PATH}")
    return lineage_map

if __name__ == "__main__":
    build_lineage_map()

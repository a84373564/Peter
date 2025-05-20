# Peter Project - S10 生命週期控制器 eco_lifecycle_controller.py

import os
import json

MODULE_DIR = "/mnt/data/Peter/modules"
MAX_MODULES = 30  # 模組最大存量限制

def decay_lifespan(mod):
    if mod.get("genetics", {}).get("lifespan", 0) > 0:
        mod["genetics"]["lifespan"] -= 1
    return mod

def load_modules():
    mods = []
    for file in os.listdir(MODULE_DIR):
        if file.endswith(".json"):
            path = os.path.join(MODULE_DIR, file)
            try:
                with open(path, "r") as f:
                    mod = json.load(f)
                mod["__path"] = path
                mods.append(mod)
            except:
                print(f"[!] 讀取失敗：{file}")
    return mods

def enforce_limit(mods):
    if len(mods) <= MAX_MODULES:
        return
    sorted_mods = sorted(mods, key=lambda x: x.get("score", 0))
    to_delete = sorted_mods[:len(mods) - MAX_MODULES]
    for mod in to_delete:
        try:
            os.remove(mod["__path"])
            print(f"[X] 模組過量，刪除：{mod['name']}")
        except:
            print(f"[!] 無法刪除：{mod['name']}")

def main():
    mods = load_modules()

    for mod in mods:
        updated = decay_lifespan(mod)
        with open(mod["__path"], "w") as f:
            json.dump(updated, f, indent=2)

    enforce_limit(mods)
    print(f"[✓] S10 完成｜模組總數：{len(mods)}")

if __name__ == "__main__":
    main()

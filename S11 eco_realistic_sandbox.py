import os
import json
import random
from datetime import datetime

PRICE_DATA_PATH = "/mnt/data/Peter/prices"
MODULE_PATH = "/mnt/data/Peter/modules"
SANDBOX_RESULTS_PATH = "/mnt/data/Peter/sandbox_results"
os.makedirs(SANDBOX_RESULTS_PATH, exist_ok=True)

INITIAL_CAPITAL = 70.0
MAX_POSITION_RATIO = 0.5
FEE_RATIO = 0.0015
SLIPPAGE_RATIO = 0.002
MAX_DRAWDOWN_THRESHOLD = 0.25
MAX_LOSS_TRADES = 3

def simulate_trade(action, price, capital, position):
    effective_price = price * (1 + SLIPPAGE_RATIO if action == "buy" else 1 - SLIPPAGE_RATIO)
    fee = effective_price * FEE_RATIO
    if action == "buy":
        qty = (capital * MAX_POSITION_RATIO) / effective_price
        cost = qty * effective_price + fee
        if cost > capital:
            return capital, position, "fail"
        capital -= cost
        position += qty
    elif action == "sell" and position > 0:
        revenue = position * effective_price - fee
        capital += revenue
        position = 0
    return capital, position, "ok"

def evaluate_module(mod_file):
    with open(os.path.join(MODULE_PATH, mod_file), "r") as f:
        code = compile(f.read(), mod_file, 'exec')
        mod_namespace = {}
        exec(code, mod_namespace)
        mod = mod_namespace.get("mod")

    if not mod or not hasattr(mod, "run"):
        return {"error": "invalid module"}

    history = []
    capital = INITIAL_CAPITAL
    position = 0.0
    equity_curve = []
    loss_count = 0
    peak_equity = capital
    max_drawdown = 0.0

    symbol = getattr(mod, "symbol", "TEST")
    price_file = f"{symbol}.json"
    try:
        with open(os.path.join(PRICE_DATA_PATH, price_file), "r") as f:
            price_data = json.load(f)
    except:
        return {"error": "no price data"}

    sample_prices = price_data[-30:]  # last 30 bars

    for bar in sample_prices:
        price = bar["close"]
        result = mod.run([bar], capital, history)

        action = result.get("action", "")
        if action in ("buy", "sell"):
            capital, position, status = simulate_trade(action, price, capital, position)
            if status == "fail":
                continue

        equity = capital + position * price
        equity_curve.append(equity)
        history.append(bar)

        peak_equity = max(peak_equity, equity)
        dd = (peak_equity - equity) / peak_equity if peak_equity else 0
        max_drawdown = max(max_drawdown, dd)

        if len(equity_curve) > 2 and equity_curve[-1] < equity_curve[-2]:
            loss_count += 1

        if equity < INITIAL_CAPITAL * (1 - MAX_DRAWDOWN_THRESHOLD) or loss_count >= MAX_LOSS_TRADES:
            break

    final_equity = capital + position * sample_prices[-1]["close"]
    result = {
        "final_equity": round(final_equity, 2),
        "profit": round(final_equity - INITIAL_CAPITAL, 2),
        "max_drawdown": round(max_drawdown, 4),
        "loss_trades": loss_count,
        "sandbox_pass": final_equity > INITIAL_CAPITAL and max_drawdown < 0.25,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(os.path.join(SANDBOX_RESULTS_PATH, f"{mod_file.replace('.py', '')}.json"), "w") as f:
        json.dump(result, f, indent=2)

    return result

def main():
    modules = [f for f in os.listdir(MODULE_PATH) if f.endswith(".py")]
    for mod_file in modules:
        try:
            res = evaluate_module(mod_file)
            print(f"[S11] {mod_file} => {res}")
        except Exception as e:
            print(f"[S11 ERROR] {mod_file}: {e}")

if __name__ == "__main__":
    main()

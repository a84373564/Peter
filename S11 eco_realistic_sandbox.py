import os
import json
import math
from datetime import datetime

MODULE_PATH = "/mnt/data/Peter/modules"
PRICE_PATH = "/mnt/data/Peter/prices"
RESULT_PATH = "/mnt/data/Peter/sandbox_results"
os.makedirs(PRICE_PATH, exist_ok=True)
os.makedirs(RESULT_PATH, exist_ok=True)

INITIAL_CAPITAL = 70.0
MAX_POSITION_RATIO = 0.5
FEE = 0.0015
SLIPPAGE = 0.002
MAX_DRAWDOWN = 0.25
MAX_LOSS_TRADES = 3

def simulate_trade(action, price, capital, position):
    trade_price = price * (1 + SLIPPAGE if action == "buy" else 1 - SLIPPAGE)
    fee = trade_price * FEE
    if action == "buy":
        qty = (capital * MAX_POSITION_RATIO) / trade_price
        cost = qty * trade_price + fee
        if cost > capital:
            return capital, position, "fail"
        capital -= cost
        position += qty
    elif action == "sell" and position > 0:
        revenue = position * trade_price - fee
        capital += revenue
        position = 0
    return capital, position, "ok"

def run_simulation(mod_file):
    mod_path = os.path.join(MODULE_PATH, mod_file)
    with open(mod_path, "r") as f:
        mod_data = json.load(f)

    capital = mod_data.get("capital", 0)
    if capital <= 0:
        return {"skipped": True}

    symbol = mod_data.get("symbol", "UNKNOWN")
    price_file = f"{symbol}.json"
    price_path = os.path.join(PRICE_PATH, price_file)

    if os.path.exists(price_path):
        with open(price_path, "r") as f:
            prices = json.load(f)
    else:
        prices = [{"close": 100 + math.sin(i / 2) * 5 + (i % 7)} for i in range(30)]
        with open(price_path, "w") as f:
            json.dump(prices, f, indent=2)

    position = 0.0
    equity_curve = []
    loss_count = 0
    peak = capital
    max_dd = 0.0

    for i, bar in enumerate(prices[-30:]):
        price = bar["close"]
        action = "hold"
        if i % 5 == 2:
            action = "buy"
        elif i % 5 == 4:
            action = "sell"

        if action in ("buy", "sell"):
            capital, position, status = simulate_trade(action, price, capital, position)

        equity = capital + position * price
        equity_curve.append(equity)

        peak = max(peak, equity)
        dd = (peak - equity) / peak if peak else 0
        max_dd = max(max_dd, dd)

        if len(equity_curve) > 2 and equity_curve[-1] < equity_curve[-2]:
            loss_count += 1

        if equity < INITIAL_CAPITAL * (1 - MAX_DRAWDOWN) or loss_count >= MAX_LOSS_TRADES:
            break

    final_equity = capital + position * prices[-1]["close"]
    result = {
        "symbol": symbol,
        "final_equity": round(final_equity, 2),
        "profit": round(final_equity - INITIAL_CAPITAL, 2),
        "max_drawdown": round(max_dd, 4),
        "loss_trades": loss_count,
        "sandbox_pass": final_equity > INITIAL_CAPITAL and max_dd < MAX_DRAWDOWN,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(os.path.join(RESULT_PATH, mod_file), "w") as f:
        json.dump(result, f, indent=2)

    return result

def main():
    mods = [f for f in os.listdir(MODULE_PATH) if f.endswith(".json")]
    for mod_file in mods:
        try:
            result = run_simulation(mod_file)
            if "skipped" in result:
                continue
            print(f"[S11] {mod_file} => {result.get('profit', 'N/A')} (pass: {result.get('sandbox_pass')})")
        except Exception as e:
            print(f"[S11 ERROR] {mod_file}: {e}")

if __name__ == "__main__":
    main()

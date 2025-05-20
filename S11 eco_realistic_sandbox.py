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
            return capital, position, "fail", 0
        capital -= cost
        position += qty
        return capital, position, "buy", qty
    elif action == "sell" and position > 0:
        revenue = position * trade_price - fee
        capital += revenue
        qty_sold = position
        position = 0
        return capital, position, "sell", qty_sold
    return capital, position, "hold", 0

def run_simulation(mod_file):
    mod_path = os.path.join(MODULE_PATH, mod_file)
    with open(mod_path, "r") as f:
        mod_data = json.load(f)

    capital = mod_data.get("capital", 0)
    if capital <= 0:
        return {"skipped": True}

    symbol = mod_data.get("symbol", "UNKNOWN")
    seed = sum(ord(c) for c in symbol)
    price_file = f"{symbol}.json"
    price_path = os.path.join(PRICE_PATH, price_file)

    if os.path.exists(price_path):
        with open(price_path, "r") as f:
            prices = json.load(f)
    else:
        prices = [{"close": 100 + math.sin((i + seed) / 3) * 4 + (i % 5)} for i in range(40)]
        with open(price_path, "w") as f:
            json.dump(prices, f, indent=2)

    position = 0.0
    equity_curve = []
    loss_count = 0
    win_count = 0
    trade_count = 0
    peak = capital
    max_dd = 0.0
    last_equity = capital

    for i, bar in enumerate(prices[-30:]):
        price = bar["close"]
        action = "hold"
        if i % 4 == 1:
            action = "buy"
        elif i % 4 == 3:
            action = "sell"

        capital, position, result, qty = simulate_trade(action, price, capital, position)

        equity = capital + position * price
        equity_curve.append(equity)

        if equity > last_equity:
            win_count += 1
        else:
            loss_count += 1

        if result in ("buy", "sell"):
            trade_count += 1

        last_equity = equity
        peak = max(peak, equity)
        dd = (peak - equity) / peak if peak else 0
        max_dd = max(max_dd, dd)

        if equity < INITIAL_CAPITAL * (1 - MAX_DRAWDOWN) or loss_count >= MAX_LOSS_TRADES:
            break

    final_equity = capital + position * prices[-1]["close"]
    total_rounds = len(equity_curve)

    result = {
        "symbol": symbol,
        "final_equity": round(final_equity, 2),
        "profit": round(final_equity - INITIAL_CAPITAL, 2),
        "max_drawdown": round(max_dd, 4),
        "win_rate": round(win_count / max(1, total_rounds), 4),
        "rounds": total_rounds,
        "trades": trade_count,
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

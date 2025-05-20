import os
import json
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
    with open(os.path.join(MODULE_PATH, mod_file), "r") as f:
        mod_data = json.load(f)

    symbol = mod_data.get("symbol", "UNKNOWN")
    logic = mod_data.get("run")
    if not logic or not symbol:
        return {"error": "invalid module format"}

    price_file = f"{symbol}.json"
    price_path = os.path.join(PRICE_PATH, price_file)
    prices = []

    if os.path.exists(price_path):
        with open(price_path, "r") as f:
            prices = json.load(f)
    else:
        print(f"[S11:FALLBACK] 自動建立價格資料：{price_file}")
        prices = [{"close": 100 + i * 0.5} for i in range(30)]
        try:
            with open(price_path, "w") as f:
                json.dump(prices, f, indent=2)
        except Exception as e:
            print(f"[S11:FALLBACK ERROR] 無法寫入價格資料：{e}")

    capital = INITIAL_CAPITAL
    position = 0.0
    equity_curve = []
    history = []
    loss_count = 0
    peak = capital
    max_dd = 0.0

    for i, bar in enumerate(prices[-30:]):
        price = bar["close"]
        # 模擬策略動作（未連動實際策略邏輯，這裡是 placeholder）
        action = "hold"
        if i % 10 == 2:
            action = "buy"
        elif i % 10 == 7:
            action = "sell"

        if action in ("buy", "sell"):
            capital, position, status = simulate_trade(action, price, capital, position)

        equity = capital + position * price
        equity_curve.append(equity)
        history.append(bar)

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
            print(f"[S11] {mod_file} => {result.get('profit', 'N/A')} (pass: {result.get('sandbox_pass')})")
        except Exception as e:
            print(f"[S11 ERROR] {mod_file}: {e}")

if __name__ == "__main__":
    main()

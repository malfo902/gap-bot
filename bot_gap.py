import threading
import time
from config import TRADE_PERCENTAGE, POLL_INTERVAL
from binance_handler import get_price, get_balance, buy_eth, sell_all_eth

gaps = {}  # chiave = gap_base, valore = {"levels": set(), "active": True}

def track_prices():
    while True:
        price = get_price()
        for gap_base_str in list(gaps.keys()):
            gap_base = float(gap_base_str)
            gap = gaps[gap_base_str]

            if not gap["active"]:
                continue

            escursione = gap_base - price
            if escursione >= 13 and 1 not in gap["levels"]:
                _buy_level(gap_base_str, 1)
            if escursione >= 15 and 2 not in gap["levels"]:
                _buy_level(gap_base_str, 2)
            if escursione >= 18 and 3 not in gap["levels"]:
                _buy_level(gap_base_str, 3)

        time.sleep(POLL_INTERVAL)

def _buy_level(gap_base_str, level):
    usdc = get_balance("USDC")
    invest = usdc * TRADE_PERCENTAGE
    buy_eth(invest)
    gaps[gap_base_str]["levels"].add(level)
    print(f"[GAP {gap_base_str}] ✅ Acquisto livello {level}")

def handle_gap_closed(gap_base):
    gap_base_str = str(gap_base)
    if gap_base_str in gaps and gaps[gap_base_str]["active"]:
        sell_all_eth()
        gaps[gap_base_str]["active"] = False
        print(f"[GAP_CLOSED] 📤 Gap chiuso a {gap_base}")
    else:
        print(f"[GAP_CLOSED] ❌ Nessun gap attivo a {gap_base}")

# Avvio del thread di monitoraggio continuo
threading.Thread(target=track_prices, daemon=True).start()

def handle_gap_down(gap_base):
    gap_base_str = str(gap_base)
    if gap_base_str not in gaps:
        gaps[gap_base_str] = {"levels": set(), "active": True}
        print(f"[GAP_DOWN] 📥 Gap registrato a {gap_base}")
    else:
        print(f"[GAP_DOWN] ⚠️ Gap già presente a {gap_base}")

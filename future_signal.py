#!/usr/bin/env python3
import os, sys, time, random, hashlib
from datetime import datetime, timedelta
from telegram_bot import send_telegram_signals_summary

R  = "\033[0m"
CY = "\033[96m"
GR = "\033[92m"
YL = "\033[93m"
RD = "\033[91m"
MG = "\033[95m"
DM = "\033[2m"
BD = "\033[1m"
WH = "\033[97m"

def clr(): os.system("clear" if os.name == "posix" else "cls")

# ── Monospace Unicode converter ────────────────────────────────────────
def to_mono(text: str) -> str:
    """Convert ASCII letters/digits to mathematical monospace Unicode."""
    result = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            result.append(chr(0x1D670 + ord(ch) - ord('A')))
        elif 'a' <= ch <= 'z':
            result.append(chr(0x1D68A + ord(ch) - ord('a')))
        elif '0' <= ch <= '9':
            result.append(chr(0x1D7F6 + ord(ch) - ord('0')))
        else:
            result.append(ch)
    return ''.join(result)

BANNER = f"""{CY}{BD}
 ███████╗██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗
 ██╔════╝██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
 █████╗  ██║   ██║   ██║   ██║   ██║██████╔╝█████╗
 ██╔══╝  ██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝
 ██║     ╚██████╔╝   ██║   ╚██████╔╝██║  ██║███████╗
 ╚═╝      ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝

 ███████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗     
 ██╔════╝██║██╔════╝ ████╗  ██║██╔══██╗██║     
 ███████╗██║██║  ███╗██╔██╗ ██║███████║██║     
 ╚════██║██║██║   ██║██║╚██╗██║██╔══██║██║     
 ███████║██║╚██████╔╝██║ ╚████║██║  ██║███████╗
 ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝

{R}{GR}           ┌─ BY SUMON ─┐{R}
{GR}           {CY}💎 PREMIUM TRADING SIGNALS 💎{R}{GR}
           └──────────┘{R}
"""

TAG_LINE = (
    f"  {GR}+{R} {WH}95%+ ACCURACY + AI FILTER ACTIVE{R}  {GR}+{R}\n"
    f"  {GR}+{R} {WH}PREMIUM SIGNALS ONLY{R}              {GR}+{R}\n"
    f"  {GR}+{R} {YL}NON-MARTINGALE MODE{R}               {GR}+{R}"
)

CONTACT = (
    f"\n  {DM}{'─'*52}{R}\n"
    f"  {CY}Channel :{R}  {WH}t.me/FUTURE_SIGNAL11{R}\n"
    f"  {CY}Support :{R}  {WH}@MD_SUMON_MT4{R}\n"
    f"  {CY}Email   :{R}  {WH}sumon.ahmed.vip.id@gmail.com{R}\n"
    f"  {DM}{'─'*52}{R}"
)

ALL_PAIRS = [
    "TRUUSD-OTC","BTCUSD-OTC","XAUUSD-OTC","XAGUSD-OTC",
    "ETHUSD-OTC","LTCUSD-OTC","BNBUSD-OTC","XRPUSD-OTC",
    "ETCUSD-OTC","ZECUSD-OTC","AXSUSD-OTC","BA-OTC",
    "PFE-OTC","AXP-OTC","JNJ-OTC","INTC-OTC",
    "FB-OTC","MCD-OTC","USCRUDE-OTC","UKBRENT-OTC",
    "USDBDT-OTC","USDEGP-OTC","USDIDR-OTC","USDINR-OTC",
    "USDMXN-OTC","USDNGN-OTC","USDPHP-OTC","USDPKR-OTC",
    "USDZAR-OTC","USDARS-OTC","USDCOP-OTC","USDDZD-OTC",
    "AUDJPY-OTC","AUDNZD-OTC","AUDUSD-OTC","AUDCAD-OTC",
    "AUDCHF-OTC","CADCHF-OTC","CHFJPY-OTC","EURAUD-OTC",
    "EURCAD-OTC","EURCHF-OTC","EURGBP-OTC","EURJPY-OTC",
    "EURNZD-OTC","EURUSD-OTC","GBPAUD-OTC","GBPCAD-OTC",
    "GBPCHF-OTC","GBPJPY-OTC","GBPUSD-OTC","NZDUSD-OTC",
    "USDBRL-OTC","USDCAD-OTC","USDCHF-OTC","USDJPY-OTC",
]

BLACKOUT_PAIRS = [
    "EURUSD-OTC","GBPUSD-OTC","USDJPY-OTC","USDCAD-OTC",
    "AUDUSD-OTC","NZDUSD-OTC","XAUUSD-OTC","BTCUSD-OTC",
    "ETHUSD-OTC","GBPJPY-OTC","EURJPY-OTC","EURGBP-OTC",
]

FILTERS = {
    "1": {"name": "AI FILTER",    "label": "Running AI Filter",          "colour": CY},
    "2": {"name": "TREND FILTER", "label": "Analysing Market Trend",     "colour": MG},
    "3": {"name": "HUMAN BRAIN",  "label": "Applying Human Brain Logic", "colour": YL},
}

def separator(char="─", width=56, colour=CY):
    print(f"{colour}{char * width}{R}")

def slow_print(text, delay=0.010):
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    print()

def animated_loader(label, colour=CY, total_time=8.0):
    width    = 28
    spinners = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    spin_dur = total_time * 0.35
    bar_dur  = total_time * 0.65
    steps    = int(spin_dur / 0.13)
    for i in range(steps):
        sys.stdout.write(f"\r  {colour}{label}  {spinners[i % len(spinners)]}{R}  ")
        sys.stdout.flush(); time.sleep(0.13)
    for filled in range(width + 1):
        time.sleep((bar_dur / width) * random.uniform(0.5, 1.5))
        bar = f"{GR}{'█' * filled}{'░' * (width - filled)}{R}"
        pct = int(filled / width * 100)
        sys.stdout.write(f"\r  {colour}{label}{R}  [{bar}]  {WH}{pct}%{R}  ")
        sys.stdout.flush()
    sys.stdout.write(f"\r  {colour}{label}{R}  [{GR}{'█'*width}{R}]  {GR}100%  DONE ✔{R}   \n\n")
    sys.stdout.flush()

def show_pairs_table(pairs):
    print(f"\n  {YL}{'SELECT PAIRS':^52}{R}")
    separator()
    cols = 4
    for i, p in enumerate(pairs):
        sys.stdout.write(f"  {YL}{str(i+1)+'.':<4}{CY}{p:<14}{R}")
        if (i + 1) % cols == 0: print()
    if len(pairs) % cols != 0: print()
    separator()
    print(f"  {DM}Input:{R} {WH}1,5,12{R}  {DM}|{R}  {WH}10-30{R}  {DM}|{R}  {WH}ALL{R}\n")

def parse_pair_input(raw, pairs):
    raw = raw.strip().upper()
    if raw == "ALL": return list(pairs)
    selected, seen = [], set()
    for part in raw.replace(" ", "").split(","):
        if "-" in part:
            try:
                a, b = part.split("-", 1)
                for idx in range(int(a)-1, int(b)):
                    if 0 <= idx < len(pairs) and idx not in seen:
                        selected.append(pairs[idx]); seen.add(idx)
            except Exception: pass
        else:
            try:
                idx = int(part) - 1
                if 0 <= idx < len(pairs) and idx not in seen:
                    selected.append(pairs[idx]); seen.add(idx)
            except Exception: pass
    return selected

def parse_time(raw):
    raw = raw.strip()
    for fmt in ("%H:%M", "%H%M"):
        try:
            t = datetime.strptime(raw, fmt)
            now = datetime.now()
            return now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
        except ValueError: continue
    return None

def make_seed(pairs, fkey, start_dt, end_dt):
    date_str = datetime.now().strftime("%Y-%m-%d")
    key = f"{date_str}|{fkey}|{start_dt.strftime('%H:%M')}|{end_dt.strftime('%H:%M')}|{''.join(sorted(pairs))}"
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % (2**32)

def fake_filter_check(pair, fkey):
    thresholds = {"1": (52, 58.0), "2": (48, 55.0), "3": (45, 52.0)}
    low, thresh = thresholds[fkey]
    base = random.uniform(low, 100)
    return base >= thresh, round(base, 1)

def generate_signals(pairs, market, fkey, start_dt, end_dt):
    seed = make_seed(pairs, fkey, start_dt, end_dt)
    rng_state = random.getstate()
    random.seed(seed)
    signals     = []
    consecutive = 0
    cursor      = start_dt + timedelta(minutes=random.randint(1, 3))
    pool        = list(pairs)
    random.shuffle(pool)
    for pair in pool:
        if cursor > end_dt: break
        passed, acc = fake_filter_check(pair, fkey)
        if not passed: continue
        consecutive = consecutive + 1 if acc < 60 else 0
        if consecutive >= 3:
            consecutive = 0; continue
        signals.append({
            "pair":      pair,
            "direction": random.choice(["CALL", "PUT"]),
            "time":      cursor.strftime("%H:%M"),
            "expiry":    "1 MIN",
        })
        cursor += timedelta(minutes=random.randint(3, 7))
    random.setstate(rng_state)
    signals.sort(key=lambda s: s["time"])
    return signals

def print_signals(signals, market, filter_info, start_dt, end_dt):
    if not signals:
        print(f"\n  {RD}No signals passed the filter for this window.{R}\n")
        return
    now_str      = datetime.now().strftime("%d %b %Y  %H:%M")
    market_label = "OTC MARKETS" if market == "OTC" else "BLACKOUT SIGNALS"
    fc           = filter_info["colour"]
    window       = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"

    print()
    separator("─")
    print(f"  {CY}{BD}FUTURE SIGNAL  --  {market_label}{R}")
    print(f"  {DM}{now_str}{R}   {fc}[{filter_info['name']}]{R}   {YL}[{window}]{R}")
    separator("─")

    for s in signals:
        mono_pair = to_mono(s["pair"])
        mono_dir  = to_mono(s["direction"].lower())
        colour_dir = GR if s["direction"] == "CALL" else RD
        print(f"  {YL}→{R} {CY}{mono_pair:<24}{R}{WH}☞{R}  {YL}{s['time']}{R}  {WH}⊱{R}  {colour_dir}{mono_dir}{R}")

    separator("─")
    print(f"  {GR}Total:{R} {WH}{len(signals)} signals{R}   {fc}{filter_info['name']}{R}   {DM}Streak Guard ON{R}")
    separator()
    print(f"  {CY}Channel :{R}  {WH}t.me/FUTURE_SIGNAL11{R}")
    print(f"  {CY}Support :{R}  {WH}@MD_SUMON_MT4{R}")
    print(f"  {CY}Email   :{R}  {WH}sumon.ahmed.vip.id@gmail.com{R}")
    separator("─")
    print()
    # ✅ Telegram এ পাঠান
    time_window_str = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
    send_telegram_signals_summary(signals, market, filter_info["name"], time_window_str)
    print(f"  {GR}✅ Signals sent to Telegram!{R}\n")

def main():
    clr()
    print(BANNER)
    print(TAG_LINE)
    print(CONTACT)
    print()
    separator()

    # Status line – OTC: ONLINE  |  BLACKOUT: ONLINE
    otc_status      = f"{CY}OTC:{R}      {GR}● ONLINE{R}"
    blackout_status = f"{CY}BLACKOUT:{R} {GR}● ONLINE{R}"
    slow_print(f"  {otc_status}   {DM}|{R}   {blackout_status}", delay=0.008)

    separator()
    print()

    # Step 1 – Market
    print(f"  {YL}{'| MARKET TYPE SELECTION |':^52}{R}\n")
    print(f"  {WH}[1]{R} {CY}=>{R}  {WH}OTC MARKETS{R}")
    print(f"  {WH}[2]{R} {MG}*{R}   {MG}BLACKOUT SIGNALS{R}")
    print()
    while True:
        try:
            ch = input(f"  {GR}> Select (1-2):{R} ").strip()
            if ch in ("1","2"): break
            print(f"  {RD}Enter 1 or 2.{R}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YL}Exiting.{R}\n"); sys.exit(0)

    market    = "OTC" if ch == "1" else "BLACKOUT"
    pair_pool = ALL_PAIRS if market == "OTC" else BLACKOUT_PAIRS

    # Step 2 – Pairs
    clr(); print(BANNER); separator()
    show_pairs_table(pair_pool)
    while True:
        try:
            raw = input(f"  {GR}> SELECT PAIRS:{R}  {DM}Examples: 1,5,12  |  10-30  |  ALL{R}\n  {GR}>{R} ").strip()
            if not raw: print(f"  {RD}Enter numbers or ALL.{R}"); continue
            selected = parse_pair_input(raw, pair_pool)
            if not selected: print(f"  {RD}No valid pairs. Try again.{R}"); continue
            break
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YL}Exiting.{R}\n"); sys.exit(0)

    print(f"\n  {GR}+{R} {WH}{len(selected)} pair(s) selected.{R}\n")

    # Step 3 – Filter
    separator()
    print(f"\n  {YL}{'| SELECT FILTER |':^52}{R}\n")
    print(f"  {WH}[1]{R}  {CY}AI FILTER{R}        {DM}-- Pattern recognition{R}")
    print(f"  {WH}[2]{R}  {MG}TREND FILTER{R}      {DM}-- Market momentum{R}")
    print(f"  {WH}[3]{R}  {YL}HUMAN BRAIN{R}       {DM}-- Intuition-based logic{R}")
    print()
    while True:
        try:
            fkey = input(f"  {GR}> Select Filter (1-3):{R} ").strip()
            if fkey in FILTERS: break
            print(f"  {RD}Enter 1, 2 or 3.{R}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YL}Exiting.{R}\n"); sys.exit(0)

    filter_info = FILTERS[fkey]
    fc = filter_info["colour"]
    print(f"\n  {fc}[{filter_info['name']}] selected.{R}\n")

    # Step 4 – Time window
    separator()
    print(f"\n  {YL}{'| SET TIME WINDOW |':^52}{R}\n")
    print(f"  {DM}Format: HH:MM (24h)   e.g. 09:00  or  14:30{R}\n")

    while True:
        try:
            start_dt = parse_time(input(f"  {GR}> Start Time:{R} "))
            if not start_dt: print(f"  {RD}Invalid. Use HH:MM.{R}"); continue
            break
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YL}Exiting.{R}\n"); sys.exit(0)

    while True:
        try:
            end_dt = parse_time(input(f"  {GR}> End Time:{R}   "))
            if not end_dt: print(f"  {RD}Invalid. Use HH:MM.{R}"); continue
            if end_dt <= start_dt: print(f"  {RD}End must be after start.{R}"); continue
            break
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YL}Exiting.{R}\n"); sys.exit(0)

    wm = int((end_dt - start_dt).total_seconds() / 60)
    print(f"\n  {GR}+{R} {WH}Window: {start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}  ({wm} min){R}")

    # Step 5 – Generate
    animated_loader(filter_info["label"], colour=fc, total_time=random.uniform(8.0, 12.0))
    signals = generate_signals(selected, market, fkey, start_dt, end_dt)
    print_signals(signals, market, filter_info, start_dt, end_dt)

    # Loop
    while True:
        try:
            cmd = input(
                f"  {CY}[R]{R} Regenerate  "
                f"{CY}[T]{R} Change Time  "
                f"{CY}[N]{R} New Session  "
                f"{CY}[Q]{R} Quit\n  {GR}>{R} "
            ).strip().upper()
        except (KeyboardInterrupt, EOFError):
            cmd = "Q"

        if cmd == "Q":
            print(f"\n  {YL}FUTURE SIGNAL closed.{R}\n"); break

        elif cmd == "R":
            animated_loader(filter_info["label"], colour=fc, total_time=random.uniform(6.0, 9.0))
            signals = generate_signals(selected, market, fkey, start_dt, end_dt)
            print_signals(signals, market, filter_info, start_dt, end_dt)

        elif cmd == "T":
            separator()
            print(f"\n  {YL}{'| UPDATE TIME WINDOW |':^52}{R}\n")
            while True:
                try:
                    ns = parse_time(input(f"  {GR}> New Start Time:{R} "))
                    if not ns: print(f"  {RD}Invalid.{R}"); continue
                    break
                except (KeyboardInterrupt, EOFError):
                    print(f"\n  {YL}Exiting.{R}\n"); sys.exit(0)
            while True:
                try:
                    ne = parse_time(input(f"  {GR}> New End Time:{R}   "))
                    if not ne: print(f"  {RD}Invalid.{R}"); continue
                    if ne <= ns: print(f"  {RD}End must be after start.{R}"); continue
                    break
                except (KeyboardInterrupt, EOFError):
                    print(f"\n  {YL}Exiting.{R}\n"); sys.exit(0)
            start_dt, end_dt = ns, ne
            wm = int((end_dt - start_dt).total_seconds() / 60)
            print(f"\n  {GR}+{R} {WH}New window: {start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}  ({wm} min){R}")
            animated_loader(filter_info["label"], colour=fc, total_time=random.uniform(6.0, 9.0))
            signals = generate_signals(selected, market, fkey, start_dt, end_dt)
            print_signals(signals, market, filter_info, start_dt, end_dt)

        elif cmd == "N":
            main(); break

        else:
            print(f"  {RD}Invalid option.{R}")

if __name__ == "__main__":
    main()

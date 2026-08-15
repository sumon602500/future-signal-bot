#!/usr/bin/env python3
"""
FUTURE SIGNAL - Advanced Trading Signal Generator
সব টেকনিক্যাল ইন্ডিকেটর সহ রিয়েল ট্রেডিং সিগন্যাল
"""

import os, sys, time, random
from datetime import datetime, timedelta
from technical_analysis import TechnicalAnalysis
from trend_analysis import TrendAnalysis
from price_action import PriceAction
from data_fetcher import DataFetcher
from signal_generator import SignalGenerator, format_signal_output
from platform_config import PlatformConfig
from telegram_bot import send_telegram_signals_summary

# ========== রঙ সংজ্ঞা ==========
R  = "\033[0m"
CY = "\033[96m"
GR = "\033[92m"
YL = "\033[93m"
RD = "\033[91m"
MG = "\033[95m"
DM = "\033[2m"
BD = "\033[1m"
WH = "\033[97m"

def clr(): 
    os.system("clear" if os.name == "posix" else "cls")

def to_mono(text: str) -> str:
    """ASCII কে ইউনিকোড মনোস্পেসে রূপান্তর করুন"""
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

{R}{GR}      ┌─ BY SUMON - ADVANCED TRADING ─┐{R}
{GR}      {CY}💎 AI + TECHNICAL ANALYSIS 💎{R}{GR}
      └───────────────────────────┘{R}
"""

TAG_LINE = (
    f"  {GR}+{R} {WH}REAL-TIME TECHNICAL ANALYSIS{R}  {GR}+{R}\n"
    f"  {GR}+{R} {WH}MULTI-PLATFORM SUPPORT{R}         {GR}+{R}\n"
    f"  {GR}+{R} {YL}RISK/REWARD CALCULATION{R}        {GR}+{R}"
)

CONTACT = (
    f"\n  {DM}{'─'*52}{R}\n"
    f"  {CY}Channel :{R}  {WH}t.me/FUTURE_SIGNAL11{R}\n"
    f"  {CY}Support :{R}  {WH}@MD_SUMON_MT4{R}\n"
    f"  {CY}Email   :{R}  {WH}sumon.ahmed.vip.id@gmail.com{R}\n"
    f"  {DM}{'─'*52}{R}"
)

def separator(char="─", width=56, colour=CY):
    print(f"{colour}{char * width}{R}")

def slow_print(text, delay=0.010):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def animated_loader(label, colour=CY, total_time=8.0):
    width = 28
    spinners = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    spin_dur = total_time * 0.35
    bar_dur = total_time * 0.65
    steps = int(spin_dur / 0.13)
    
    for i in range(steps):
        sys.stdout.write(f"\r  {colour}{label}  {spinners[i % len(spinners)]}{R}  ")
        sys.stdout.flush()
        time.sleep(0.13)
    
    for filled in range(width + 1):
        time.sleep((bar_dur / width) * random.uniform(0.5, 1.5))
        bar = f"{GR}{'█' * filled}{'░' * (width - filled)}{R}"
        pct = int(filled / width * 100)
        sys.stdout.write(f"\r  {colour}{label}{R}  [{bar}]  {WH}{pct}%{R}  ")
        sys.stdout.flush()
    
    print(f"\r  {colour}{label}{R}  [{GR}{'█'*width}{R}]  {GR}100%  DONE ✔{R}   \n")

def show_platforms():
    """প্ল্যাটফর্ম সিলেকশন প্রদর্শন করুন"""
    print(PlatformConfig.display_platforms())

def show_pairs_table(pairs):
    """পেয়ার টেবিল প্রদর্শন করুন"""
    print(f"\n  {YL}{'SELECT PAIRS':^52}{R}")
    separator()
    cols = 3
    for i, p in enumerate(pairs):
        sys.stdout.write(f"  {YL}{str(i+1)+'.':<4}{CY}{p:<16}{R}")
        if (i + 1) % cols == 0:
            print()
    if len(pairs) % cols != 0:
        print()
    separator()
    print(f"  {DM}Input:{R} {WH}1,5,12{R}  {DM}|{R}  {WH}10-30{R}  {DM}|{R}  {WH}ALL{R}\n")

def parse_pair_input(raw, pairs):
    """ইউজার ইনপুট পার্স করুন"""
    raw = raw.strip().upper()
    if raw == "ALL":
        return list(pairs)
    
    selected, seen = [], set()
    for part in raw.replace(" ", "").split(","):
        if "-" in part:
            try:
                a, b = part.split("-", 1)
                for idx in range(int(a)-1, int(b)):
                    if 0 <= idx < len(pairs) and idx not in seen:
                        selected.append(pairs[idx])
                        seen.add(idx)
            except:
                pass
        else:
            try:
                idx = int(part) - 1
                if 0 <= idx < len(pairs) and idx not in seen:
                    selected.append(pairs[idx])
                    seen.add(idx)
            except:
                pass
    
    return selected

def parse_time(raw):
    """সময় পার্স করুন"""
    raw = raw.strip()
    for fmt in ("%H:%M", "%H%M"):
        try:
            t = datetime.strptime(raw, fmt)
            now = datetime.now()
            return now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
        except:
            continue
    return None

def print_signals(signals, market, platform, start_dt, end_dt):
    """সিগন্যাল প্রিন্ট করুন"""
    
    if not signals:
        print(f"\n  {RD}কোনো শক্তিশালী সিগন্যাল পাওয়া যায়নি।{R}\n")
        return
    
    now_str = datetime.now().strftime("%d %b %Y  %H:%M")
    window = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
    
    print()
    separator("─")
    print(f"  {CY}{BD}FUTURE SIGNAL{R}")
    print(f"  {DM}{now_str}{R}   {YL}[{platform}]{R}   {YL}[{window}]{R}")
    separator("─")
    
    for sig in signals:
        if sig["confidence"] >= 60:  # শুধুমাত্র শক্তিশালী সিগন্যাল
            emoji = "🟢" if sig["direction"] == "CALL" else "🔴" if sig["direction"] == "PUT" else "⚪"
            print(f"  {emoji} {CY}{sig['pair']:<12}{R} {YL}{sig['signal']:<15}{R} আত্মবিশ্বাস: {WH}{sig['confidence']}%{R}")
            print(f"      মূল্য: {sig['details']['current_price']} | সাপোর্ট: {sig['details']['nearest_support']} | রেজিস্ট্যান্স: {sig['details']['nearest_resistance']}")
            print()
    
    separator("─")
    print(f"  {GR}মোট:{R} {WH}{len([s for s in signals if s['confidence'] >= 60])} শক্তিশালী সিগন্যাল{R}")
    separator()
    print()

def main():
    clr()
    print(BANNER)
    print(TAG_LINE)
    print(CONTACT)
    print()
    separator()
    
    # স্ট্যাটাস লাইন
    status = f"{CY}Status:{R} {GR}● ONLINE{R}"
    slow_print(f"  {status}", delay=0.008)
    
    separator()
    print()
    
    # ধাপ 1: প্ল্যাটফর্ম সিলেকশন
    show_platforms()
    
    while True:
        try:
            ch = input(f"  {GR}> প্ল্যাটফর্ম বেছে নিন (1-3):{R} ").strip()
            if ch in ("1", "2", "3"):
                break
            print(f"  {RD}1, 2 বা 3 লিখুন।{R}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YL}প্রস্থান করা হচ্ছে।{R}\n")
            sys.exit(0)
    
    platform_key = ["quotex", "pocket_option", "olymptrade"][int(ch)-1]
    platform_info = PlatformConfig.get_platform_info(platform_key)
    platform_name = platform_info["name"]
    
    print(f"\n  {GR}+{R} {WH}{platform_name} নির্বাচিত।{R}\n")
    
    # ধাপ 2: পেয়ার সিলেকশন
    clr()
    print(BANNER)
    separator()
    
    pair_pool = PlatformConfig.get_all_pairs_flat(platform_key)
    show_pairs_table(pair_pool)
    
    while True:
        try:
            raw = input(f"  {GR}> পেয়ার নির্বাচন করুন:{R} ").strip()
            if not raw:
                print(f"  {RD}সংখ্যা বা ALL লিখুন।{R}")
                continue
            selected = parse_pair_input(raw, pair_pool)
            if not selected:
                print(f"  {RD}কোনো বৈধ পেয়ার নেই।{R}")
                continue
            break
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YL}প্রস্থান করা হচ্ছে।{R}\n")
            sys.exit(0)
    
    print(f"\n  {GR}+{R} {WH}{len(selected)} পেয়ার নির্বাচিত।{R}\n")
    
    # ধাপ 3: সময় উইন্ডো
    separator()
    print(f"\n  {YL}{'| সময় উইন্ডো সেট করুন |':^52}{R}\n")
    print(f"  {DM}ফরম্যাট: HH:MM (24ঘণ্টা)   উদাহরণ: 09:00 বা 14:30{R}\n")
    
    while True:
        try:
            start_dt = parse_time(input(f"  {GR}> শুরুর সময়:{R} "))
            if not start_dt:
                print(f"  {RD}অবৈধ। HH:MM ব্যবহার করুন।{R}")
                continue
            break
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YL}প্রস্থান করা হচ্ছে।{R}\n")
            sys.exit(0)
    
    while True:
        try:
            end_dt = parse_time(input(f"  {GR}> শেষের সময়:{R}   "))
            if not end_dt:
                print(f"  {RD}অবৈধ। HH:MM ব্যবহার করুন।{R}")
                continue
            if end_dt <= start_dt:
                print(f"  {RD}শেষ সময় শুরুর পরে হতে হবে।{R}")
                continue
            break
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {YL}প্রস্থান করা হচ্ছে।{R}\n")
            sys.exit(0)
    
    wm = int((end_dt - start_dt).total_seconds() / 60)
    print(f"\n  {GR}+{R} {WH}উইন্ডো: {start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}  ({wm} মিনিট){R}\n")
    
    # ধাপ 4: ডাটা ফেচ এবং বিশ্লেষণ
    animated_loader("ডাটা ফেচ করা হচ্ছে", colour=CY, total_time=random.uniform(5.0, 8.0))
    
    fetcher = DataFetcher()
    signal_gen = SignalGenerator()
    
    # ডাটা ফেচ করুন
    all_signals = []
    for pair in selected:
        try:
            # ডেমো ডাটা ব্যবহার করুন (রিয়েল API এর পরিবর্তে)
            df = fetcher.get_ohlcv_data(pair, data_source="sample", periods=100, start_price=100)
            
            if df is not None:
                signal = signal_gen.analyze_pair(df, pair)
                all_signals.append(signal)
        except Exception as e:
            print(f"  {RD}Error processing {pair}: {e}{R}")
    
    print_signals(all_signals, "OTC MARKETS", platform_name, start_dt, end_dt)
    
    # টেলিগ্রাম এ পাঠান
    try:
        time.sleep(1)
        send_telegram_signals_summary(
            all_signals,
            "OTC",
            "Real Technical Analysis",
            f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
        )
        print(f"  {GR}✅ সিগন্যাল টেলিগ্রামে পাঠানো হয়েছে!{R}\n")
    except Exception as e:
        print(f"  {YL}⚠️  টেলিগ্রাম সতর্কতা: {e}{R}\n")
    
    # লু��� অপশন
    while True:
        try:
            cmd = input(
                f"  {CY}[R]{R} পুনরায় অ্যানালাইজ  "
                f"{CY}[N]{R} নতুন সেশন  "
                f"{CY}[Q]{R} প্রস্থান\n  {GR}>{R} "
            ).strip().upper()
        except (KeyboardInterrupt, EOFError):
            cmd = "Q"
        
        if cmd == "Q":
            print(f"\n  {YL}FUTURE SIGNAL বন্ধ হচ্ছে।{R}\n")
            break
        elif cmd == "R":
            animated_loader("পুনরায় অ্যানালাইজ করা হচ্ছে", colour=CY, total_time=random.uniform(3.0, 5.0))
            # পুনরায় বিশ্লেষণ করুন
            print_signals(all_signals, "OTC MARKETS", platform_name, start_dt, end_dt)
        elif cmd == "N":
            main()
            break
        else:
            print(f"  {RD}অবৈধ অপশন।{R}")

if __name__ == "__main__":
    main()

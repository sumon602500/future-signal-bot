#!/usr/bin/env python3
"""
Platform Configuration Module
Quotex, Pocket Option, OlympTrade এর OTC পেয়ার এবং সেটিংস
"""

# ========== QUOTEX OTC PAIRS ==========
QUOTEX_OTC_PAIRS = {
    "CRYPTO": [
        "BTCUSD", "ETHUSD", "LTCUSD", "BNBUSD", "XRPUSD",
        "ADAUSD", "DOTUSD", "SOLANASUSD", "MATICUSD", "AVAXUSD"
    ],
    "METALS": [
        "XAUUSD", "XAGUSD"
    ],
    "FOREX": [
        "EURUSD", "GBPUSD", "USDJPY", "USDCAD", "AUDUSD",
        "NZDUSD", "EURGBP", "EURJPY", "GBPJPY", "USDCHF"
    ],
    "COMMODITIES": [
        "USCRUDE", "UKBRENT", "NATGAS"
    ],
    "INDICES": [
        "US30", "US100", "US500", "UK100", "GER40"
    ],
    "STOCKS": [
        "BA", "PFE", "AXP", "JNJ", "INTC", "FB", "MCD",
        "AMZN", "GOOGL", "MSFT", "TSLA", "AAPL"
    ]
}

# ========== POCKET OPTION OTC PAIRS ==========
POCKET_OPTION_OTC_PAIRS = {
    "CRYPTO": [
        "BTCUSD", "ETHUSD", "LTCUSD", "BNBUSD", "XRPUSD",
        "ADAUSD", "TRXUSD", "ETCUSD", "LINKUSD", "UNIUSD"
    ],
    "METALS": [
        "XAUUSD", "XAGUSD"
    ],
    "FOREX": [
        "EURUSD", "GBPUSD", "USDJPY", "USDCAD", "AUDUSD",
        "NZDUSD", "EURGBP", "EURJPY", "GBPJPY", "CHFJPY"
    ],
    "COMMODITIES": [
        "USCRUDE", "UKBRENT"
    ],
    "INDICES": [
        "US30", "US100", "US500", "UK100", "SPX"
    ],
    "STOCKS": [
        "BA", "PFE", "AXP", "JNJ", "INTC", "FB", "MCD",
        "DIS", "PYPL", "SQ", "CRM", "NFLX"
    ]
}

# ========== OLYMP TRADE OTC PAIRS ==========
OLYMPTRADE_OTC_PAIRS = {
    "CRYPTO": [
        "BTCUSD", "ETHUSD", "LTCUSD", "BNBUSD", "XRPUSD",
        "BCHUSD", "DASHUSD", "XMRUSD", "ZECUSD", "NEOUSD"
    ],
    "METALS": [
        "XAUUSD", "XAGUSD"
    ],
    "FOREX": [
        "EURUSD", "GBPUSD", "USDJPY", "USDCAD", "AUDUSD",
        "NZDUSD", "EURCHF", "GBPCHF", "AUDCHF", "CADCHF"
    ],
    "COMMODITIES": [
        "USCRUDE", "UKBRENT", "COPPER"
    ],
    "INDICES": [
        "US30", "US100", "US500", "DAX40", "CAC40"
    ],
    "STOCKS": [
        "BA", "PFE", "AXP", "JNJ", "INTC", "FB", "MCD",
        "VTSAX", "VOO", "VTI", "SCHB", "VB"
    ]
}

# ========== প্ল্যাটফর্ম বৈশিষ্ট্য ==========
PLATFORM_FEATURES = {
    "quotex": {
        "name": "Quotex",
        "emoji": "💎",
        "min_expiry": "30 সেকেন্ড",
        "max_expiry": "4 ঘণ্টা",
        "min_amount": "$1",
        "payout": "85-90%",
        "pairs": QUOTEX_OTC_PAIRS,
        "url": "https://quotex.io"
    },
    "pocket_option": {
        "name": "Pocket Option",
        "emoji": "📱",
        "min_expiry": "5 সেকেন্ড",
        "max_expiry": "1 ঘণ্টা",
        "min_amount": "$1",
        "payout": "80-92%",
        "pairs": POCKET_OPTION_OTC_PAIRS,
        "url": "https://po.me"
    },
    "olymptrade": {
        "name": "OlympTrade",
        "emoji": "🏆",
        "min_expiry": "1 মিনিট",
        "max_expiry": "4 ঘণ্টা",
        "min_amount": "$1",
        "payout": "80-95%",
        "pairs": OLYMPTRADE_OTC_PAIRS,
        "url": "https://olymptrade.com"
    }
}

# ========== সাধারণ OTC PAIRS (সব প্ল্যাটফর্মে) ==========
COMMON_OTC_PAIRS = [
    "BTCUSD", "ETHUSD", "LTCUSD", "BNBUSD", "XRPUSD",
    "XAUUSD", "XAGUSD",
    "EURUSD", "GBPUSD", "USDJPY", "USDCAD", "AUDUSD",
    "USCRUDE", "UKBRENT",
    "US30", "US100", "US500",
    "BA", "PFE", "AXP", "JNJ", "INTC"
]

class PlatformConfig:
    """প্ল্যাটফর্ম কনফিগারেশন ম্যানেজার"""
    
    @staticmethod
    def get_platform_pairs(platform_name):
        """
        নির্দিষ্ট প্ল্যাটফর্মের OTC পেয়ার পান
        """
        platform = platform_name.lower()
        
        if platform == "quotex":
            return QUOTEX_OTC_PAIRS
        elif platform == "pocket_option" or platform == "pocket option":
            return POCKET_OPTION_OTC_PAIRS
        elif platform == "olymptrade" or platform == "olymp trade":
            return OLYMPTRADE_OTC_PAIRS
        else:
            return {"ALL": COMMON_OTC_PAIRS}
    
    @staticmethod
    def get_all_pairs_flat(platform_name):
        """
        সব পেয়ার একটি সাধারণ লিস্টে ফ্ল্যাট করুন
        """
        pairs_dict = PlatformConfig.get_platform_pairs(platform_name)
        flat_list = []
        for category, pairs in pairs_dict.items():
            flat_list.extend(pairs)
        return list(set(flat_list))  # ডুপ্লিকেট সরান
    
    @staticmethod
    def get_platform_info(platform_name):
        """
        প্ল্যাটফর্ম তথ্য পান
        """
        platform = platform_name.lower()
        
        if platform == "quotex":
            return PLATFORM_FEATURES["quotex"]
        elif platform == "pocket_option" or platform == "pocket option":
            return PLATFORM_FEATURES["pocket_option"]
        elif platform == "olymptrade" or platform == "olymp trade":
            return PLATFORM_FEATURES["olymptrade"]
        else:
            return None
    
    @staticmethod
    def list_platforms():
        """
        সব উপলব্ধ প্ল্যাটফর্ম তালিকাভুক্ত করুন
        """
        return list(PLATFORM_FEATURES.keys())
    
    @staticmethod
    def display_platforms():
        """
        ইউজার-বান্ধব প্ল্যাটফর্ম তালিকা প্রদর্শন করুন
        """
        output = "\n  " + "="*50 + "\n"
        output += "  📊 উপলব্ধ প্ল্যাটফর্ম:\n"
        output += "  " + "="*50 + "\n\n"
        
        for idx, (key, info) in enumerate(PLATFORM_FEATURES.items(), 1):
            output += f"  [{idx}] {info['emoji']} {info['name']}\n"
            output += f"       পেআউট: {info['payout']} | সর্বনিম্ন: {info['min_amount']}\n"
            output += f"       পেয়ার সংখ্যা: {sum(len(v) for v in info['pairs'].values())}\n\n"
        
        output += "  " + "="*50 + "\n"
        return output

# প্ল্যাটফর্ম ম্যাপিং
PLATFORM_MAP = {
    1: "quotex",
    2: "pocket_option",
    3: "olymptrade"
}

print("✅ Platform Configuration Module Loaded")

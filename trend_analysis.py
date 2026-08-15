#!/usr/bin/env python3
"""
Trend Analysis Module
ট্রেন্ড ডিটেকশন, ভলিউম অ্যানালাইসিস, মার্কেট মোমেন্টাম
"""

import numpy as np
import pandas as pd

class TrendAnalysis:
    """ট্রেন্ড এবং মোমেন্টাম বিশ্লেষণ"""
    
    @staticmethod
    def detect_trend(close_prices, period=20):
        """
        আপট্রেন্ড/ডাউনট্রেন্ড ডিটেকশন
        রিটার্ন: "UPTREND", "DOWNTREND", "SIDEWAYS"
        """
        sma_short = close_prices.rolling(window=period//2).mean()
        sma_long = close_prices.rolling(window=period).mean()
        
        if sma_short.iloc[-1] > sma_long.iloc[-1]:
            return "UPTREND", 1
        elif sma_short.iloc[-1] < sma_long.iloc[-1]:
            return "DOWNTREND", -1
        else:
            return "SIDEWAYS", 0
    
    @staticmethod
    def calculate_momentum(close_prices, period=10):
        """
        মোমেন্টাম = বর্তমান মূল্য - (period দিন আগের মূল্য)
        ইতিবাচক = ঊর্ধ্বমুখী মোমেন্টাম
        নেতিবাচক = নিম্নমুখী মোমেন্টাম
        """
        momentum = close_prices - close_prices.shift(period)
        return momentum
    
    @staticmethod
    def calculate_roc(close_prices, period=12):
        """
        Rate of Change (ROC)
        পরিবর্তনের হার (শতাংশ)
        """
        roc = ((close_prices - close_prices.shift(period)) / close_prices.shift(period)) * 100
        return roc
    
    @staticmethod
    def analyze_volume(volume, close_prices, period=20):
        """
        ভলিউম এনালাইসিস
        - ভলিউম প্রবণতা
        - অন-ব্যালেন্স ভলিউম (OBV)
        - ভলিউম সিগন্যাল
        """
        volume_sma = volume.rolling(window=period).mean()
        
        # অন-ব্যালেন্স ভলিউম (OBV)
        obv = (np.sign(close_prices.diff()) * volume).fillna(0).cumsum()
        
        # ভলিউম ট্রেন্ড
        if volume.iloc[-1] > volume_sma.iloc[-1]:
            volume_trend = "INCREASING"
            volume_signal = 1
        elif volume.iloc[-1] < volume_sma.iloc[-1]:
            volume_trend = "DECREASING"
            volume_signal = -1
        else:
            volume_trend = "NEUTRAL"
            volume_signal = 0
        
        return {
            "volume_sma": volume_sma,
            "obv": obv,
            "trend": volume_trend,
            "signal": volume_signal,
            "current_volume": volume.iloc[-1],
            "avg_volume": volume_sma.iloc[-1]
        }
    
    @staticmethod
    def calculate_adx(high, low, close, period=14):
        """
        Average Directional Index (ADX)
        ট্রেন্ড শক্তি নির্দেশ করে
        0-20: দুর্বল ট্রেন্ড
        20-40: মাঝারি ট্রেন্ড
        40+: শক্তিশালী ট্রেন্ড
        """
        plus_dm = high.diff()
        minus_dm = low.diff()
        
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0
        minus_dm = abs(minus_dm)
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        atr = tr.rolling(window=period).mean()
        
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()
        
        return adx, plus_di, minus_di
    
    @staticmethod
    def detect_divergence(price, indicator, period=20):
        """
        Divergence ডিটেকশন
        মূল্য নতুন উচ্চতায় কিন্তু সূচক নতুন উচ্চতায় নেই = বিয়ারিশ ডাইভার্জেন্স
        """
        price_highs = price.rolling(window=period).max()
        indicator_highs = indicator.rolling(window=period).max()
        
        # বিয়ারিশ ডাইভার্জেন্স
        if price.iloc[-1] > price_highs.iloc[-period] and indicator.iloc[-1] < indicator_highs.iloc[-period]:
            return "BEARISH_DIVERGENCE", -1
        
        # বুলিশ ডাইভার্জেন্স
        if price.iloc[-1] < price_highs.iloc[-period] and indicator.iloc[-1] > indicator_highs.iloc[-period]:
            return "BULLISH_DIVERGENCE", 1
        
        return "NO_DIVERGENCE", 0
    
    @staticmethod
    def market_strength(uptrend, volume_signal, momentum_signal, rsi_signal):
        """
        সামগ্রিক বাজার শক্তি গণনা
        -3 থেকে +3 স্কেলে
        """
        strength = uptrend + volume_signal + momentum_signal + rsi_signal
        return strength

# ট্রেন্ড শক্তি সূচী
TREND_STRENGTH = {
    3: "🟢 অত্যন্ত শক্তিশালী বুলিশ",
    2: "🟢 শক্তিশালী বুলিশ",
    1: "🟡 মৃদু বুলিশ",
    0: "⚪ নিরপেক্ষ",
    -1: "🟠 মৃদু বিয়ারিশ",
    -2: "🔴 শক্তিশালী বিয়ারিশ",
    -3: "🔴 অত্যন্ত শক্তিশালী বিয়ারিশ",
}

print("✅ Trend Analysis Module Loaded")

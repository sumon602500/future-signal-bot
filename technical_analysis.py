#!/usr/bin/env python3
"""
Technical Analysis Module
রিয়েল টেকনিক্যাল ইন্ডিকেটর ক্যালকুলেশন
"""

import numpy as np
import pandas as pd

class TechnicalAnalysis:
    """সব টেকনিক্যাল ইন্ডিকেটর হিসাব করার ক্লাস"""
    
    @staticmethod
    def calculate_sma(data, period=20):
        """Simple Moving Average (সরল গড়)"""
        return data.rolling(window=period).mean()
    
    @staticmethod
    def calculate_ema(data, period=20):
        """Exponential Moving Average (সূচক গড়)"""
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_rsi(data, period=14):
        """
        Relative Strength Index (RSI)
        0-30: ওভারসোল্ড (কিনুন)
        70-100: ওভারবট (বিক্রয় করুন)
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(data, fast=12, slow=26, signal=9):
        """
        MACD (Moving Average Convergence Divergence)
        রিটার্ন: macd_line, signal_line, histogram
        """
        ema_fast = data.ewm(span=fast, adjust=False).mean()
        ema_slow = data.ewm(span=slow, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(data, period=20, num_std=2):
        """
        বলিন্জার ব্যান্ড
        রিটার্ন: upper_band, middle_band, lower_band
        """
        sma = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        
        upper_band = sma + (num_std * std)
        lower_band = sma - (num_std * std)
        
        return upper_band, sma, lower_band
    
    @staticmethod
    def find_support_resistance(data, window=20):
        """
        সাপোর্ট এবং রেজিস্ট্যান্স লেভেল খুঁজুন
        """
        # রেজিস্ট্যান্স = স্থানীয় সর্বোচ্চ
        resistance = data.rolling(window=window, center=True).max()
        
        # সাপোর্ট = স্থানীয় সর্বনিম্ন
        support = data.rolling(window=window, center=True).min()
        
        return support, resistance
    
    @staticmethod
    def calculate_atr(high, low, close, period=14):
        """
        Average True Range (ATR)
        ভোলাটিলিটি মাপার জন্য
        """
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def calculate_volume_ma(volume, period=20):
        """ভলিউম মুভিং এভারেজ"""
        return volume.rolling(window=period).mean()

# ইন্ডিকেটর সাইন এবং মান
INDICATOR_THRESHOLDS = {
    "rsi": {"overbought": 70, "oversold": 30},
    "macd": {"bullish": "positive", "bearish": "negative"},
    "bollinger": {"upper": "resistance", "lower": "support"},
}

print("✅ Technical Analysis Module Loaded")

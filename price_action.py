#!/usr/bin/env python3
"""
Price Action Module
ক্যান্ডেল প্যাটার্ন এবং প্রাইস লেভেল বিশ্লেষণ
"""

import numpy as np
import pandas as pd

class PriceAction:
    """প্রাইস অ্যাকশন এবং ক্যান্ডেল প্যাটার্ন বিশ্লেষণ"""
    
    @staticmethod
    def analyze_candle(open_price, close_price, high, low):
        """
        একটি ক্যান্ডেল বিশ্লেষণ করুন
        রিটার্ন: ক্যান্ডেল টাইপ এবং শক্তি
        """
        body = abs(close_price - open_price)
        upper_wick = high - max(open_price, close_price)
        lower_wick = min(open_price, close_price) - low
        total_range = high - low
        
        # ক্যান্ডেল শরীরের শতাংশ
        body_percent = body / total_range if total_range > 0 else 0
        
        if close_price > open_price:
            # বুলিশ ক্যান্ডেল
            candle_type = "BULLISH"
            if body_percent > 0.8:
                pattern = "STRONG_BULLISH"
                strength = 2
            elif body_percent > 0.5:
                pattern = "MODERATE_BULLISH"
                strength = 1
            else:
                pattern = "WEAK_BULLISH"
                strength = 0
        elif close_price < open_price:
            # বিয়ারিশ ক্যান্ডেল
            candle_type = "BEARISH"
            if body_percent > 0.8:
                pattern = "STRONG_BEARISH"
                strength = -2
            elif body_percent > 0.5:
                pattern = "MODERATE_BEARISH"
                strength = -1
            else:
                pattern = "WEAK_BEARISH"
                strength = 0
        else:
            # ডজি ক্যান্ডেল
            candle_type = "DOJI"
            pattern = "DOJI"
            strength = 0
        
        return {
            "type": candle_type,
            "pattern": pattern,
            "strength": strength,
            "body": body,
            "upper_wick": upper_wick,
            "lower_wick": lower_wick,
            "body_percent": body_percent
        }
    
    @staticmethod
    def detect_engulfing(prev_candle, curr_candle):
        """
        Engulfing প্যাটার্ন ডিটেকশন
        বুলিশ এনগালফিং: আগের বিয়ারিশ ক্যান্ডেল বর্তমান বুলিশ ক্যান্ডেল দ্বারা সম্পূর্ণভাবে আচ্ছাদিত
        """
        # বুলিশ এনগালফিং
        if (prev_candle["type"] == "BEARISH" and 
            curr_candle["type"] == "BULLISH"):
            return "BULLISH_ENGULFING", 2
        
        # বিয়ারিশ এনগালফিং
        if (prev_candle["type"] == "BULLISH" and 
            curr_candle["type"] == "BEARISH"):
            return "BEARISH_ENGULFING", -2
        
        return "NO_ENGULFING", 0
    
    @staticmethod
    def detect_hammer(candle):
        """
        Hammer প্যাটার্ন ডিটেকশন
        ছোট শরীর + লম্বা নিম্ন wick = বুলিশ সিগন্যাল
        """
        if candle["body_percent"] < 0.3 and candle["lower_wick"] > 2 * candle["body"]:
            return "HAMMER", 1
        return "NO_HAMMER", 0
    
    @staticmethod
    def detect_shooting_star(candle):
        """
        Shooting Star প্যাটার্ন ডিটেকশন
        ছোট শরীর + লম্বা উপরের wick = বিয়ারিশ সিগন্যাল
        """
        if candle["body_percent"] < 0.3 and candle["upper_wick"] > 2 * candle["body"]:
            return "SHOOTING_STAR", -1
        return "NO_SHOOTING_STAR", 0
    
    @staticmethod
    def detect_reversal_patterns(recent_candles):
        """
        বিপরীতকরণ প্যাটার্ন ডিটেকশন (3-5 ক্যান্ডেল)
        """
        if len(recent_candles) < 3:
            return "INSUFFICIENT_DATA", 0
        
        # উঠানামা প্যাটার্ন (বুলিশ)
        if (recent_candles[-3]["type"] == "BEARISH" and
            recent_candles[-2]["type"] == "BULLISH" and
            recent_candles[-1]["type"] == "BULLISH"):
            return "BULLISH_REVERSAL", 2
        
        # উঠানামা প্যাটার্ন (বিয়ারিশ)
        if (recent_candles[-3]["type"] == "BULLISH" and
            recent_candles[-2]["type"] == "BEARISH" and
            recent_candles[-1]["type"] == "BEARISH"):
            return "BEARISH_REVERSAL", -2
        
        return "NO_REVERSAL", 0
    
    @staticmethod
    def find_support_resistance_levels(data, window=20, threshold=0.02):
        """
        সাপোর্ট এবং রেজিস্ট্যান্স লেভেল খুঁজুন
        """
        # স্থানীয় সর্বোচ্চ (রেজিস্ট্যান্স)
        resistance_points = []
        for i in range(window, len(data) - window):
            if data[i] == max(data[i-window:i+window]):
                resistance_points.append(data[i])
        
        # স্থানীয় সর্বনিম্ন (সাপোর্ট)
        support_points = []
        for i in range(window, len(data) - window):
            if data[i] == min(data[i-window:i+window]):
                support_points.append(data[i])
        
        # ক্লাস্টার করুন এবং গড় বের করুন
        resistance_levels = []
        support_levels = []
        
        if resistance_points:
            # সমান স্তরগুলি একত্রিত করুন
            resistance_points.sort()
            current_cluster = [resistance_points[0]]
            for price in resistance_points[1:]:
                if abs(price - current_cluster[-1]) / current_cluster[-1] < threshold:
                    current_cluster.append(price)
                else:
                    resistance_levels.append(np.mean(current_cluster))
                    current_cluster = [price]
            if current_cluster:
                resistance_levels.append(np.mean(current_cluster))
        
        if support_points:
            support_points.sort()
            current_cluster = [support_points[0]]
            for price in support_points[1:]:
                if abs(price - current_cluster[-1]) / current_cluster[-1] < threshold:
                    current_cluster.append(price)
                else:
                    support_levels.append(np.mean(current_cluster))
                    current_cluster = [price]
            if current_cluster:
                support_levels.append(np.mean(current_cluster))
        
        return sorted(resistance_levels, reverse=True), sorted(support_levels)
    
    @staticmethod
    def price_rejection_at_level(current_price, level, tolerance=0.01):
        """
        লেভেলে মূল্য প্রত্যাখ্যান আছে কিনা চেক করুন
        """
        if abs(current_price - level) / level < tolerance:
            return True
        return False
    
    @staticmethod
    def calculate_risk_reward(entry, stop_loss, take_profit):
        """
        ঝুঁকি/পুরস্কার অনুপাত গণনা করুন
        """
        risk = abs(entry - stop_loss)
        reward = abs(take_profit - entry)
        
        if risk == 0:
            return 0
        
        ratio = reward / risk
        return ratio

# ক্যান্ডেল প্যাটার্ন সাইন
CANDLE_PATTERNS = {
    "BULLISH_ENGULFING": {"strength": 2, "emoji": "🟢"},
    "BEARISH_ENGULFING": {"strength": -2, "emoji": "🔴"},
    "HAMMER": {"strength": 1, "emoji": "🟢"},
    "SHOOTING_STAR": {"strength": -1, "emoji": "🔴"},
    "DOJI": {"strength": 0, "emoji": "⚪"},
    "STRONG_BULLISH": {"strength": 1, "emoji": "🟢"},
    "STRONG_BEARISH": {"strength": -1, "emoji": "🔴"},
}

print("✅ Price Action Module Loaded")

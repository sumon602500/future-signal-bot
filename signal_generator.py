#!/usr/bin/env python3
"""
Signal Generator Module
সব টেকনিক্যাল ইন্ডিকেটর একত্রিত করে ট্রেডিং সিগন্যাল তৈরি করুন
"""

import pandas as pd
import numpy as np
from technical_analysis import TechnicalAnalysis
from trend_analysis import TrendAnalysis, TREND_STRENGTH
from price_action import PriceAction, CANDLE_PATTERNS
from data_fetcher import DataFetcher

class SignalGenerator:
    """সম্পূর্ণ ট্রেডিং সিগন্যাল জেনারেটর"""
    
    def __init__(self):
        self.ta = TechnicalAnalysis()
        self.trend = TrendAnalysis()
        self.price_action = PriceAction()
        self.fetcher = DataFetcher()
    
    def analyze_pair(self, df, pair_name="PAIR"):
        """
        একটি পেয়ারের সম্পূর্ণ বিশ্লেষণ করুন
        রিটার্ন: সম্পূর্ণ সিগন্যাল ডাটা
        """
        
        if df is None or len(df) < 30:
            return {
                "pair": pair_name,
                "signal": "INSUFFICIENT_DATA",
                "confidence": 0,
                "direction": "NEUTRAL",
                "details": {}
            }
        
        # প্রয়োজনীয় কলাম নিশ্চিত করুন
        try:
            close = pd.to_numeric(df['close'], errors='coerce')
            high = pd.to_numeric(df['high'], errors='coerce') if 'high' in df.columns else close
            low = pd.to_numeric(df['low'], errors='coerce') if 'low' in df.columns else close
            volume = pd.to_numeric(df['volume'], errors='coerce') if 'volume' in df.columns else pd.Series([1]*len(df))
        except:
            return {
                "pair": pair_name,
                "signal": "DATA_ERROR",
                "confidence": 0,
                "direction": "NEUTRAL",
                "details": {}
            }
        
        # ========== টেকনিক্যাল ইন্ডিকেটর ==========
        
        # 1. মুভিং এভারেজ
        sma_20 = self.ta.calculate_sma(close, period=20)
        ema_12 = self.ta.calculate_ema(close, period=12)
        
        # 2. RSI
        rsi = self.ta.calculate_rsi(close, period=14)
        
        # 3. MACD
        macd_line, signal_line, histogram = self.ta.calculate_macd(close)
        
        # 4. বলিন্জার ব্যান্ড
        upper_bb, middle_bb, lower_bb = self.ta.calculate_bollinger_bands(close, period=20, num_std=2)
        
        # 5. ATR (ভোলাটিলিটি)
        atr = self.ta.calculate_atr(high, low, close, period=14)
        
        # ========== ট্রেন্ড বিশ্লেষণ ==========
        
        # 1. ট্রেন্ড ডিটেকশন
        trend_name, trend_signal = self.trend.detect_trend(close, period=20)
        
        # 2. মোমেন্টাম
        momentum = self.trend.calculate_momentum(close, period=10)
        momentum_signal = 1 if momentum.iloc[-1] > 0 else -1 if momentum.iloc[-1] < 0 else 0
        
        # 3. ভলিউম বিশ্লেষণ
        volume_analysis = self.trend.analyze_volume(volume, close, period=20)
        volume_signal = volume_analysis["signal"]
        
        # 4. ADX (ট্রেন্ড শক্তি)
        adx, plus_di, minus_di = self.trend.calculate_adx(high, low, close, period=14)
        trend_strength = adx.iloc[-1] if len(adx) > 0 else 0
        
        # ========== প্রাইস অ্যাকশন ==========
        
        # 1. বর্তমান ক্যান্ডেল
        curr_candle = self.price_action.analyze_candle(
            close.iloc[-1], close.iloc[-1],  # প্রকৃত open/close নেই, সিমুলেশনে close ব্যবহার করছি
            high.iloc[-1], low.iloc[-1]
        )
        
        # 2. সাপোর্ট এবং রেজিস্ট্যান্স
        resistance_levels, support_levels = self.price_action.find_support_resistance_levels(
            close.values, window=20
        )
        
        current_price = close.iloc[-1]
        nearest_resistance = resistance_levels[0] if resistance_levels else current_price * 1.02
        nearest_support = support_levels[0] if support_levels else current_price * 0.98
        
        # ========== সিগন্যাল স্কোরিং ==========
        
        score = 0
        signals_count = 0
        
        # মুভিং এভারেজ সিগন্যাল
        if ema_12.iloc[-1] > sma_20.iloc[-1]:
            score += 1
        else:
            score -= 1
        signals_count += 1
        
        # RSI সিগন্যাল
        rsi_value = rsi.iloc[-1]
        if rsi_value < 30:
            score += 1  # ওভারসোল্ড = কিনুন
        elif rsi_value > 70:
            score -= 1  # ওভারবট = বিক্রয় করুন
        signals_count += 1
        
        # MACD সিগন্যাল
        if macd_line.iloc[-1] > signal_line.iloc[-1]:
            score += 1
        else:
            score -= 1
        signals_count += 1
        
        # বলিন্জার ব্যান্ড সিগন্যাল
        if close.iloc[-1] < lower_bb.iloc[-1]:
            score += 1  # নিম্ন ব্যান্ডের নিচে = কিনুন
        elif close.iloc[-1] > upper_bb.iloc[-1]:
            score -= 1  # উপর ব্যান্ডের উপরে = বিক্রয় করুন
        signals_count += 1
        
        # ট্রেন্ড সিগন্যাল
        score += trend_signal
        signals_count += 1
        
        # মোমেন্টাম সিগন্যাল
        score += momentum_signal
        signals_count += 1
        
        # ভলিউম সিগন্যাল
        score += volume_signal
        signals_count += 1
        
        # ========== চূড়ান্ত সিগন্যাল নির্ধারণ করুন ==========
        
        confidence = abs(score) / signals_count if signals_count > 0 else 0
        confidence_percent = int(confidence * 100)
        
        if score >= 4:
            signal = "STRONG_BUY"
            direction = "CALL"
        elif score >= 2:
            signal = "BUY"
            direction = "CALL"
        elif score <= -4:
            signal = "STRONG_SELL"
            direction = "PUT"
        elif score <= -2:
            signal = "SELL"
            direction = "PUT"
        else:
            signal = "NEUTRAL"
            direction = "HOLD"
        
        # ========== ঝুঁকি/পুরস্কার অনুপাত ==========
        
        risk = abs(current_price - nearest_support)
        reward = abs(nearest_resistance - current_price)
        risk_reward_ratio = reward / risk if risk > 0 else 0
        
        # ========== বিস্তারিত তথ্য সংকলন করুন ==========
        
        details = {
            "current_price": round(current_price, 4),
            "nearest_support": round(nearest_support, 4),
            "nearest_resistance": round(nearest_resistance, 4),
            "risk_reward_ratio": round(risk_reward_ratio, 2),
            
            "indicators": {
                "sma_20": round(sma_20.iloc[-1], 4) if len(sma_20) > 0 else None,
                "ema_12": round(ema_12.iloc[-1], 4) if len(ema_12) > 0 else None,
                "rsi": round(rsi_value, 2),
                "macd": round(macd_line.iloc[-1], 4) if len(macd_line) > 0 else None,
                "macd_signal": round(signal_line.iloc[-1], 4) if len(signal_line) > 0 else None,
                "bb_upper": round(upper_bb.iloc[-1], 4) if len(upper_bb) > 0 else None,
                "bb_lower": round(lower_bb.iloc[-1], 4) if len(lower_bb) > 0 else None,
            },
            
            "trend": {
                "direction": trend_name,
                "strength": round(trend_strength, 2),
                "momentum": round(momentum.iloc[-1], 2) if len(momentum) > 0 else 0,
                "volume_trend": volume_analysis["trend"],
                "volume_current": int(volume_analysis["current_volume"]),
                "volume_avg": int(volume_analysis["avg_volume"]),
            }
        }
        
        return {
            "pair": pair_name,
            "signal": signal,
            "direction": direction,
            "confidence": confidence_percent,
            "score": score,
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": details
        }
    
    def generate_signals_batch(self, pairs_data_dict):
        """
        একাধিক পেয়ারের জন্য সিগন্যাল তৈরি করুন
        pairs_data_dict: {"PAIR1": df1, "PAIR2": df2, ...}
        """
        signals = []
        
        for pair_name, df in pairs_data_dict.items():
            signal = self.analyze_pair(df, pair_name)
            signals.append(signal)
        
        # শক্তিশালী সিগন্যাল দিয়ে সর্টিং করুন
        signals.sort(key=lambda x: x["confidence"], reverse=True)
        
        return signals

def format_signal_output(signal):
    """
    সুন্দর সিগন্যাল আউটপুট ফরম্যাট করুন
    """
    
    emoji_map = {
        "STRONG_BUY": "🟢🟢🟢",
        "BUY": "🟢🟢",
        "SELL": "🔴🔴",
        "STRONG_SELL": "🔴🔴🔴",
        "NEUTRAL": "⚪"
    }
    
    emoji = emoji_map.get(signal["signal"], "⚪")
    
    output = f"""
    ╔════════════════════════════════════╗
    ║  {emoji} {signal['pair']} - {signal['signal']}
    ║  আত্মবিশ্বাস: {signal['confidence']}% | দিক: {signal['direction']}
    ║  মূল্য: {signal['details']['current_price']}
    ║  সাপোর্ট: {signal['details']['nearest_support']} | রেজিস্ট্যান্স: {signal['details']['nearest_resistance']}
    ║  R/R Ratio: {signal['details']['risk_reward_ratio']}
    ║  RSI: {signal['details']['indicators']['rsi']}
    ║  ট্রেন্ড: {signal['details']['trend']['direction']} (শক্তি: {signal['details']['trend']['strength']})
    ╚════════════════════════════════════╝
    """
    
    return output

print("✅ Signal Generator Module Loaded")

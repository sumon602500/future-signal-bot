#!/usr/bin/env python3
"""
Data Fetcher Module
ফ্রি API থেকে রিয়েল মার্কেট ডাটা ফেচ করুন
ব্যবহার করছি: YFinance, CoinGecko, Alpha Vantage
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

class DataFetcher:
    """রিয়েল মার্কেট ডাটা ফেচ করার ক্লাস"""
    
    def __init__(self):
        self.session = requests.Session()
        self.timeout = 10
    
    # ========== YFINANCE ডাটা ==========
    @staticmethod
    def fetch_yfinance_data(symbol, period="5d", interval="1h"):
        """
        YFinance থেকে ডাটা ফেচ করুন
        symbol: "EURUSD=X", "BTCUSD" ইত্যাদি
        period: "5d", "1mo", "3mo" ইত্যাদি
        interval: "1m", "5m", "15m", "1h", "1d"
        """
        try:
            url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={int((datetime.now() - timedelta(days=30)).timestamp())}&period2={int(datetime.now().timestamp())}&interval={interval}&events=history"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                if len(lines) > 1:
                    # CSV পার্স করুন
                    data = []
                    headers = lines[0].split(',')
                    for line in lines[1:]:
                        values = line.split(',')
                        if len(values) == len(headers):
                            data.append(dict(zip(headers, values)))
                    
                    return pd.DataFrame(data)
        except Exception as e:
            print(f"YFinance Error: {e}")
        
        return None
    
    # ========== COINGECKO ডাটা (ক্রিপ্টো) ==========
    @staticmethod
    def fetch_coingecko_data(coin_id, days=30, vs_currency="usd"):
        """
        CoinGecko থেকে ক্রিপ্টো ডাটা ফেচ করুন
        coin_id: "bitcoin", "ethereum" ইত্যাদি
        """
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
            params = {
                "vs_currency": vs_currency,
                "days": days,
                "interval": "daily"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                prices = data.get('prices', [])
                volumes = data.get('volumes', [])
                
                df_data = []
                for price, volume in zip(prices, volumes):
                    df_data.append({
                        'timestamp': datetime.fromtimestamp(price[0]/1000),
                        'close': price[1],
                        'volume': volume[1]
                    })
                
                return pd.DataFrame(df_data)
        except Exception as e:
            print(f"CoinGecko Error: {e}")
        
        return None
    
    # ========== ALPHA VANTAGE ডাটা ==========
    @staticmethod
    def fetch_alpha_vantage_data(symbol, api_key="demo", interval="60min"):
        """
        Alpha Vantage থেকে ডাটা ফেচ করুন
        ফ্রি API কী: "demo" (সীমিত)
        রিয়েল API কী পেতে: https://www.alphavantage.co/
        """
        try:
            if interval == "daily":
                url = f"https://www.alphavantage.co/query"
                params = {
                    "function": "TIME_SERIES_DAILY",
                    "symbol": symbol,
                    "apikey": api_key,
                    "outputsize": "compact"
                }
            else:
                url = f"https://www.alphavantage.co/query"
                params = {
                    "function": "TIME_SERIES_INTRADAY",
                    "symbol": symbol,
                    "interval": interval,
                    "apikey": api_key,
                    "outputsize": "compact"
                }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # সঠিক কী খুঁজুন
                time_series_key = None
                for key in data.keys():
                    if "Time Series" in key:
                        time_series_key = key
                        break
                
                if time_series_key and time_series_key in data:
                    time_series = data[time_series_key]
                    df_data = []
                    
                    for timestamp, values in time_series.items():
                        df_data.append({
                            'timestamp': timestamp,
                            'open': float(values.get('1. open', 0)),
                            'high': float(values.get('2. high', 0)),
                            'low': float(values.get('3. low', 0)),
                            'close': float(values.get('4. close', 0)),
                            'volume': float(values.get('5. volume', 0))
                        })
                    
                    return pd.DataFrame(df_data)
        except Exception as e:
            print(f"Alpha Vantage Error: {e}")
        
        return None
    
    # ========== সিমুলেটেড ডাটা (ফল্ব্যাক) ==========
    @staticmethod
    def generate_sample_data(symbol, periods=100, start_price=100):
        """
        টেস্টিং এর জন্য সিমুলেটেড ডাটা তৈরি করুন
        (যখন API কাজ না করে)
        """
        data = []
        current_price = start_price
        
        for i in range(periods):
            # র্যান্ডম ওয়াক
            change = np.random.randn() * 2
            current_price += change
            
            open_price = current_price - np.random.rand() * 2
            high = max(current_price, open_price) + np.random.rand() * 1
            low = min(current_price, open_price) - np.random.rand() * 1
            volume = np.random.randint(1000000, 10000000)
            
            data.append({
                'timestamp': datetime.now() - timedelta(hours=periods-i),
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(current_price, 2),
                'volume': volume
            })
        
        return pd.DataFrame(data)
    
    # ========== সাধারণ ইন্টারফেস ==========
    def get_ohlcv_data(self, symbol, data_source="yfinance", **kwargs):
        """
        OHLCV ডাটা পান (Open, High, Low, Close, Volume)
        """
        if data_source == "yfinance":
            return self.fetch_yfinance_data(symbol, **kwargs)
        elif data_source == "coingecko":
            return self.fetch_coingecko_data(symbol, **kwargs)
        elif data_source == "alpha_vantage":
            api_key = kwargs.get("api_key", "demo")
            return self.fetch_alpha_vantage_data(symbol, api_key=api_key, **kwargs)
        elif data_source == "sample":
            return self.generate_sample_data(symbol, **kwargs)
        else:
            return self.generate_sample_data(symbol)

# সাধারণ ফরেক্স পেয়ার ম্যাপিং
FOREX_PAIRS = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "USDJPY=X",
    "USDCAD": "USDCAD=X",
    "AUDUSD": "AUDUSD=X",
    "NZDUSD": "NZDUSD=X",
}

# ক্রিপ্টো পেয়ার ম্যাপিং
CRYPTO_PAIRS = {
    "BTCUSD": "bitcoin",
    "ETHUSD": "ethereum",
    "LTCUSD": "litecoin",
    "BNBUSD": "binancecoin",
    "XRPUSD": "ripple",
}

# মেটাল পেয়ার ম্যাপিং
METAL_PAIRS = {
    "XAUUSD": "GC=F",  # সোনা
    "XAGUSD": "SI=F",  # রূপা
}

print("✅ Data Fetcher Module Loaded")

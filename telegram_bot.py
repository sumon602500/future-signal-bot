#!/usr/bin/env python3
import requests
from datetime import datetime
from telegram_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, USE_EMOJI, LOG_FILE

class TelegramBot:
    def __init__(self, bot_token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    def send_message(self, text, parse_mode="HTML"):
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }
            response = requests.post(self.api_url, json=payload, timeout=10)
            if response.status_code == 200:
                self._log("✅ বার্তা সফলভাবে পাঠানো হয়েছে")
                return True
            else:
                self._log(f"❌ Error: {response.status_code}")
                return False
        except Exception as e:
            self._log(f"❌ Exception: {str(e)}")
            return False
    
    def send_signals_summary(self, signals, market, filter_name, time_window):
        try:
            if not signals:
                message = f"<b>❌ No Signals Generated</b>\nMarket: {market}\nFilter: {filter_name}"
                return self.send_message(message, parse_mode="HTML")
            
            message = (
                f"<b>📊 FUTURE SIGNAL - BATCH REPORT</b>\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"<b>Market:</b> {market}\n"
                f"<b>Filter:</b> {filter_name}\n"
                f"<b>Time Window:</b> {time_window}\n"
                f"<b>Generated:</b> {datetime.now().strftime('%d %b %Y | %H:%M:%S')}\n"
                f"━━━━━━━━━━━━━━━━━━━\n\n"
                f"<b>📈 Total Signals: {len(signals)}</b>\n\n"
            )
            
            for idx, signal in enumerate(signals, 1):
                pair = signal.get("pair", "N/A")
                direction = signal.get("direction", "N/A")
                time_str = signal.get("time", "N/A")
                direction_emoji = "📈" if direction == "CALL" else "📉"
                message += f"<b>{idx}.</b> <code>{pair}</code> → {direction_emoji} <b>{direction}</b> @ <code>{time_str}</code>\n"
            
            message += (
                f"\n━━━━━━━━━━━━━━━━━━━\n"
                f"✅ All signals passed quality filter\n"
                f"📞 Support: @MD_SUMON_MT4\n"
                f"📱 Channel: t.me/FUTURE_SIGNAL11"
            )
            return self.send_message(message, parse_mode="HTML")
        except Exception as e:
            self._log(f"❌ Error: {str(e)}")
            return False
    
    def _log(self, message):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
            print(message)
        except Exception as e:
            print(f"Log Error: {e}")

telegram_bot = TelegramBot()

def send_telegram_signals_summary(signals, market, filter_name, time_window):
    return telegram_bot.send_signals_summary(signals, market, filter_name, time_window)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.send_message("<b>🧪 Test</b>\nTelegram Bot ✅ Working!")

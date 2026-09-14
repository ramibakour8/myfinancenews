import os
import re
import asyncio
import yfinance as yf

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


# =========================
# SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")


# الصفقات المفتوحة
active_trades = {}


# =========================
# PARSE RECOMMENDATION
# =========================

def parse_trade(text):
    if not text:
        return None

    text_upper = text.upper()

    # BUY / SELL
    direction_match = re.search(r"\b(BUY|SELL)\b", text_upper)
    if not direction_match:
        return None

    direction = direction_match.group(1)

    # GOLD / XAU / XAUUSD
    if not any(x in text_upper for x in ["GOLD", "XAU", "XAUUSD"]):
        return None

    # Entry
    entry_match = re.search(
        r"(?:👉\s*)?(\d{3,5}(?:\.\d+)?)",
        text
    )

    if not entry_match:
        return None

    entry = float(entry_match.group(1))

    # TP1
    tp1_match = re.search(
        r"TP\s*1\s*[:\-]?\s*(\d{3,5}(?:\.\d+)?)",
        text_upper
    )

    # TP2
    tp2_match = re.search(
        r"TP\s*2\s*[:\-]?\s*(\d{3,5}(?:\.\d+)?)",
        text_upper
    )

    # SL
    sl_match = re.search(
        r"SL\s*[:\-]?\s*(\d{3,5}(?:\.\d+)?)",
        text_upper
    )

    if not tp1_match or not sl_match:
        return None

    tp1 = float(tp1_match.group(1))
    tp2 = float(tp2_match.group(1)) if tp2_match else None
    sl = float(sl_match.group(1))

    return {
        "direction": direction,
        "symbol": "GOLD",
        "entry": entry,
        "tp1": tp1,
        "tp2": tp2,
        "sl": sl,
        "tp1_hit": False,
        "tp2_hit": False,
        "sl_hit": False,
    }


# =========================
# GET GOLD PRICE
# =========================

def get_gold_price():
    try:
        ticker = yf.Ticker("GC=F")
        price = ticker.fast_info.get("last_price")

        if price:
            return float(price)

    except Exception as e:
        print("Price error:", e)

    return None


# =========================
# CHECK TRADE
# =========================

async def check_trades(context: ContextTypes.DEFAULT_TYPE):

    if not active_trades:
        return

    price = get_gold_price()

    if price is None:
        return

    print("Gold price:", price)

    for key, trade in list(active_trades.items()):

        direction = trade["direction"]

        # =========================
        # BUY
        # =========================

        if direction == "BUY":

            # TP1
            if not trade["tp1_hit"] and price >= trade["tp1"]:

                trade["tp1_hit"] = True

                try:
                    await context.bot.edit_message_text(
                        chat_id=key[0],
                        message_id=key[1],
                        text=(
                            f"BUY GOLD\n"
                            f"👉 {trade['entry']}\n"
                            f"🟢TP1: {trade['tp1']} ✅\n"
                            f"🟢TP2: {trade['tp2'] if trade['tp2'] else '-'} ⏳\n"
                            f"⛔️SL: {trade['sl']}"
                        )
                    )
                except Exception as e:
                    print("Edit error:", e)

            # TP2
            if (
                trade["tp2"]
                and
                trade["tp1_hit"]
                and
                not trade["tp2_hit"]
                and
                price >= trade["tp2"]
            ):

                trade["tp2_hit"] = True

                try:
                    await context.bot.edit_message_text(
                        chat_id=key[0],
                        message_id=key[1],
                        text=(
                            f"BUY GOLD\n"
                            f"👉 {trade['entry']}\n"
                            f"🟢TP1: {trade['tp1']} ✅\n"
                            f"🟢TP2: {trade['tp2']} ✅\n"
                            f"⛔️SL: {trade['sl']}"
                        )
                    )
                except Exception as e:
                    print("Edit error:", e)

                del active_trades[key]
                continue

            # SL
            if not trade["sl_hit"] and price <= trade["sl"]:

                trade["sl_hit"] = True

                try:
                    await context.bot.edit_message_text(
                        chat_id=key[0],
                        message_id=key[1],
                        text=(
                            f"BUY GOLD\n"
                            f"👉 {trade['entry']}\n"
                            f"🟢TP1: {trade['tp1']} "
                            f"{'✅' if trade['tp1_hit'] else '❌'}\n"
                            f"🟢TP2: {trade['tp2'] if trade['tp2'] else '-'}\n"
                            f"⛔️SL: {trade['sl']} ❌"
                        )
                    )
                except Exception as e:
                    print("Edit error:", e)

                del active_trades[key]


        # =========================
        # SELL
        # =========================

        elif direction == "SELL":

            # TP1
            if not trade["tp1_hit"] and price <= trade["tp1"]:

                trade["tp1_hit"] = True

                try:
                    await context.bot.edit_message_text(
                        chat_id=key[0],
                        message_id=key[1],
                        text=(
                            f"SELL GOLD\n"
                            f"👉 {trade['entry']}\n"
                            f"🟢TP1: {trade['tp1']} ✅\n"
                            f"🟢TP2: {trade['tp2'] if trade['tp2'] else '-'} ⏳\n"
                            f"⛔️SL: {trade['sl']}"
                        )
                    )
                except Exception as e:
                    print("Edit error:", e)

            # TP2
            if (
                trade["tp2"]
                and
                trade["tp1_hit"]
                and
                not trade["tp2_hit"]
                and
                price <= trade["tp2"]
            ):

                trade["tp2_hit"] = True

                try:
                    await context.bot.edit_message_text(
                        chat_id=key[0],
                        message_id=key[1],
                        text=(
                            f"SELL GOLD\n"
                            f"👉 {trade['entry']}\n"
                            f"🟢TP1: {trade['tp1']} ✅\n"
                            f"🟢TP2: {trade['tp2']} ✅\n"
                            f"⛔️SL: {trade['sl']}"
                        )
                    )
                except Exception as e:
                    print("Edit error:", e)

                del active_trades[key]
                continue

            # SL
            if not trade["sl_hit"] and price >= trade["sl"]:

                trade["sl_hit"] = True

                try:
                    await context.bot.edit_message_text(
                        chat_id=key[0],
                        message_id=key[1],
                        text=(
                            f"SELL GOLD\n"
                            f"👉 {trade['entry']}\n"
                            f"🟢TP1: {trade['tp1']} "
                            f"{'✅' if trade['tp1_hit'] else '❌'}\n"
                            f"🟢TP2: {trade['tp2'] if trade['tp2'] else '-'}\n"
                            f"⛔️SL: {trade['sl']} ❌"
                        )
                    )
                except Exception as e:
                    print("Edit error:", e)

                del active_trades[key]


# =========================
# NEW TELEGRAM MESSAGE
# =========================

async def new_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.channel_post

    if not message or not message.text:
        return

    trade = parse_trade(message.text)

    if not trade:
        return

    key = (
        message.chat.id,
        message.message_id
    )

    active_trades[key] = trade

    print("NEW TRADE:", trade)


# =========================
# START BOT
# =========================

def main():

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST,
            new_message
        )
    )

    application.job_queue.run_repeating(
        check_trades,
        interval=15,
        first=10
    )

    print("Trade bot started...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()

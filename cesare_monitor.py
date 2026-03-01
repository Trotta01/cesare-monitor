import asyncio
import aiohttp
import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# CONFIG - MODIFICA
MONITOR_TOKEN = "8636882217:AAHpPBwS6_Qbb4KIM5enrsgtzoku3pBa3_M"
GROUP_CHAT_ID = -1003078713466
OFFLINE_STICKER = "CAACAgQAAxkBAAEQpnJppASLZc9lzdQqbIoQXwMltjR_dAAC8h0AAqk5IFHx-i33-nbh0DoE"
ONLINE_STICKER = "CAACAgQAAxkBAAEQpnRppAT16OxIp6u00djb3F-AAuiv3gACKCAAAvrNIFHPf12iheKncjoE"
STATUS_FILE_URL = "https://TUO_GIST_O_REPLIT_RAW_URL/bot_status.json"  # Crea Gist o file pubblico

was_online = True

async def check_cesare():
    global was_online
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(STATUS_FILE_URL, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                status = await resp.json()
        is_online = status.get("is_online", False)
        if was_online and not is_online:
            print("🚨 Cesare OFFLINE!")
            bot = Application.builder().token(MONITOR_TOKEN).build().bot
            await bot.send_sticker(GROUP_CHAT_ID, OFFLINE_STICKER)
            await bot.send_message(GROUP_CHAT_ID, "🚨 Cesare è andato in crash!")
        was_online = is_online
        return is_online
    except Exception as e:
        print(f"Errore check: {e}")
        return False

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = "🟢 ONLINE" if await check_cesare() else "🔴 OFFLINE"
    await update.message.reply_text(f"Cesare: {status}")

async def test_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    await bot.send_sticker(GROUP_CHAT_ID, OFFLINE_STICKER)
    await update.message.reply_text("🧪 Sticker test inviato!")

async def monitor_loop(application: Application):
    while True:
        await check_cesare()
        await asyncio.sleep(30)

async def main():
    app = Application.builder().token(MONITOR_TOKEN).build()
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("test", test_cmd))

    # Avvia monitor in background
    asyncio.create_task(monitor_loop(app))

    print("🟢 Monitor Cesare attivo! /status o /test")
    await app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
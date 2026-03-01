import asyncio
import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

MONITOR_TOKEN = "8636882217:AAHpPBwS6_Qbb4KIM5enrsgtzoku3pBa3_M"
GROUP_CHAT_ID = -1003078713466
OFFLINE_STICKER = "CAACAgQAAxkBAAEQpnJppASLZc9lzdQqbIoQXwMltjR_dAAC8h0AAqk5IFHx-i33-nbh0DoE"
STATUS_FILE_URL = "https://gist.githubusercontent.com/Trotta01/a1b054dd232743b33523184250ff970c/raw/2e35c3f16c1d8267311773a9d26998534e7bdc0d/gistfile1.txt"

was_online = True


async def check_cesare():
    global was_online
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(
                total=10)) as session:
            async with session.get(STATUS_FILE_URL) as resp:
                status = await resp.json()
        is_online = status.get("is_online", False)
        if was_online and not is_online:
            print("🚨 Cesare OFFLINE!")
            await asyncio.sleep(1)  # Anti-flood
            bot = Application.builder().token(MONITOR_TOKEN).build().bot
            await bot.send_sticker(GROUP_CHAT_ID, OFFLINE_STICKER)
            await bot.send_message(GROUP_CHAT_ID,
                                   "🚨 Cesare è andato in crash!")
        was_online = is_online
        return is_online
    except:
        return False


async def status_cmd(update: Update, context):
    status = "🟢 ONLINE" if await check_cesare() else "🔴 OFFLINE"
    await update.message.reply_text(f"Cesare: {status}")


async def test_cmd(update: Update, context):
    await context.bot.send_sticker(GROUP_CHAT_ID, OFFLINE_STICKER)
    await update.message.reply_text("🧪 Test OK!")


async def main():
    app = Application.builder().token(MONITOR_TOKEN).build()
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("test", test_cmd))

    # Timer check ogni 30s (no loop infinito)
    async def periodic_check():
        while True:
            await check_cesare()
            await asyncio.sleep(30)

    check_task = asyncio.create_task(periodic_check())

    print("🟢 Monitor LIVE - Test /status!")
    await app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Stopped")

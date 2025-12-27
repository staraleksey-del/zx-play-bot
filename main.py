# main.py — ЧИСТАЯ ВЕРСИЯ БЕЗ FLASK
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GAMES = [
    {"name": "Manic Miner", "url": "https://zx-games.ru/play/manic-miner/"},
    {"name": "Jet Set Willy", "url": "https://zx-games.ru/play/jet-set-willy/"},
    {"name": "Chuckie Egg", "url": "https://zx-games.ru/play/chuckie-egg/"},
    {"name": "Saboteur!", "url": "https://zx-games.ru/play/saboteur/"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(g["name"], callback_data=f'play_{i}')] for i, g in enumerate(GAMES)]
    keyboard.append([InlineKeyboardButton("🔄 Обновить", callback_data="refresh")])
    await update.message.reply_text(
        "🎮 Добро пожаловать в **zx_play_bot**!\nВыберите игру ZX Spectrum:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "refresh":
        await start(query, context)
        return
    try:
        game = GAMES[int(query.data.split('_')[1])]
        await query.edit_message_text(
            f"🚀 *{game['name']}*\n[Играть]({game['url']})\n\nКурсоры + пробел.",
            parse_mode="Markdown"
        )
    except (IndexError, ValueError):
        await query.edit_message_text("❌ Ошибка. Напишите /start.")

if __name__ == "__main__":
    # Безопасное получение токена — удаляем ВСЕ пробелы
    BOT_TOKEN = "".join(os.environ["BOT_TOKEN"].split())
    WEBHOOK_URL = os.environ["WEBHOOK_URL"].rstrip("/")

    logger.info("✅ Запуск бота...")
    logger.info(f"Webhook URL: {WEBHOOK_DIR}/{BOT_TOKEN[:10]}...")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(game_handler))

    # Запуск ЧЕРЕЗ ВСТРОЕННЫЙ СЕРВЕР (tornado), без Flask!
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
        url_path=BOT_TOKEN  # <-- это создаёт endpoint /ваш_токен
    )

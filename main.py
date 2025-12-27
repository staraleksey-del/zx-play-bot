# main.py
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Игры ZX Spectrum
GAMES = [
    {"name": "Manic Miner", "url": "https://zx-games.ru/play/manic-miner/"},
    {"name": "Jet Set Willy", "url": "https://zx-games.ru/play/jet-set-willy/"},
    {"name": "Chuckie Egg", "url": "https://zx-games.ru/play/chuckie-egg/"},
    {"name": "Saboteur!", "url": "https://zx-games.ru/play/saboteur/"},
    {"name": "Atic Atac", "url": "https://zx-games.ru/play/atic-atac/"},
    {"name": "Dizzy: The Egg of Columbus", "url": "https://zx-games.ru/play/dizzy-the-egg-of-columbus/"},
    {"name": "Lode Runner", "url": "https://zx-games.ru/play/lode-runner/"},
    {"name": "The Hobbit", "url": "https://zx-games.ru/play/the-hobbit/"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(game["name"], callback_data=f'play_{i}')]
        for i, game in enumerate(GAMES)
    ]
    # Добавим кнопку "Обновить список" на случай, если сообщение устарело
    keyboard.append([InlineKeyboardButton("🔄 Обновить список", callback_data="refresh")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎮 Добро пожаловать в **zx_play_bot**!\n"
        "Выберите классическую игру ZX Spectrum для запуска в браузере:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "refresh":
        await start(query, context)
        return

    try:
        game_index = int(query.data.split('_')[1])
        game = GAMES[game_index]
        await query.edit_message_text(
            f"🚀 Запускаю *{game['name']}*!\n\n"
            f"👉 [Играть сейчас в браузере]({game['url']})\n\n"
            "💡 Управление: курсоры + пробел (иногда Z/X). Работает на PC и мобильных!",
            parse_mode="Markdown",
            disable_web_page_preview=False
        )
    except (IndexError, ValueError, KeyError):
        await query.edit_message_text("❌ Ошибка. Напишите /start для нового меню.")

# Health-check для Render
from flask import Flask
app_flask = Flask(__name__)

@app_flask.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

    if not BOT_TOKEN or not WEBHOOK_URL:
        raise RuntimeError("❗ Установите BOT_TOKEN и WEBHOOK_URL в переменных окружения.")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(game_handler))

    port = int(os.environ.get("PORT", 10000))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=BOT_TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )
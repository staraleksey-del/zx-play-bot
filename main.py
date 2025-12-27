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

# === Настройка логирования ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Список игр ===
GAMES = [
    {"name": "Manic Miner", "url": "https://zx-games.ru/play/manic-miner/"},
    {"name": "Jet Set Willy", "url": "https://zx-games.ru/play/jet-set-willy/"},
    {"name": "Chuckie Egg", "url": "https://zx-games.ru/play/chuckie-egg/"},
    {"name": "Saboteur!", "url": "https://zx-games.ru/play/saboteur/"},
    {"name": "Atic Atac", "url": "https://zx-games.ru/play/atic-atac/"},
]

# === Обработчики ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(game["name"], callback_data=f'play_{i}')]
        for i, game in enumerate(GAMES)
    ]
    keyboard.append([InlineKeyboardButton("🔄 Обновить", callback_data="refresh")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎮 Добро пожаловать в **zx_play_bot**!\nВыберите игру ZX Spectrum:",
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
        idx = int(query.data.split('_')[1])
        game = GAMES[idx]
        await query.edit_message_text(
            f"🚀 *{game['name']}*\n[Играть]({game['url']})\n\nКурсоры + пробел.",
            parse_mode="Markdown"
        )
    except:
        await query.edit_message_text("❌ Ошибка. Напишите /start.")

# === Запуск ===
if __name__ == "__main__":
    # Безопасное получение и очистка токена
    BOT_TOKEN = "".join(os.environ["BOT_TOKEN"].split())  # удаляет ВСЕ пробелы и переносы
    WEBHOOK_URL = os.environ["WEBHOOK_URL"].rstrip("/")

    logger.info(f"Запуск бота с webhook: {WEBHOOK_URL}/{BOT_TOKEN[:10]}...")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(game_handler))

    port = int(os.environ.get("PORT", 10000))
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
        url_path=BOT_TOKEN
    )

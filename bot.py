"""
bot.py — Бот мессенджера для сервиса АудиоСервис
Библиотека: python-telegram-bot >= 20.0
Установка:  pip install python-telegram-bot
Запуск:     python bot.py
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ── Настройки ─────────────────────────────────────────────────────────────────

TOKEN    = "8720934363:AAFQhKcr9iAsDykPq1J7uJFIIKq3w4hb4PM"
SITE_URL = "https://loca.lt"

# ── Тексты сообщений ──────────────────────────────────────────────────────────

TEXT_WELCOME = (
    "👋 Привет! Я бот сервиса *АудиоСервис*.\n\n"
    "Здесь ты можешь:\n"
    "• Узнать, что умеет наш сайт\n"
    "• Перейти на сайт и послушать свою музыку прямо в браузере\n\n"
    "Выбери действие 👇"
)

TEXT_SITE_INFO = (
    "🎵 *АудиоСервис — веб-плеер прямо в браузере*\n\n"
    "Что умеет сайт:\n"
    "• Загрузка WAV / MP3 / OGG с твоего устройства\n"
    "• Встроенный плеер: Play, Pause, Stop, перемотка\n"
    "• Регулировка громкости\n"
    "• Файлы *не загружаются на сервер* — всё остаётся у тебя\n"
    "• Адаптивный дизайн: работает на телефоне и ПК\n\n"
    "Нажми кнопку ниже, чтобы открыть сайт 👇"
)

# ── Клавиатуры ────────────────────────────────────────────────────────────────

def keyboard_main() -> InlineKeyboardMarkup:
    """Главная Inline-клавиатура: О сайте + Перейти на сайт."""
    buttons = [
        [
            InlineKeyboardButton("О сайте 📋",        callback_data="site_info"),
            InlineKeyboardButton("Перейти на сайт 🌐", url=SITE_URL),
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def keyboard_go_to_site() -> InlineKeyboardMarkup:
    """Клавиатура с единственной кнопкой перехода на сайт."""
    buttons = [
        [InlineKeyboardButton("Открыть сайт 🌐", url=SITE_URL)]
    ]
    return InlineKeyboardMarkup(buttons)

# ── Обработчики ───────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start — приветственное сообщение."""
    await update.message.reply_text(
        text=TEXT_WELCOME,
        parse_mode="Markdown",
        reply_markup=keyboard_main(),
    )


async def button_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий Inline-кнопок."""
    query = update.callback_query
    await query.answer()  # убираем индикатор загрузки на кнопке

    if query.data == "site_info":
        await query.edit_message_text(
            text=TEXT_SITE_INFO,
            parse_mode="Markdown",
            reply_markup=keyboard_go_to_site(),
        )

# ── Точка запуска ─────────────────────────────────────────────────────────────

def main() -> None:
    """Сборка и запуск бота."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()


if __name__ == "__main__":
    main()

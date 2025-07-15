
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Загрузка данных
with open("products.json", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

# Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(cat.title(), callback_data=f"cat_{cat}")]
        for cat in PRODUCTS.keys()
    ]
    keyboard.append([InlineKeyboardButton("ℹ️ О магазине", callback_data="about")])
    await update.message.reply_text("👋 Добро пожаловать в магазин Social Sh!\nВыберите категорию:", reply_markup=InlineKeyboardMarkup(keyboard))

# Обработка категорий и карточек товаров
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("cat_"):
        category = query.data[4:]
        items = PRODUCTS.get(category, [])
        if not items:
            await query.edit_message_text(f"Категория «{category.title()}» пока пуста.")
            return
        for item in items:
            text = f"{item['title']}\n💵 Цена: {item['price']}\n📏 Размеры: {item['sizes']}"
            button = InlineKeyboardMarkup([[InlineKeyboardButton("🛒 Купить на Авито", url=item['link'])]])
            await query.message.reply_text(text, reply_markup=button)
    elif query.data == "about":
        await query.edit_message_text(
            "🧥 Магазин одежды Social Sh\n"
            "📍 Стильная одежда по лучшим ценам\n"
            "🚚 Доставка по всей России\n"
            "📲 Все покупки через Авито — удобно и безопасно!\n\n"
            "Спасибо, что выбираете нас! ❤️"
        )

# Запуск бота
def main():
    TOKEN = "7824900331:AAHjSDlnNElq8hjbRyI6o6YLvN6F6HrXQ5c"  # <-- Замените на свой токен от BotFather
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()

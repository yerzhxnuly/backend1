from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from bot.models import Product

TELEGRAM_TOKEN = 'ВАШ_ТОКЕН'
bot = Bot(token=TELEGRAM_TOKEN)

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        update = Update.de_json(request.json, bot)
        dispatcher = Dispatcher(bot, None, use_context=True)

        # Команда для просмотра товаров
        def view_products(update, context):
            products = Product.objects.all()
            response = "\n".join([f"{p.id}: {p.name} - {p.price}" for p in products])
            update.message.reply_text(response if response else "Товары отсутствуют.")

        # Команда для добавления товара
        def add_product(update, context):
            try:
                name, price = context.args
                product = Product.objects.create(name=name, price=float(price))
                update.message.reply_text(f"Товар {product.name} добавлен!")
            except Exception as e:
                update.message.reply_text("Ошибка: Убедитесь, что вы указали имя и цену.")

        dispatcher.add_handler(CommandHandler("view_products", view_products))
        dispatcher.add_handler(CommandHandler("add_product", add_product))

        dispatcher.process_update(update)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "not ok"})


import telebot
from telebot import types
import time
import logging

# Замените 'YOUR_BOT_TOKEN' на ваш токен бота
BOT_TOKEN = '8114121009:AAHzdL2L70WR9mTPtZ5nloNHfSLG_JAuNvk'

bot = telebot.TeleBot(BOT_TOKEN)

# Кнопка для покупки товара
buy_button = types.KeyboardButton("❤️ купить товар ❤️")
# Создаем клавиатуру с кнопкой покупки
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
main_keyboard.add(buy_button)

# Храним информацию о выбранных товарах и пользователях
users_data = {}

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='a',
          format='%(asctime)s - %(levelname)s - %(message)s')

@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_id = message.chat.id
  username = message.from_user.username
  
  # Проверка наличия юзернейма
  if not username:
    bot.send_message(
      user_id,
      "⚠️ У вас нет юзернейма! Пожалуйста, установите его в настройках Telegram, чтобы продолжить.",
      reply_markup=None
    )
    return # Выход из обработчика, чтобы пользователь мог установить юзернейм
  
  bot.send_message(
    user_id,
    """
Приветствуем тебя  в KitanovShop! тут ты можешь приобрести нужные тебе товары по самым низким ценам.
почему цены такие низкие? наш магазин делает МАЛЕЙШУЮ наценку в отличии других продавьцов.

Приятных покупок!

Выбирай  нужный тебе товар по кнопке
ниже:
    """,
    reply_markup=main_keyboard
  )

@bot.message_handler(func=lambda message: message.text == "❤️ купить товар ❤️")
def handle_buy(message):
  bot.send_message(
    message.chat.id,
    "Выберите товар:",
    reply_markup=generate_buy_keyboard()
  )

# Функция для создания клавиатуры с товарами
def generate_buy_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # Физ. номера
    keyboard.add(types.KeyboardButton("⚠️новорег физ\n0.85$"))
    keyboard.add(types.KeyboardButton("⚠️физ отлега 2г\n2.43$"))
    keyboard.add(types.KeyboardButton("⚠️физ отлега 5лет\n4.35$"))
    keyboard.add(types.KeyboardButton("⚠️физ отлега 6лет\n4.98$"))
    keyboard.add(types.KeyboardButton("⚠️Tdata руФиз новорег\n0.8$"))
    keyboard.add(types.KeyboardButton("⚠️физ отлега год\n1$"))
    # Промокоды
    keyboard.add(types.KeyboardButton("😁КИНОПОИСК 60дней бесплатно\n0.25$"))
    keyboard.add(types.KeyboardButton("😁ИВИ до года бесплатно\n0.30$"))
    keyboard.add(types.KeyboardButton("😁KION 20 дней бесплатно\n0.27$"))
    keyboard.add(types.KeyboardButton("😁ЯНДЕКС ЕДА \n0.4$"))
    # Telegram Premium
    keyboard.add(types.KeyboardButton("⚪️TELEGRAM PREMIUM 1  месяц\n3.55$"))
    keyboard.add(types.KeyboardButton("⚪️TELEGRAM PREMIUM 3 месяца(подарком)\n14$"))
    keyboard.add(types.KeyboardButton("⚪️TEPEGRAM PREMIUM 1 месяц(со входом)\n3.25$"))
    # Чаты
    keyboard.add(types.KeyboardButton("🛡30 папок чатов по разным темам(1200+ чатов)\n1$"))
    keyboard.add(types.KeyboardButton("🛡100 чатов(линк)\n0.25$"))
    keyboard.add(types.KeyboardButton("🛡50 чатов(линк)\n0.15$"))
    keyboard.add(types.KeyboardButton("🛡10 папок чатов(300+)\n0.35$"))
    keyboard.add(types.KeyboardButton("🛡20 папок чатрв(610+)\n0.45$"))
    keyboard.add(types.KeyboardButton("✉️Tdata Telegram accounts от 10шт\n0.5$ за шт"))
    # Скрипты
    keyboard.add(types.KeyboardButton("🖥СКРИПТ по авторассылу(не сносит акки!)\n0.55$"))
    keyboard.add(types.KeyboardButton("🖥СКРИПТ ловецЧеков(большой функционал)\n0.55$"))
    # Skype
    keyboard.add(types.KeyboardButton("скайп с любым балансом\n?$"))
    keyboard.add(types.KeyboardButton("скайп с балансом 5$\n3.5$"))
    keyboard.add(types.KeyboardButton("скайп с балансом 3$\n2.5$"))
    keyboard.add(types.KeyboardButton("скайп с балансом 15$\n6$"))
    keyboard.add(types.KeyboardButton("скайп с балансом 30$\n15$"))
     #звезды тг - ДОБАВЛЕНО
    keyboard.add(types.KeyboardButton("🌟Telegram Stars(50шт)\n1$"))
    return keyboard

@bot.message_handler(func=lambda message: True)
def handle_item(message):
    item_name = message.text
    # Извлекаем цену из текста кнопки
    price = item_name.split("\n")[1].strip("$")
    users_data[message.chat.id] = {
        "item": item_name,
        "price": price
    }
    # Создаем инлайн-клавиатуру с кнопкой "Подтвердить оплату"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Подтвердить оплату", callback_data="confirm_payment"))
    bot.send_message(
        message.chat.id,
        f"""
        {item_name}
        Цена товара: {price}$
        https://t.me/send?start=IVX614wkWXdx
        Оплатите по счету {price}
        ✋ДОБАВЬТЕ В КОММЕНТАРИИ СВОЙ ЮЗЕРНЕЙМ А ИНАЧЕ ТОВАРА НЕ ВЫДАДИМ✋
        """,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "confirm_payment")
def handle_confirm_payment(call):
    user_id = call.message.chat.id
    username = call.message.from_user.username
    item_name = users_data[user_id]["item"]
    price = users_data[user_id]["price"]

    # Проверка наличия юзернейма
    if not username:
        bot.send_message(
            user_id,
            "⚠️ У вас нет юзернейма! Пожалуйста, установите его в настройках Telegram, чтобы продолжить.",
            reply_markup=None
        )
        return  # Выход из обработчика, чтобы пользователь мог установить юзернейм
    
    # Отправляем заявку администратору
    bot.send_message(
        chat_id='510331002', # Замените на ваш ID чата администратора
        text=f"Заявка от @{call.message.from_user.username}\nТовар: {item_name}\nЦена: {price}$",
        reply_markup=generate_admin_keyboard(user_id)
    )
    # Отправляем сообщение пользователю о получении заявки
    bot.send_message(
        user_id,
        "✅ Заявка на расмотрении. Ожидайте подтверждения от администратора."
    )

# Функция для создания клавиатуры администратора
def generate_admin_keyboard(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Принять заявку", callback_data=f"accept_{user_id}"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_"))
def handle_accept_payment(call):
    user_id = int(call.data.split("_")[1])
    # Отправляем сообщение пользователю о подтверждении заявки
    bot.send_message(
        chat_id=user_id,
        text="✅ Ваша заявка принята! для получение товара свяжитесь со мной @kitanova"
    )
    # Удаляем информацию о пользователе из словаря
    users_data.pop(user_id, None)
    # Удаляем кнопку "Принять заявку" из сообщения админа
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

# Основная петля бота
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        time.sleep(1) # Пауза перед повторной попыткой

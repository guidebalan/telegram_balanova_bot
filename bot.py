import telebot
import os
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")  # токен берется из переменных окружения
CHANNEL = "@balanova1"  # замените на ваш канал

bot = telebot.TeleBot(TOKEN)

# Словарь с гайдами
guides = {
    "100 подарков на 2 года": "guides/100gifts-2years.pdf",
    "идеальный горшок": "guides/super-gorshok.pdf",
    "готовимся к малышу": "guides/guide-baby-get-ready.pdf",
    "сумки в роддом и история родов": "guides/birth-bags.pdf",
    "подарки на годик": "guides/guide-present.pdf",
    "50 развивашек своими руками": "guides/guide-entertaiment.pptx.pdf",
    "я не плохая мама. Я просто устала": "guides/relax-mommy.pdf",
    "путешествие с малышом до года": "guides/baby-travel.pdf",
}

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status != 'left'
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for guide_name in guides.keys():
        markup.add(types.KeyboardButton(guide_name))
    bot.send_message(message.chat.id, "Привет! Какой гайд тебя интересует?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in guides.keys())
def send_guide(message):
    guide_file = guides[message.text]
    
    if is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "Спасибо за подписку! Вот твой файл❤️")
        with open(guide_file, "rb") as f:
            bot.send_document(message.chat.id, f)
    else:
        bot.send_message(message.chat.id, f"Пожалуйста, подпишитесь на канал {CHANNEL} и нажмите /start снова.")

bot.infinity_polling()

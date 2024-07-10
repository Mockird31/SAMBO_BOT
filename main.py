from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.async_telebot import AsyncTeleBot
from find_athete import *
import asyncio
import os
TOKEN = os.getenv("TOKEN_SAMBO")

bot = AsyncTeleBot(TOKEN)
print(TOKEN)
user_states = {}

# Define possible states
STATE_NONE = 0
STATE_WAITING_FOR_NAME = 1

@bot.message_handler(func=lambda message: True)
async def check_message(message):
    user_id = message.from_user.id
    user_state = user_states.get(user_id, STATE_NONE)
    mes = message.text.lower()
    
    if mes == "регистрация":
        pass
    elif mes == "найти спортсмена":
        await bot.reply_to(message, "Введите ФИО спортсмена")
        user_states[user_id] = STATE_WAITING_FOR_NAME
    elif user_state == STATE_WAITING_FOR_NAME:
        athlete_info = get_info(mes)
        if athlete_info[1] != None:
            await bot.send_photo(message.chat.id, photo = athlete_info[1], caption=athlete_info[0], parse_mode="Markdown")
        else:
            await bot.send_message(message.chat.id, athlete_info[0], parse_mode="Markdown")
        print(athlete_info)
        user_states[user_id] = STATE_NONE
    else:
        await bot.reply_to(message, "Неизвестная команда")
    

@bot.message_handler(commands=['start'])
async def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_find_sportsman = KeyboardButton("Найти спортсмена")
    btn_register = KeyboardButton("Регистрация")
    markup.add(btn_find_sportsman, btn_register)
    await bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)

@bot.message_handler(commands=['help'])
async def send_welcome(message):
    text = "Бот помогает получить информацию о спортсменах.\nЗарегистрироваться на соревнованиях."
    await bot.reply_to(message, text)

if __name__ == '__main__':
    asyncio.run(bot.polling())



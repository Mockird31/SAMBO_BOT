from aiogram.filters.command import Command, CommandStart
from aiogram import F, Router
from aiogram import types
import emoji

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Найти спортсмена")],
        [types.KeyboardButton(text="Ближайшие соревнования")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите опцию")
    await message.answer("hahahah" + emoji.emojize(":brain:"), reply_markup=keyboard)


@router.message(F.text.lower() == "найти спортсмена")
async def show_sportsman(message: types.Message):
    await message.answer("Как зовут спортсмена?")#, reply_markup=types.ReplyKeyboardRemove)
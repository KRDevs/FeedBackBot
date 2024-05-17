from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_requirements


async def all_requirements():
    requirements = await get_requirements()
    keyboard = InlineKeyboardBuilder()
    for requirement in requirements:
        keyboard.add(InlineKeyboardButton(text=f'{requirement.id}- murojaat',
                                          callback_data=f'requirement_{requirement.id}'))
    return keyboard.adjust(2).as_markup()


def stars():
    kb = [
        [(InlineKeyboardButton(text="⭐️⭐️⭐️⭐️⭐️", callback_data='5'))],
        [(InlineKeyboardButton(text="⭐️⭐️⭐️⭐️", callback_data='4'))],
        [(InlineKeyboardButton(text="⭐️⭐️⭐️", callback_data='3'))],
        [(InlineKeyboardButton(text="⭐️⭐️", callback_data='2'))],
        [(InlineKeyboardButton(text="⭐️", callback_data='1'))]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

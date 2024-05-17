from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def send_number():
    kb = [
        [(KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True))]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def new_requirement():
    kb = [
        [(KeyboardButton(text="🆕 Yangi murojaat yuborish"))]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def back_btn():
    kb = [
        [(KeyboardButton(text="🔙 Orqaga"))]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

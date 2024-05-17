from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram import types
from app.database import requests as rq

from app.keyboards.common_kb import send_number, new_requirement
from app.keyboards.inline_kb import stars

user = Router()


class Process(StatesGroup):
    name = State()
    number = State()
    question = State()
    star = State()
    star2 = State()
    question2 = State()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await rq.add_user(message.from_user.id)
    if not user:
        await message.answer('Botimizga xush kelibsiz!!!\n\nIltimos ismingizni kiriting')
        await state.set_state(Process.name)
    else:
        await message.answer('Xizmatimizni baholang!', reply_markup=stars())
        await state.set_state(Process.star2)


@user.message(Process.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Process.number)
    await message.answer('Pastdagi tugma orqali telefon raqamingizni yuboring 👇',
                         reply_markup=send_number())


@user.message(Process.number, F.contact)
async def get_star(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz endi fikr qoldirishingiz mumkin!",
                         reply_markup=types.ReplyKeyboardRemove())
    user = await state.get_data()
    await rq.edit_user(message.from_user.id,
                       user['name'],
                       user['number'],
                       message.from_user.username)
    await message.answer('Xizmatimizni baholang😉',
                         reply_markup=stars())
    await state.set_state(Process.star)


@user.callback_query(Process.star)
async def get_number(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.update_data(star=callback.data)
    print(callback.data)
    await bot.send_message(chat_id=callback.message.chat.id, text='Iltimos talab yoki taklifingizni yuboring 😉',
                           reply_markup=ReplyKeyboardRemove())
    await state.set_state(Process.question)


@user.message(Process.question)
async def get_question(message: Message, state: FSMContext):
    await rq.add_requirement(message.text, message.from_user.id)
    await message.answer('Fikr bildirganingiz uchun rahmat!!! Xizmatlarimizni albatta yanada sifatli qilamiz!',
                         reply_markup=new_requirement())
    await state.clear()


@user.message(F.text == "🆕 Yangi murojaat yuborish")
async def new_question(message: Message, state: FSMContext):
    await message.answer('Xizmatimizni baholang 😉',
                         reply_markup=stars())
    await state.set_state(Process.star2)


@user.callback_query(Process.star2)
async def get_number(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.update_data(star=callback.data)
    print(type(callback.data))
    await bot.send_message(chat_id=callback.message.chat.id, text='Iltimos talab yoki taklifingizni yuboring 😉',
                           reply_markup=ReplyKeyboardRemove())
    await state.set_state(Process.question2)


@user.message(Process.question2)
async def get_question(message: Message, state: FSMContext):
    await rq.add_requirement(message.text, message.from_user.id)
    await message.answer('Fikr bildirganingiz uchun rahmat!!! Xizmatlarimizni albatta yanada sifatli qilamiz!',
                         reply_markup=new_requirement())
    await state.clear()

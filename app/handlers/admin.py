from aiogram import Router, F, Bot
from aiogram.filters import Filter
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery

from app.database.requests import get_requirement, get_user, delete_requirement
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.inline_kb import all_requirements

admin = Router()


class AnswerState(StatesGroup):
    answer = State()


class Admin(Filter):
    def __init__(self):
        self.admins = [1976114820]

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


@admin.message(Admin(), Command('murojaatlar'))
async def requirements(message: Message):
    await message.answer('Barcha murojaatlar', reply_markup=await all_requirements())


@admin.callback_query(F.data.startswith('requirement_'))
async def answer_requirement(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AnswerState.answer)
    await callback.answer('Murojaatlardan birini tanlang')
    requirement = await get_requirement(callback.data.split('_')[1])
    user = await get_user(requirement.user)
    await state.update_data(tg_id=user.tg_id)
    await state.update_data(requirement_id=requirement.id)
    await callback.message.answer(
        f'ℹ️ Murojaat: {requirement.text}\n\n👤 {user.name}\n📞 {user.number}\n@{user.username}\n\n📝 Javobingizni qoldiring!')


@admin.message(Admin(), AnswerState.answer)
async def send_answer(message: Message, state: FSMContext, bot: Bot):
    info = await state.get_data()
    await bot.send_message(chat_id=info['tg_id'], text=message.text)
    await delete_requirement(info['requirement_id'])
    await message.answer('Xabar yuborildi!')
    await state.clear()

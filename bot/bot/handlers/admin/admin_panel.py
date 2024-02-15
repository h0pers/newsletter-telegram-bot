from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

from bot.config import MessageText
from bot.keyboards.inline.admin_panel.main import admin_panel_markup

admin_panel_router = Router()


@admin_panel_router.message(Command(commands=['start', 'admin']))
async def admin_panel_handler(message: Message):
    await message.answer(text=MessageText.ADMIN_PANEL.format(username=message.from_user.username or message.from_user.first_name),
                         reply_markup=admin_panel_markup.get_markup())

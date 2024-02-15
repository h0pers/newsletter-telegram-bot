import logging

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from sqlalchemy import text

from bot.fsm.newsletter import Newsletter
from bot.database.main import tasks_db_session_local
from bot.config import MessageText
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.main import new_newsletter_markup

set_newsletter_message_router = Router()


@set_newsletter_message_router.message(StateFilter(Newsletter.set_newsletter_message))
async def set_message(message: Message, state: FSMContext):
    try:
        data = {
            'message_id': message.message_id,
            'message_thread_id': message.message_thread_id,
            'from_chat_id': message.chat.id,
        }
        await state.update_data(data)
        await state.set_state(Newsletter.control_newsletter)
        await message.answer(text=MessageText.MESSAGE_ADDED)
        await message.answer(
            text=MessageText.ADMIN_PANEL.format(username=message.from_user.username or message.from_user.first_name),
            reply_markup=new_newsletter_markup.get_markup())

    except AttributeError:
        await message.answer(text=MessageText.ERROR_MESSAGE)



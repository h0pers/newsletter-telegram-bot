from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import text

from bot.fsm.newsletter import Newsletter
from bot.config import MessageText
from bot.keyboards.inline.main import Inline
from bot.database.main import tasks_db_session_local
from bot.callback.newsletter import NewsletterAction
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.main import new_newsletter_markup

set_newsletter_chat_callback_router = Router()


@set_newsletter_chat_callback_router.callback_query(NewsletterAction.filter(F.set_newsletter_chat == 1))
async def set_chat_id(query: CallbackQuery, state: FSMContext):
    channels_message = []
    await state.set_state(Newsletter.set_newsletter_chat)
    async with tasks_db_session_local.begin() as session:
        statement = 'SELECT * FROM channels;'
        channels = await session.execute(statement=text(statement))

    for channel in channels:
        channels_message.append(f"<b>Название чата:</b> @{channel.chat_username} <b>ID чата:</b> {channel.id}")

    if len(channels_message) < 1:
        await query.message.answer(text=MessageText.NO_AVAILABLE_CHANNELS,
                                   reply_markup=Inline([[Inline.cancel_button]]).get_markup())
        await query.answer(text=MessageText.NO_AVAILABLE_CHANNELS)
        return

    await query.message.answer(text=MessageText.PICK_NEWSLETTER_CHAT)
    await query.message.answer(text='\n'.join(channels_message),
                               reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await query.answer()


@set_newsletter_chat_callback_router.callback_query(StateFilter(Newsletter.set_newsletter_chat), F.data == 'cancel')
async def cancel_chat_id(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
        reply_markup=new_newsletter_markup.get_markup())

    try:
        data.pop('reply_chats_id')

    except KeyError:
        pass

    await state.set_data(data)
    await state.set_state(Newsletter.new_newsletter)
    await query.answer(text=MessageText.CANCELED)


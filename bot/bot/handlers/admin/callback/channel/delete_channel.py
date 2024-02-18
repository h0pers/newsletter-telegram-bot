from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.sql import text

from bot.config import MessageText
from bot.callback.channels import ChannelsAction
from bot.fsm.channel import Channel
from bot.keyboards.inline.admin_panel.control_channels.main import control_channels_markup
from bot.keyboards.inline.main import Inline
from bot.database.main import tasks_db_session_local
from bot.keyboards.inline.main import InlineButtonText

delete_channel_callback_router = Router()


@delete_channel_callback_router.callback_query(ChannelsAction.filter(F.delete_channel == 1))
async def delete_channel(query: CallbackQuery, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = '''SELECT * FROM channels;'''
        channels = await session.execute(statement=text(statement))

    await query.message.answer(text=MessageText.WOULD_DELETE_CHANNEL)
    for channel in channels:
        delete_button = InlineKeyboardButton(text=InlineButtonText.DELETE_BUTTON,
                                             callback_data=ChannelsAction(primary_chat_id=channel.id).pack())
        await query.message.answer(text=MessageText.CHANNEL_DETAILS.format(username=channel.chat_username,
                                                                           creation_date=channel.creation_date.strftime(
                                                                               '%D')),
                                   reply_markup=Inline([[delete_button]]).get_markup())

    await query.message.answer(text='Закончить удаление групп?',
                               reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await state.set_state(Channel.delete_channel)
    await query.answer()


@delete_channel_callback_router.callback_query(StateFilter(Channel.delete_channel), ChannelsAction.filter(F.primary_chat_id != 0))
async def delete_picked_channel(query: CallbackQuery, callback_data: ChannelsAction):
    await query.message.edit_text(text=f"{query.message.text}\n<b>Удалено.</b>")
    async with tasks_db_session_local.begin() as session:
        statement = f'DELETE FROM bot_message_tasks WHERE reply_chat_id={callback_data.primary_chat_id};'
        await session.execute(text(statement))
        statement = f'DELETE FROM bot_periodic_message_tasks WHERE reply_chat_id={callback_data.primary_chat_id};'
        await session.execute(text(statement))
        statement = f'DELETE FROM channels WHERE id={callback_data.primary_chat_id};'
        await session.execute(text(statement))

    await query.answer('Удалено')


@delete_channel_callback_router.callback_query(StateFilter(Channel.delete_channel), F.data == 'cancel')
async def cancel_deleting(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
        reply_markup=control_channels_markup.get_markup())
    await state.set_state(Channel.control_channel)
    await query.answer()

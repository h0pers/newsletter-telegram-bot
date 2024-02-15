from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import text

from bot.config import MessageText
from bot.callback.channels import ChannelsAction
from bot.fsm.channel import Channel
from bot.database.main import tasks_db_session_local
from bot.keyboards.inline.admin_panel.control_channels.main import control_channels_markup

available_channels_callback_router = Router()


@available_channels_callback_router.callback_query(ChannelsAction.filter(F.view_available_channels == 1))
async def available_channel(query: CallbackQuery, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = 'SELECT * FROM channels;'
        channels = await session.execute(statement=text(statement))

    await query.message.answer(text=MessageText.AVAILABLE_CHANNELS)
    for channel in channels:
        await query.message.answer(text=MessageText.CHANNEL_DETAILS.format(username=channel.chat_username,
                                                                           creation_date=channel.creation_date.strftime(
                                                                               '%D')))
    await query.message.answer(text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
                               reply_markup=control_channels_markup.get_markup())
    await state.set_state(Channel.control_channel)
    await query.answer()

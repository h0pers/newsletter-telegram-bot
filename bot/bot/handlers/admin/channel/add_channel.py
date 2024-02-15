from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from bot.fsm.channel import Channel
from bot.config import MessageText
from bot.keyboards.inline.admin_panel.control_channels.main import control_channels_markup
from bot.database.main import tasks_db_session_local
add_channel_router = Router()


@add_channel_router.message(StateFilter(Channel.new_channel))
async def add_channel(message: Message, state: FSMContext):
    try:
        async with tasks_db_session_local.begin() as session:
            statement = f"""
            INSERT INTO channels (chat_id, chat_username)
            VALUES ({message.forward_from_chat.id}, '{message.forward_from_chat.username}');"""
            await session.execute(statement=text(statement))

        await message.answer(text=MessageText.ADD_CHANNEL_SUCCESSFUL)
        await message.answer(text=MessageText.ADMIN_PANEL.format(username=message.from_user.username or message.from_user.first_name),
                             reply_markup=control_channels_markup.get_markup())
        await state.set_state(Channel.control_channel)

    except AttributeError:
        await message.answer(text=MessageText.ADD_CHANNEL_ERROR)
    except IntegrityError:
        await message.answer(text=MessageText.CHANNEL_EXIST)

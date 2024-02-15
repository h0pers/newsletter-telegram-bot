from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from bot.config import MessageText
from bot.callback.channels import ChannelsAction
from bot.fsm.channel import Channel
from bot.keyboards.inline.admin_panel.control_channels.main import control_channels_markup
from bot.keyboards.inline.main import Inline

add_channel_callback_router = Router()


@add_channel_callback_router.callback_query(ChannelsAction.filter(F.new_channel == 1))
async def add_channel(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.ADD_CHANNEL,
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[[Inline.cancel_button]]))
    await state.set_state(Channel.new_channel)
    await state.update_data({'add_channel_chat_id': query.message.chat.id,
                             'add_channel_message_id': query.message.message_id})
    await query.answer()


@add_channel_callback_router.callback_query(StateFilter(Channel.new_channel), F.data == 'cancel')
async def cancel_adding(query: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await query.message.delete()
    await bot.delete_message(chat_id=data['add_channel_chat_id'],
                             message_id=data['add_channel_message_id'])
    await query.message.answer(text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
                               reply_markup=control_channels_markup.get_markup())
    await state.clear()
    await state.set_state(Channel.control_channel)

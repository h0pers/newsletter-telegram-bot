from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline.admin_panel.main import admin_panel_markup
from bot.callback.channels import ChannelsAction
from bot.fsm.channel import Channel
from bot.keyboards.inline.admin_panel.control_channels.main import control_channels_markup

control_channels_callback_router = Router()


@control_channels_callback_router.callback_query(ChannelsAction.filter(F.control_channel == 1))
async def control_channel(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=control_channels_markup.get_markup())
    await state.set_state(Channel.control_channel)


@control_channels_callback_router.callback_query(StateFilter(Channel.control_channel), F.data == 'back')
async def back_admin_panel(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=admin_panel_markup.get_markup())
    await state.clear()

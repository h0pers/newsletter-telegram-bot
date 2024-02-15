from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from bot.config import MessageText
from bot.keyboards.inline.admin_panel.main import admin_panel_markup

main_page_callback_router = Router()


@main_page_callback_router.callback_query(F.data == 'main_page')
async def main_page(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
                                  reply_markup=admin_panel_markup.get_markup())
    await state.clear()

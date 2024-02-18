from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.sql import text

from bot.config import MessageText
from bot.database.main import tasks_db_session_local
from bot.fsm.categories import Categories
from bot.keyboards.inline.admin_panel.control_newsletter.control_categories.main import control_categories_markup

new_category_router = Router()


@new_category_router.message(StateFilter(Categories.new_category))
async def new_category(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer(text=MessageText.ERROR_MESSAGE)
        raise Exception('is not a string')

    async with tasks_db_session_local.begin() as session:
        statement = f"INSERT INTO bot_message_categories (title) VALUES ('{message.text}');"
        await session.execute(statement=text(statement))

    await message.answer(text=MessageText.NEW_CATEGORY_SUCCESSFUL.format(category=message.text))
    await state.set_state(Categories.control_categories)
    await message.answer(
        text=MessageText.ADMIN_PANEL.format(username=message.from_user.username or message.from_user.first_name),
        reply_markup=control_categories_markup.get_markup())

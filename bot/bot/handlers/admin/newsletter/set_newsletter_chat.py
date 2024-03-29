from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from sqlalchemy import text

from bot.fsm.newsletter import Newsletter
from bot.database.main import tasks_db_session_local
from bot.config import MessageText

from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.main import new_newsletter_markup

set_newsletter_chat_router = Router()


@set_newsletter_chat_router.message(StateFilter(Newsletter.set_newsletter_chat))
async def set_chat_id(message: Message, state: FSMContext):
    message_text = [number.strip() for number in message.text.split(',')]
    for word in message_text:
        if not word.isnumeric():
            await message.answer(text='Данное сообщение не является цифрой. Попробуйте ещё раз')
            return

        async with tasks_db_session_local.begin() as session:
            statement = f'SELECT chat_id FROM channels WHERE id={word} LIMIT 1;'
            chat_id = await session.execute(statement=text(statement))
            chat_id = chat_id.scalar()

        if chat_id is None:
            await message.answer(text=MessageText.CHANNEL_NOT_FOUND)
            return
    await state.update_data({'reply_chats_id': list(set(message_text))})
    await message.answer(text=MessageText.DONE)
    await message.answer(text=MessageText.ADMIN_PANEL.format(username=message.from_user.username or message.from_user.first_name),
                         reply_markup=new_newsletter_markup.get_markup())
    await state.set_state(Newsletter.new_newsletter)


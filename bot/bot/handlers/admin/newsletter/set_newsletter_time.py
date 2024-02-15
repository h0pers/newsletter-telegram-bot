from datetime import datetime
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter

from bot.fsm.newsletter import Newsletter
from bot.config import MessageText
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.main import new_newsletter_markup

set_newsletter_time_router = Router()


@set_newsletter_time_router.message(StateFilter(Newsletter.set_newsletter_time))
async def set_message(message: Message, state: FSMContext):
    try:
        datetime.strptime(message.text, '%H:%M')
        await state.update_data({'publish_time': message.text})
        await message.answer(text=MessageText.SET_MESSAGE_SUCCESSFULUl)
        await message.answer(
            text=MessageText.ADMIN_PANEL.format(username=message.from_user.username or message.from_user.first_name),
            reply_markup=new_newsletter_markup.get_markup())
        await state.set_state(Newsletter.control_newsletter)

    except TypeError:
        await message.answer(text=MessageText.ERROR_MESSAGE)

    except ValueError:
        await message.answer(text=MessageText.SET_MESSAGE_TIME_ERROR)

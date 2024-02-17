import logging
from datetime import timedelta
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter

from bot.fsm.newsletter import Newsletter
from bot.config import MessageText
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.control_time import control_time_markup

set_newsletter_period_time_message_router = Router()


@set_newsletter_period_time_message_router.message(StateFilter(Newsletter.set_newsletter_periodic_time))
async def set_newsletter_period_time(message: Message, state: FSMContext):
    try:
        time_data = [float(time) for time in message.text.split(':', maxsplit=2)]
        logging.info(timedelta(days=time_data[0], hours=time_data[1], minutes=time_data[2]))
        await state.update_data({'period_time_data': time_data})
        data = await state.get_data()
        try:
            data.pop('publish_time')
        except:
            pass
        await state.set_data(data)
        await state.set_state(Newsletter.control_newsletter_time)
        await message.answer(text=MessageText.SET_MESSAGE_SUCCESSFULUl)
        await message.answer(text=MessageText.ADMIN_PANEL.format(username=message.from_user.username or message.from_user.first_name),
                             reply_markup=control_time_markup.get_markup())

    except Exception as exception:
        logging.exception(exception)
        await message.answer(text=MessageText.ERROR_MESSAGE)

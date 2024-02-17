from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.newsletter import NewsletterAction
from bot.fsm.newsletter import Newsletter
from bot.config import MessageText
from bot.keyboards.inline.main import Inline
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.control_time import control_time_markup

set_periodic_time_callback_router = Router()


@set_periodic_time_callback_router.callback_query(NewsletterAction.filter(F.set_newsletter_periodic_time == 1))
async def set_periodic_time(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.PERIODIC_TIME_TASK,
                               reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await query.answer()
    await state.set_state(Newsletter.set_newsletter_periodic_time)


@set_periodic_time_callback_router.callback_query(StateFilter(Newsletter.set_newsletter_periodic_time), F.data == 'cancel')
async def cancel_periodic_time(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        data.pop('period_time_data')

    except KeyError:
        pass

    await state.set_data(data)
    await query.message.answer(text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
                               reply_markup=control_time_markup.get_markup())
    await query.answer(text=MessageText.CANCELED)
    await state.set_state(Newsletter.control_newsletter_time)



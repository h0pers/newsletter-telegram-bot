from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.newsletter import NewsletterAction
from bot.config import MessageText
from bot.fsm.newsletter import Newsletter
from bot.keyboards.inline.main import Inline
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.main import new_newsletter_markup

set_newsletter_time_callback_router = Router()


@set_newsletter_time_callback_router.callback_query(NewsletterAction.filter(F.set_newsletter_time == 1))
async def set_time(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.SET_MESSAGE_TIME)
    await query.message.answer(text=MessageText.WOULD_CANCEL,
                               reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await state.set_state(Newsletter.set_newsletter_time)
    await query.answer(text=MessageText.SET_MESSAGE_TIME)


@set_newsletter_time_callback_router.callback_query(StateFilter(Newsletter.set_newsletter_time), F.data == 'cancel')
async def cancel_set_time(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        data.pop('publish_time')

    except KeyError:
        pass

    await state.set_data(data)
    await state.set_state(Newsletter.control_newsletter)
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
        reply_markup=new_newsletter_markup.get_markup())
    await query.answer(text=MessageText.CANCELED)


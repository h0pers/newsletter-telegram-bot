from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callback.newsletter import NewsletterAction
from bot.config import MessageText
from bot.fsm.newsletter import Newsletter
from bot.keyboards.inline.admin_panel.control_newsletter.new_newsletter.main import new_newsletter_markup
from bot.keyboards.inline.main import Inline

set_newsletter_message_callback_router = Router()


@set_newsletter_message_callback_router.callback_query(NewsletterAction.filter(F.set_newsletter_message == 1))
async def set_message(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text=MessageText.ADD_MESSAGE)
    await query.message.answer(text=MessageText.WOULD_CANCEL,
                               reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await state.set_state(Newsletter.set_newsletter_message)
    await query.answer(text='Перешлите сообщение')


@set_newsletter_message_callback_router.callback_query(StateFilter(Newsletter.set_newsletter_message), F.data == 'cancel')
async def cancel_set_message(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        data.pop('from_chat_id')
        data.pop('message_thread_id')
        data.pop('message_id')

    except KeyError:
        pass

    await state.set_data(data)
    await state.set_state(Newsletter.control_newsletter)
    await query.message.answer(
        text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
        reply_markup=new_newsletter_markup.get_markup())
    await query.answer(text=MessageText.CANCELED)

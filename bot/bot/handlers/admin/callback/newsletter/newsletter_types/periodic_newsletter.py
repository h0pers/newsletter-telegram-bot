from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from sqlalchemy import text

from bot.callback.newsletter import NewsletterTypes
from bot.fsm.newsletter import Newsletter
from bot.config import MessageText
from bot.database.main import tasks_db_session_local
from bot.keyboards.inline.main import Inline
from bot.keyboards.inline.admin_panel.control_newsletter.available_newsletters.main import choose_newsletter_type
from bot.callback.newsletter import NewsletterAction
from bot.keyboards.inline.main import InlineButtonText

periodic_newsletter_callback_router = Router()


@periodic_newsletter_callback_router.callback_query(NewsletterTypes.filter(F.periodic_message == 1))
async def periodic_newsletter(query: CallbackQuery, bot: Bot, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = '''
        SELECT (id, reply_chat_id, from_chat_id, message_id, message_thread_id, time_interval) 
        FROM bot_periodic_message_tasks;
        '''

        tasks = await session.execute(statement=text(statement))
        tasks = tasks.scalars().all()

        for task in tasks:
            statement = f'SELECT chat_username FROM channels WHERE id={task[1]};'
            channel = await session.execute(statement=text(statement))
            channel_username = channel.scalar()
            delete_button = InlineKeyboardButton(text=InlineButtonText.DELETE_BUTTON,
                                                 callback_data=NewsletterAction(newsletter_id=task[0],
                                                                                delete_newsletter=1).pack())
            await query.message.answer(text=MessageText.PERIODIC_NEWSLETTER_DETAILS.format(username=channel_username,
                                                                                           publish_time=task[5]),
                                       reply_markup=Inline([[delete_button]]).get_markup())
            await bot.forward_message(chat_id=query.message.chat.id, from_chat_id=task[2], message_id=task[3],
                                      message_thread_id=task[4])

        await query.message.answer(text=MessageText.WOULD_CANCEL,
                                   reply_markup=Inline([[Inline.cancel_button]]).get_markup())
    await state.set_state(Newsletter.edit_periodic_newsletter)
    await query.answer()


@periodic_newsletter_callback_router.callback_query(StateFilter(Newsletter.edit_periodic_newsletter),
                                                    NewsletterAction.filter(F.delete_newsletter == 1 and F.newsletter_id != 0))
async def delete_periodic_newsletter(query: CallbackQuery, callback_data: NewsletterAction, state: FSMContext):
    async with tasks_db_session_local.begin() as session:
        statement = f'DELETE FROM bot_periodic_message_tasks WHERE id={callback_data.newsletter_id}'
        await session.execute(statement=text(statement))

    await query.message.edit_text(text=query.message.text + '\n<b>Удалено.</b>')
    await query.answer(text=MessageText.DONE)


@periodic_newsletter_callback_router.callback_query(StateFilter(Newsletter.edit_periodic_newsletter), F.data == 'cancel')
async def cancel_periodic_newsletter(query: CallbackQuery, state: FSMContext):
    await state.set_state(Newsletter.edit_newsletter)
    await query.message.answer(text=MessageText.ADMIN_PANEL.format(username=query.from_user.username or query.from_user.first_name),
                               reply_markup=choose_newsletter_type.get_markup())
    await query.answer()

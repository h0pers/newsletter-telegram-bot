from sqlalchemy import text

from app.database.main import SessionLocal


def refresh_periodic_messages_datetime():
    with SessionLocal.begin() as session:
        statement = 'UPDATE bot_periodic_message_tasks SET last_publish_time=NOW()'
        session.execute(statement=text(statement))


def run_schedule():
    refresh_periodic_messages_datetime()

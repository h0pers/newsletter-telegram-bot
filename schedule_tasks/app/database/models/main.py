from app.database.main import engine, Base
from .tasks import *
from .channels import *


def register_models() -> None:
    with engine.begin() as conn:
        Base.metadata.create_all(conn)

import logging
import sys

from app.database.models.main import register_models
from app.main import run_schedule


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    register_models()
    run_schedule()

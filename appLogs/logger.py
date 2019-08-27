import logging
from logging.config import fileConfig
from os import path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)


def getLogger(name=None):
    if name is None:
        log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
        fileConfig(log_file_path)
        logger = logging.getLogger()

        return logger
    else:
        logger = logging.getLogger(name)

        # Replace the previous handlers with the new FileHandler
        for old_handler in logger.handlers:
            logger.removeHandler(old_handler)

        return logger
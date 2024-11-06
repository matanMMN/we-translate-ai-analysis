import sys
import os
import logging
from loguru import logger as loguru_logger
from logging.config import fileConfig
from globals import ROOT_DIR
from meditranslate.app.configurations import config

logging.getLogger('pymongo').setLevel(logging.INFO)
logging.getLogger('faker').setLevel(logging.INFO)

def init_logger():
    DISABLE_EXISTING_LOGGERS = False
    LOG_DIR = None
    IS_STDOUT = True
    LOG_FILE = None
    LAST_RUN_LOG_FILE = None


    current_dir = os.path.dirname(os.path.abspath(__file__))
    logging_config_path = os.path.join(ROOT_DIR, 'logging.ini')
    fileConfig(logging_config_path, disable_existing_loggers=DISABLE_EXISTING_LOGGERS)

    if LOG_DIR is not None:
        logging_files_path = os.path.join(current_dir, LOG_DIR)
        if not os.path.exists(logging_files_path):
            os.makedirs(logging_files_path)
        LOG_FILE = os.path.join(logging_files_path, 'application.log')
        LAST_RUN_LOG_FILE = os.path.join(logging_files_path, 'last_run_application.log')


    # Remove default Loguru logger and set up a new one with custom configurations
    loguru_logger.remove()

    # Log rotation for file logging: daily log rotation with 7-day retention and compression
    if LOG_FILE is not None:
        loguru_logger.add(
            LOG_FILE,
            rotation="1 day",   # New file is created each day
            retention="7 days",  # Keep logs for 7 days
            compression="zip",   # Compress old logs as zip
            level=config.RETENTION_LOG_LEVEL,       # Set the default log level to DEBUG
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            enqueue=True         # Async logging for better performance
        )
    if LAST_RUN_LOG_FILE is not None:
        loguru_logger.add(
            LAST_RUN_LOG_FILE,
            level=config.LAST_RUN_LOG_LEVEL,       # Set the default log level to DEBUG
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            enqueue=True,         # Async logging for better performance
            mode='w'
        )

    # Console handler with colored logs for easier debugging in development
    # if IS_STDOUT is True:
    loguru_logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
        level=config.STD_LOG_LEVEL
    )

    # # Exception logging for unhandled exceptions
    # def exception_handler(exc_type, exc_value, exc_traceback):
    #     # Log the exception with a full traceback
    #     logger.exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    # # Assign the exception handler for unhandled exceptions
    # sys.excepthook = exception_handler

    # Integrate Loguru with the standard `logging` module for compatibility
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            loguru_level = getattr(logger, record.levelname.lower(), "info")
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            loguru_level(record.getMessage(), depth=depth)

    logging.basicConfig(handlers=[InterceptHandler()], level=config.BASE_LOG_LEVEL)


    return loguru_logger

logger = init_logger()

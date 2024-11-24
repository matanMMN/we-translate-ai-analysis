import sys
import os
import json
from dotenv import load_dotenv
from meditranslate.app.loggers import logger
from meditranslate.app.application import create_app
from globals import PYTHON_VERSION,ROOT_DIR
from meditranslate.app.configurations import EnvironmentType
from fastapi import FastAPI
from meditranslate.app.configurations import config
import logging

load_dotenv(f"./environments/.env.{config.ENVIRONMENT}")

os.makedirs(config.UPLOAD_DIR, exist_ok=True)

if "pytest" in sys.modules:
    logger.warning(f"pytest is imported - overiding config.ENVIRONMENT from {config.ENVIRONMENT} ->  {EnvironmentType.TESTING.value}")
    config.ENVIRONMENT = EnvironmentType.TESTING.value

if  config.ENVIRONMENT == EnvironmentType.DEVELOPMENT.value and config.DEBUG_ON_INIT == True:
    import debugpy
    logger.info("Waiting for debugger to attach...")
    debugpy.wait_for_client()


def log_env():
    if config.PRINT_ENVIRONMENT:
        envrioment_log = {
            "python version:":PYTHON_VERSION,
            "current dir":ROOT_DIR,
            "env": config.ENVIRONMENT,
            # "env_data":{key: value for key, value in os.environ.items()}
        }
        logger.info(f"""\n\nENVIRONMENT LOG\n{json.dumps(envrioment_log,indent=2)}""")

def log_app(_app:FastAPI):
    if config.PRINT_APP:
        app_log = {
            "title":config.APP_NAME,
            "host":config.APP_HOST,
            "port":config.APP_PORT,
            "docs":_app.docs_url,
            # "license": app.license_info
        }
        logger.info(f"""\n\nAPPLICATION LOG\n{json.dumps(app_log,indent=2)}""")

log_env()
app = create_app()
log_app(app)

if __name__ == "__main__":
    pass

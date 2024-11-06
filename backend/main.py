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
    envrioment_log = {
        "python version:":PYTHON_VERSION,
        "current dir":ROOT_DIR,
        "env": config.ENVIRONMENT,
        "print_env": config.PRINT_ENVIRONMENT,
    }

    if config.PRINT_ENVIRONMENT:
        env_data = {key: value for key, value in os.environ.items()}
        # env_data = json.dumps(dict(os.environ),indent=2)
        envrioment_log['env_data'] = env_data

    logger.info(f"""\n\nENVIRONMENT LOG\n{json.dumps(envrioment_log,indent=2)}""")

log_env()

def log_app(_app:FastAPI):

    app_log = {
        "title":config.APP_NAME,
        "host":config.APP_HOST,
        "port":config.APP_PORT,
        "docs":_app.docs_url,
        "license": app.license_info

    }
    logger.info(f"""\n\nAPPLICATION LOG\n{json.dumps(app_log,indent=2)}""")

app = create_app()
log_app(app)

if __name__ == "__main__":
    pass

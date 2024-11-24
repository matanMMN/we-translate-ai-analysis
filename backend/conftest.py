""" Module """
import logging
import pytest
import pytest_asyncio
from _pytest.logging import LogCaptureFixture
from meditranslate.app.loggers import logger
from dotenv import load_dotenv

load_dotenv("./environments/.env.testing")

pytestmark = pytest.mark.anyio

logging.getLogger('faker').setLevel(logging.ERROR)


class PropagateHandler(logging.Handler):
    def emit(self,record):
        logger = logging.getLogger(record.name)
        if logger.isEnabledFor(record.levelno):
            logger.handle(record)


@pytest.fixture(autouse=True,scope="session")
def cleanup_loguru():
    logger.remove()


@pytest.fixture(autouse=True,scope="session")
def propegate_loguru(cleanup_loguru):
    handler_id = logger.add(PropagateHandler(),format="{message}")
    yield
    logger.remove(handler_id)

@pytest_asyncio.fixture(autouse=True) #ignore
async def caplog(caplog: LogCaptureFixture):
    """
        Make pytest work with loguru. See:https://loguru.readthedocs.io/en/stable/resources/migration.html#making-things-work-with-pytest-and-caplog
    """
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)


@pytest.fixture(params=[
    pytest.param(('asyncio', {'use_uvloop': True}), id='asyncio+uvloop'),
    # pytest.param(('asyncio', {'use_uvloop': False}), id='asyncio'),
    # pytest.param(('trio', {'restrict_keyboard_interrupt_to_checkpoints': True}), id='trio')
])
def anyio_backend(request):
    return request.param

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine
from meditranslate.app.loggers import logger

def use_inspector(conn):
    inspector = inspect(conn)
    logger.info(inspector.get_view_names())
    return inspector.get_table_names()

async def run(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(use_inspector)


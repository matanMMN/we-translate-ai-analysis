from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from typing import Union
import json

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.expression import Delete, Insert, Update

from meditranslate.app.configurations import config
from meditranslate.app.loggers import logger


# Create two separate database engines: one for write operations and another for read operations.
# Both engines are set up with the same database URL, but they could be configured to point to
# different instances (e.g., a primary for writes and a replica for reads).
engines = {
    "writer": create_async_engine(
        str(config.DATABASE_URL),                # Database connection URL.
        pool_recycle=3600,                  # Time in seconds to recycle connections.
        echo=False,                          # If True, SQL statements will be logged.
        future=True,                        # Enables future compatibility features.
        # isolation_level="AUTOCOMMIT",      # Sets the isolation level for transactions.
    ),
    "reader": create_async_engine(
        str(config.DATABASE_URL),                # Database connection URL.
        pool_recycle=3600,                  # Time in seconds to recycle connections.
        echo=False,                          # If True, SQL statements will be logged.
        future=True,                        # Enables future compatibility features.
        # isolation_level="AUTOCOMMIT",      # Sets the isolation level for transactions.
    ),
}

class RoutingSession(Session):
    """
    Custom SQLAlchemy Session class that routes database operations to either
    the writer or reader engine based on the type of operation.
    """

    def get_bind(self, mapper=None, clause=None, **kwargs):
        """
        Overrides the `get_bind` method to determine which engine to use.
        If the operation is a write (Insert, Update, Delete) or if the session
        is in a flushing state, it uses the writer engine. Otherwise, it uses the reader engine.

        :param mapper: Optional, specifies the mapped class or other attributes.
        :param clause: The SQL clause to be executed (e.g., Insert, Update, Delete).
        :return: The engine to use for this session (either writer or reader).
        """
        # logger.info(f"BINDING")
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            # logger.info(f"BINDING WRITER")
            return engines["writer"].sync_engine
        # logger.info(f"BINDING READER")
        return engines["reader"].sync_engine

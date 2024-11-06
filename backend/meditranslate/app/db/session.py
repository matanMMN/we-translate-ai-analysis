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



# Context variable for session management; stores the current session context (e.g., session ID).
# `ContextVar` allows each asynchronous task to have an independent session context,
# avoiding conflicts when handling multiple requests concurrently.
session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    """
    Retrieves the current session context (e.g., session ID) for the current task.

    :return: The current session context as a string.
    """
    session_id = session_context.get()
    logger.debug(f"GET_SESSION_CONTEXT {session_id}")
    return session_id


def set_session_context(session_id: str) -> Token:
    """
    Sets a new session context for the current task, using the provided session ID.
    This helps in binding the session uniquely to each asynchronous task or request.

    :param session_id: Unique identifier for the session context.
    :return: A `Token` that can be used to reset the session context.
    """
    logger.debug(f"SET_SESSION_CONTEXT {session_id}")
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    """
    Resets the session context to a previous state using the provided `Token`.
    This function is typically called after the session is no longer needed.

    :param context: A `Token` representing the previous session context to restore.
    """

    session_context.reset(context)
    logger.debug(f"RESET_SESSION_CONTEXT {context}")


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


# Define an asynchronous session factory with various configurations.
async_session_factory = async_sessionmaker(
    class_=AsyncSession,                          # Specifies the class for the session (AsyncSession).
    sync_session_class=RoutingSession,            # Defines the sync session class for routing.
    expire_on_commit=False,                       # If True, instances will be expired after commit.
    #echo=True,                                   # If True, SQL statements will be printed to the log.
    #echo_pool=True,                              # If True, pool checkouts will be logged.
    #enable_from_linting=True,                     # Enables linting for `FROM` clauses.
    #hide_parameters=True,                        # If True, parameters will be hidden in the log.
    # insertmanyvalues_page_size=1000,             # Number of rows to insert at a time for bulk inserts.
    # json_deserializer=json.loads,                 # Function for deserializing JSON.
    # json_serializer=json.dumps,                   # Function for serializing to JSON.
    # max_identifier_length=None,                   # Maximum length for identifiers (None for no limit)..
    # pool_reset_on_return='rollback',              # Reset connections to this state on return to the pool.
    # plugins=[],                                   # List of plugins to use with the session.
    # query_cache_size=100,                         # Size of the query cache.
    # connect_args={},                              # Additional arguments passed to the database connection.
)

# Create a scoped session, which ensures each async task or request gets its own session.
# The scope is determined by `get_session_context()`, which returns the session ID associated
# with the current task. This allows each request to operate independently.
AsyncScopedSession: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)



async def get_session():
    """
    Dependency injection for database sessions in asynchronous frameworks.
    Yields the current session and closes it afterward. This ensures each request
    gets a fresh session that is cleaned up after use.

    :yield: The database session.
    """
    try:
        yield AsyncScopedSession
    finally:
        await AsyncScopedSession.close()



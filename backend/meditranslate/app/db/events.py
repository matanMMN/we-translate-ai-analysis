import time
import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from meditranslate.app.loggers import logger


def register_event_listeners():
# connect event on instance of Engine

    @event.listens_for(Engine, "before_execute")
    def my_before_execute(
        conn,
        clauseelement,
        multiparams,
        params,
        execution_options,
    ):
        logger.info("before execute!")

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault("query_start_time", []).append(time.time())
        logger.debug("Start Query: %s", statement)

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info["query_start_time"].pop(-1)
        logger.debug("Query Complete!")
        logger.debug("Total Time: %f seconds", total)

    @event.listens_for(Session, "before_commit")
    def before_commit(session):
        logger.debug(f"Before commit: {session.new}")  # Log new objects being committed
        logger.debug(f"Modified objects: {session.dirty}")  # Log modified objects

    @event.listens_for(Session, "after_commit")
    def after_commit(session):
        logger.debug("After commit")

    @event.listens_for(Session, "before_flush")
    def before_flush(session, flush_context, instances):
        logger.debug("Before flush: %s", instances)

    @event.listens_for(Session, "after_flush")
    def after_flush(session, flush_context):
        logger.debug("After flush: %s", flush_context)

    @event.listens_for(Session, "after_bulk_insert")
    def after_bulk_insert(session, result, target, values):
        logger.debug("After bulk insert: %s", values)

    @event.listens_for(Session, "after_bulk_update")
    def after_bulk_update(session, result, target, values):
        logger.debug("After bulk update: %s", values)

    @event.listens_for(Session, "after_bulk_delete")
    def after_bulk_delete(session, result, target, values):
        logger.debug("After bulk delete: %s", values)


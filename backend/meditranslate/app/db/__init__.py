from meditranslate.app.db.base import Base
from meditranslate.app.db.decorator import standalone_session
from meditranslate.app.db.transaction import Propagation, Transactional
from meditranslate.app.db.base_repository import BaseRepository
from meditranslate.app.db.events import register_event_listeners
from meditranslate.app.db.session import (
    get_session,
    reset_session_context,
    AsyncScopedSession,
    set_session_context,
    engines
)
from meditranslate.app.db.models import *

async def init_db():
    engine = engines['writer']
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

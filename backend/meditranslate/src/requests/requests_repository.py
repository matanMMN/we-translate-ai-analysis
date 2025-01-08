from sqlalchemy.ext.asyncio import AsyncSession
from meditranslate.app.db.base_repository import BaseRepository
from meditranslate.src.requests.requests import Request

class RequestRepository(BaseRepository[Request]):
    def __init__(self, session: AsyncSession):
        super().__init__(Request, session)
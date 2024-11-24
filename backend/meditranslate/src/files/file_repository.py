from meditranslate.app.db.models import File
from meditranslate.app.db.base_repository import BaseRepository

class FileRepository(BaseRepository[File]):
    def __init__(self, db_session):
        super().__init__(File, db_session)

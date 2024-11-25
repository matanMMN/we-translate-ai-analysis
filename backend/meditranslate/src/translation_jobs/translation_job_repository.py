from meditranslate.app.db.models import TranslationJob
from meditranslate.app.db.base_repository import BaseRepository

class TranslationJobRepository(BaseRepository[TranslationJob]):
    def __init__(self, db_session):
        super().__init__(TranslationJob, db_session)

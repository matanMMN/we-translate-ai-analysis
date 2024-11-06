from meditranslate.app.db.models import Translation
from meditranslate.app.db.base_repository import BaseRepository

class TranslationRepository(BaseRepository[Translation]):
    def __init__(self, db_session):
        super().__init__(Translation, db_session)

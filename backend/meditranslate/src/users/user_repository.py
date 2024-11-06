from meditranslate.app.db.models import User
from meditranslate.app.db.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db_session):
        super().__init__(User, db_session)

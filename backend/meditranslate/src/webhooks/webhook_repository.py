from meditranslate.app.db.base_repository import BaseRepository
from meditranslate.src.webhooks.webhook import Webhook

class WebhookRepository(BaseRepository[Webhook]):
    def __init__(self, db_session):
        super().__init__(Webhook, db_session)
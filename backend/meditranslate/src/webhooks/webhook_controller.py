# from typing import List
from meditranslate.app.shared.base_controller import BaseController
from meditranslate.src.webhooks.webhook import Webhook
from meditranslate.src.webhooks.webhook_service import WebhookService
from meditranslate.app.db.transaction import Transactional, Propagation
from typing import Dict, List


class WebhookController(BaseController[Webhook]):
    def __init__(self, webhook_service: WebhookService):
        super().__init__(Webhook, webhook_service)
        self.webhook_service = webhook_service

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def register_webhook(self, webhook_data: dict) -> Webhook:
        return await self.webhook_service.register_webhook(webhook_data)
    
    async def get_webhook(self, webhook_id: str) -> Webhook:
        return await self.webhook_service.get_webhook(webhook_id)
    
    async def get_user_webhooks(self, user_id: str) -> List[Webhook]:
        """Get all webhooks for a user"""
        return await self.webhook_service.get_user_webhooks(user_id)

    async def get_webhook_by_translation_job(self, translation_job_id: str, user_id: str) -> Webhook:
        """Get webhook for a specific translation job"""
        return await self.webhook_service.get_webhook_by_translation_job(
            translation_job_id=translation_job_id,
            user_id=user_id
    )

    async def notify_translation_complete(self, translation_job_id: str, translation_data: Dict) -> None:
        await self.webhook_service.notify_translation_complete(translation_job_id, translation_data)
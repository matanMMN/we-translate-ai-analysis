from logging import Filter
from typing import Dict, List
from meditranslate.app.shared.base_service import BaseService
from meditranslate.src.webhooks.webhook import Webhook
from meditranslate.src.webhooks.webhook_repository import WebhookRepository
from meditranslate.src.translation_jobs.translation_job_repository import TranslationJobRepository
from meditranslate.app.errors import AppError, HTTPStatus
from datetime import datetime
import httpx
from meditranslate.app.loggers import logger


class WebhookService(BaseService[Webhook]):
    def __init__(
            self,
            webhook_repository: WebhookRepository,
            translation_job_repository: TranslationJobRepository
    ):
        super().__init__(model=Webhook, repository=webhook_repository)
        self.webhook_repository = webhook_repository
        self.translation_job_repository = translation_job_repository

    async def register_webhook(self, webhook_data: Dict) -> Webhook:
        # Validate that required fields are present
        required_fields = ["user_id", "translation_job_id"]
        for field in required_fields:
            if field not in webhook_data:
                raise AppError(
                    title="webhook registration",
                    message=f"Missing required field: {field}",
                    http_status=HTTPStatus.BAD_REQUEST
                )

        # Verify that the translation job exists and belongs to the user
        translation_job = await self.translation_job_repository.get_by(
            "id",
            webhook_data["translation_job_id"],
            unique=True
        )

        if not translation_job:
            raise AppError(
                title="webhook registration",
                message="Translation job not found",
                http_status=HTTPStatus.NOT_FOUND
            )

        if translation_job.created_by != webhook_data["user_id"]:
            raise AppError(
                title="webhook registration",
                message="Translation job does not belong to the user",
                http_status=HTTPStatus.FORBIDDEN
            )

        # Check if a webhook already exists for this translation job
        existing_webhook = await self.webhook_repository.get_by(
            "translation_job_id",
            webhook_data["translation_job_id"],
            unique=True
        )

        if existing_webhook:
            raise AppError(
                title="webhook registration",
                message="A webhook already exists for this translation job",
                http_status=HTTPStatus.CONFLICT
            )
        # Add created_at timestamp
        webhook_data["created_at"] = datetime.now()
        # webhook_data["callback_url"] = str(webhook_data["callback_url"])
        webhook_data.update({
            "is_triggered": False,
            "triggered_at": None
        })

        webhook = await self.webhook_repository.create(webhook_data)
        return webhook.as_dict()

    async def get_webhook(self, webhook_id: str) -> Webhook:
        """Get a webhook by its ID"""
        webhook = await self.webhook_repository.get_by(
            "id",
            webhook_id,
            unique=True
        )

        if not webhook:
            raise AppError(
                title="get webhook",
                message="Webhook not found",
                http_status=HTTPStatus.NOT_FOUND
            )

        return webhook.as_dict()

    async def notify_translation_complete(self, translation_job_id: str, translation_data: Dict) -> None:
        """Send webhook notification when translation is complete"""
        webhook = await self.webhook_repository.get_by(
            "translation_job_id",
            translation_job_id,
            unique=True
        )

        if webhook: # and not webhook.is_triggered:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        str("http://app:3000/api/stream"),
                        # str("http://host.docker.internal:3000/api/stream"),
                        json={
                            "event": "translation_complete",
                            "translation_job_id": translation_job_id,
                            "translation_data": translation_data
                        },
                        timeout=10.0
                    )
                    response.raise_for_status()
                await self.webhook_repository.update(
                    webhook,
                    {
                        "file_id": translation_data.get("file_id"),
                        "is_triggered": True,
                        "triggered_at": datetime.now()
                    }
                )

            except Exception as e:
                # Log the error but don't raise it - webhook failures shouldn't affect the main flow
                logger.error(f"Failed to send webhook notification: {str(e)}")

    async def get_user_webhooks(self, user_id: str) -> List[Webhook]:
        """Get all webhooks for a user"""
        filters = [Filter("user_id", user_id)]
        webhooks = await self.webhook_repository.get_many(filters=filters)
        return [webhook.as_dict() for webhook in webhooks]

    async def get_webhook_by_translation_job(self, translation_job_id: str, user_id: str) -> Webhook:
        """Get webhook for a specific translation job"""
        webhook = await self.webhook_repository.get_by(
            "translation_job_id",
            translation_job_id,
            unique=True
        )

        if not webhook:
            raise AppError(
                title="get webhook",
                message="No webhook found for this translation job",
                http_status=HTTPStatus.NOT_FOUND
            )

        if webhook.user_id != user_id:
            raise AppError(
                title="get webhook",
                message="Webhook not found",
                http_status=HTTPStatus.NOT_FOUND
            )

        return webhook.as_dict()

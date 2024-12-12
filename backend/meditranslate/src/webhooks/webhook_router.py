from meditranslate.app.shared.schemas import BaseResponseSchema
from fastapi import APIRouter, Depends, Body
from typing import Annotated
from meditranslate.app.dependancies.user import CurrentUserDep
from meditranslate.app.shared.factory import Factory
from meditranslate.app.dependancies.auth import AuthenticationRequired
from meditranslate.src.webhooks.webhook_controller import WebhookController
from meditranslate.src.webhooks.webhook_schemas import (
    WebhookCreateSchema,
    WebhookResponseSchema
)
from meditranslate.app.errors import AppError,HTTPStatus
from typing import List

class WebhookListResponseSchema(BaseResponseSchema):
    data: List[WebhookResponseSchema]

webhook_router = APIRouter(
    tags=["webhooks"],
    dependencies=[Depends(AuthenticationRequired)]
)






@webhook_router.post(
    "/register",
    response_model=WebhookResponseSchema,
    status_code=201,
    summary="Register a webhook for translation job completion"
)
async def register_webhook(
    current_user: CurrentUserDep,
    webhook_data: Annotated[WebhookCreateSchema, Body(example={
        "translation_job_id": "123e4567-e89b-12d3-a456-426614174000",
        # "callback_url": "https://example.com/webhook"
    })],
    webhook_controller: WebhookController = Depends(Factory.get_webhook_controller)
) -> WebhookResponseSchema:
    """
    Register a webhook to be notified when a translation job is completed.
    
    - **translation_job_id**: ID of the translation job to monitor
    """
        # - **callback_url**: URL that will receive the webhook POST request

    webhook_data_dict = webhook_data.model_dump()
    webhook_data_dict["user_id"] = current_user.id
    
    webhook = await webhook_controller.register_webhook(webhook_data_dict)
    return WebhookResponseSchema(
        data=webhook,
        status_code=201
    )


@webhook_router.get(
    "/{webhook_id}",
    response_model=WebhookResponseSchema,
    summary="Get webhook details"
)
async def get_webhook(
    webhook_id: str,
    current_user: CurrentUserDep,
    webhook_controller: WebhookController = Depends(Factory.get_webhook_controller)
) -> WebhookResponseSchema:
    """
    Get details of a registered webhook.
    """
    webhook = await webhook_controller.get_webhook(webhook_id)
    print(webhook)
    # # Ensure user can only access their own webhooks
    # if webhook.user_id != current_user.id:
    #     raise AppError(
    #         title="get webhook",
    #         message="Webhook not found",
    #         http_status=HTTPStatus.NOT_FOUND
    #     )
    
    return WebhookResponseSchema(
        data=webhook,
        status_code=200
    )

@webhook_router.get(
    "/user/webhooks",
    response_model=WebhookListResponseSchema,
    summary="Get all webhooks for the current user"
)
async def get_user_webhooks(
    current_user: CurrentUserDep,
    webhook_controller: WebhookController = Depends(Factory.get_webhook_controller)
) -> WebhookListResponseSchema:
    """
    Get all webhooks registered by the current user.
    """
    webhooks = await webhook_controller.get_user_webhooks(current_user.id)
    return WebhookListResponseSchema(
        data=webhooks,
        status_code=200
    )

@webhook_router.get(
    "/translation_jobs/{translation_job_id}",
    response_model=WebhookResponseSchema,
    summary="Get webhook for a specific translation job"
)
async def get_webhook_by_translation_job(
    translation_job_id: str,
    current_user: CurrentUserDep,
    webhook_controller: WebhookController = Depends(Factory.get_webhook_controller)
) -> WebhookResponseSchema:
    """
    Get webhook details for a specific translation job.
    """
    webhook = await webhook_controller.get_webhook_by_translation_job(
        translation_job_id=translation_job_id,
        user_id=current_user.id
    )
    return WebhookResponseSchema(
        data=webhook,
        status_code=200
    )
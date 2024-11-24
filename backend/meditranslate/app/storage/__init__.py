from meditranslate.app.storage.aws_s3 import AWSStorageService
from meditranslate.app.storage.base_storage_service import BaseStorageService
from meditranslate.app.configurations import aws_config, config,EnvironmentType

file_storage_service = AWSStorageService(
    config=aws_config,
    base_url=aws_config.endpoint_url,
    bucket_name=config.BUCKET_NAME,
    is_testing=False if config.ENVIRONMENT == EnvironmentType.PRODUCTION else True
)

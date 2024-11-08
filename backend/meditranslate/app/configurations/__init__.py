from meditranslate.app.configurations.app_config import AppConfig
from meditranslate.app.configurations.config import EnvironmentType
from meditranslate.app.configurations.aws_config import AWSConfig

config: AppConfig = AppConfig()

aws_config =  AWSConfig(
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    endpoint_url=config.AWS_ENDPOINT_URL,
    region_name=config.AWS_REGION_NAME,
    verify=False
)

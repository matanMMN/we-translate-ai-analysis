from fastapi import APIRouter

from meditranslate.src.common.tasks import register_tasks_endpoint
from meditranslate.src.common.ping import register_ping_endpoint
from meditranslate.src.common.health import register_health_endpoint
from meditranslate.src.common.version import register_version_endpoint
from meditranslate.src.common.uptime import register_uptime_endpoint

common_router = APIRouter()
register_ping_endpoint(common_router)
register_health_endpoint(common_router)
register_uptime_endpoint(common_router)
register_version_endpoint(common_router)
register_tasks_endpoint(common_router)

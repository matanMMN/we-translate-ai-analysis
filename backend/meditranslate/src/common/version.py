from fastapi import APIRouter
from meditranslate.app.configurations import config

def register_version_endpoint(router:APIRouter):
    @router.get("/version", summary="Version info", response_description="Version details")
    async def version():
        return await get_version()


async def get_version():
    return {
        "version": config.RELEASE_VERSION,
        "commit": "abc123def",
        "build_date": config.RELEASE_DATE
    }

from fastapi import APIRouter

def register_health_endpoint(router:APIRouter):
    @router.get("/health", summary="Health check", response_description="Health status")
    async def health():
        return await health_check()


async def health_check():
    # Example: Check database connectivity, external API, etc.
    # Here we just return a simple static check
    return {"status": "healthy"}
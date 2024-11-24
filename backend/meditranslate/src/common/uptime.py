from fastapi import APIRouter

import time

start_time = time.time()


def register_uptime_endpoint(router:APIRouter):
    @router.get("/uptime", summary="Uptime", response_description="Server uptime")
    async def uptime():
        return await get_uptime()
    

async def get_uptime():
    uptime_seconds = time.time() - start_time
    return {"uptime": uptime_seconds}
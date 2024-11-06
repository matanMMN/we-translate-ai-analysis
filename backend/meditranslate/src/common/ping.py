from fastapi import APIRouter

def register_ping_endpoint(router:APIRouter):
    @router.get("/ping", summary="ping", response_description="ping",status_code=200,response_model=None) 
    async def ping():
        return await get_ping_message()


async def get_ping_message():
    return {
        "message": "pong",
    }

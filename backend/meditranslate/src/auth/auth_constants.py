from pydantic import BaseModel


class JWTData(BaseModel):
    user_id:str

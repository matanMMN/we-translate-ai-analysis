from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,EmailStr,StringConstraints,ConfigDict
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user



# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user

class LoginSchema(BaseSchema):
    username:Annotated[str,StringConstraints()]
    password:Annotated[str,StringConstraints()]

class TokenSchema(BaseSchema):
    access_token:str
    token_type:str

class TokenResponseSchema(BaseResponseSchema):
    data:TokenSchema


class UserSessionIdentifier(BaseModel):
    user_id:str
    username:str
    email:str



import typing
from datetime import datetime,timedelta,timezone
from enum import Enum
import uuid
from typing import Optional
from pydantic import BaseModel
from jose import ExpiredSignatureError, JWTError, jwt


class JWTDecodeError(Exception):
    pass

class JWTExpiredError(Exception):
    pass

class JWTAlgorithm(str, Enum):
    HS256 = "HS256"  # HMAC with SHA-256
    HS384 = "HS384"  # HMAC with SHA-384
    HS512 = "HS512"  # HMAC with SHA-512
    RS256 = "RS256"  # RSA with SHA-256
    RS384 = "RS384"  # RSA with SHA-384
    RS512 = "RS512"  # RSA with SHA-512
    ES256 = "ES256"  # ECDSA with SHA-256
    ES384 = "ES384"  # ECDSA with SHA-384
    ES512 = "ES512"  # ECDSA with SHA-512
    PS256 = "PS256"  # RSA-PSS with SHA-256
    PS384 = "PS384"  # RSA-PSS with SHA-384
    PS512 = "PS512"  # RSA-PSS with SHA-512
    EdDSA = "EdDSA"  # Edwards-curve Digital Signature Algorithm

class JWTPayload(BaseModel):
    data: dict
    jti: str
    iat: datetime
    exp: datetime
    token_type:str


def create_jwt_token(secret_key:str,  data: dict, expire_minutes: int, token_type:Optional[str]=None, algorithm:JWTAlgorithm=JWTAlgorithm.HS256):
    to_encode = JWTPayload(
        data=data,
        jti=str(uuid.uuid4()),
        iat=datetime.now(timezone.utc),
        exp=datetime.now(timezone.utc) + timedelta(minutes=expire_minutes),
        token_type=token_type
    ).model_dump()
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm.value)
    return encoded_jwt


def decode_jwt_token(secret_key:str, token: str, algorithms:typing.List[JWTAlgorithm]=[JWTAlgorithm.HS256]):
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm.value for algorithm in algorithms])
    except ExpiredSignatureError as e:
        raise JWTExpiredError() from e
    except Exception as e:
        raise JWTDecodeError() from e


def decode_expired_jwt_token(secret_key:str, token: str,algorithms:typing.List[JWTAlgorithm]=[JWTAlgorithm.HS256]) -> dict:
    try:
        return jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm.value for algorithm in algorithms],
            options={"verify_exp": False},
        )
    except JWTError as e:
        raise JWTDecodeError() from e

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


def create_jwt_token(secret_key:str,  data: dict, expire_minutes: int, token_type:str="bearer", algorithm:JWTAlgorithm=JWTAlgorithm.HS256):
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
        algos = [algorithm.value for algorithm in algorithms]
        return jwt.decode(token, secret_key, algorithms=algos)
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


if __name__ == "__main__":
    # Setup test data
    secret_key = "test_secret"
    data = {"user_id": 123, "role": "admin"}
    expire_minutes = 5
    algorithm = JWTAlgorithm.HS256

    # Test create_jwt_token
    print("Testing create_jwt_token:")
    token = create_jwt_token(secret_key, data, expire_minutes, algorithm=algorithm)
    print(f"Generated Token: {token}\n")

    # Test decode_jwt_token (valid case)
    print("Testing decode_jwt_token (valid):")
    try:
        decoded_data = decode_jwt_token(secret_key, token, algorithms=[algorithm])
        print(f"Decoded Data: {decoded_data}\n")
    except JWTDecodeError as e:
        print(f"Error decoding JWT: {str(e)}\n")

    # Test decode_jwt_token (expired case)
    print("Testing decode_jwt_token (expired):")
    expired_token = create_jwt_token(secret_key, data, expire_minutes=-1, algorithm=algorithm)  # expired token
    try:
        decoded_data = decode_jwt_token(secret_key, expired_token, algorithms=[algorithm])
        print(f"Decoded Data (Expired): {decoded_data}\n")
    except JWTExpiredError as e:
        print(f"JWT Expired Error: {str(e)}\n")

    # Test decode_jwt_token (invalid secret key)
    print("Testing decode_jwt_token (invalid secret):")
    try:
        decoded_data = decode_jwt_token("wrong_secret", token, algorithms=[algorithm])
        print(f"Decoded Data (Invalid Secret): {decoded_data}\n")
    except JWTDecodeError as e:
        print(f"JWT Decode Error: {str(e)}\n")

    # Test decode_expired_jwt_token (with expired token)
    print("Testing decode_expired_jwt_token (expired):")
    expired_token = create_jwt_token(secret_key, data, expire_minutes=-1, algorithm=algorithm)  # expired token
    try:
        decoded_data = decode_expired_jwt_token(secret_key, expired_token, algorithms=[algorithm])
        print(f"Decoded Data (Expired Token, No Exp Check): {decoded_data}\n")
    except JWTDecodeError as e:
        print(f"Error decoding expired JWT: {str(e)}\n")

    # Test decode_expired_jwt_token (invalid secret key)
    print("Testing decode_expired_jwt_token (invalid secret):")
    try:
        decoded_data = decode_expired_jwt_token("wrong_secret", expired_token, algorithms=[algorithm])
        print(f"Decoded Data (Invalid Secret): {decoded_data}\n")
    except JWTDecodeError as e:
        print(f"JWT Decode Error: {str(e)}\n")

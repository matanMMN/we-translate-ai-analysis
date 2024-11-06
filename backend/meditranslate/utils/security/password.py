# from passlib.context import CryptContext
import bcrypt

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )


def hash_password(password: str,encoding="utf-8") -> str:
    pwd_bytes = password.encode(encoding)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password



def verify_password(plain_password: str, hashed_password: bytes,encoding="utf-8") -> bool:
    password_byte_enc = plain_password.encode(encoding)
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password)
    # return pwd_context.verify(plain_password, hashed_password)

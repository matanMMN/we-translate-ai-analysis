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

# Minimum eight characters, at least one letter and one number:
PASSWORD_REGEX = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

# Minimum eight characters, at least one letter, one number and one special character:
PASSWORD_REGEX = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

# Minimum eight characters, at least one uppercase letter, one lowercase letter and one number:
PASSWORD_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

# Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:
PASSWORD_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

# Minimum eight and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character:
PASSWORD_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$"

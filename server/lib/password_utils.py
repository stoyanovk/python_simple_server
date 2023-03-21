import bcrypt


def generate_password(password: str) -> bytes:
    b64_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(b64_password, salt)


def check_password(password: str, hashed_password: bytes) -> bool:
    b64_password = password.encode("utf-8")
    return bcrypt.checkpw(b64_password, hashed_password)

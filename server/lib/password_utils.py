import bcrypt


def generate_password(password):
    b64_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(b64_password, salt)


def check_password(password, hashed_password):
    b64_password = password.encode("utf-8")
    return bcrypt.checkpw(b64_password, hashed_password)

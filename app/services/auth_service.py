from passlib.context import CryptContext
from app.database.mongodb import db
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_user(
    username,
    password
):
    hashed_password = hash_password(
        password
    )

    result = db.users.insert_one({
        "username": username,
        "password": hashed_password
    })

    return str(result.inserted_id)


def get_user(username):

    return db.users.find_one(
        {"username": username}
    )


def create_access_token(
    username
):

    expire = datetime.utcnow() + timedelta(
        hours=24
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload["sub"]

    except JWTError:

        return None
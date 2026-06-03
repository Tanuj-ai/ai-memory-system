from fastapi import APIRouter, Header
from typing import Annotated
from fastapi import Header
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
from app.models.user import (
    UserRegister,
    UserLogin
)

from app.services.auth_service import (
    create_user,
    get_user,
    verify_password,
    create_access_token,
    verify_token
)

router = APIRouter()


@router.post("/register")
def register(user: UserRegister):

    user_id = create_user(
        user.username,
        user.password
    )

    return {
        "message": "User registered",
        "user_id": user_id
    }


@router.post("/login")
def login(user: UserLogin):

    db_user = get_user(
        user.username
    )

    if not db_user:

        return {
            "message": "User not found"
        }

    valid = verify_password(
        user.password,
        db_user["password"]
    )

    if not valid:

        return {
            "message": "Invalid password"
        }

    token = create_access_token(
        user.username
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }




@router.get("/me")
def me(
    token: str = Depends(
        oauth2_scheme
    )
):

    username = verify_token(
        token
    )

    if not username:

        return {
            "message": "Invalid token"
        }

    return {
        "username": username
    }
@router.get("/test-header")
def test_header(
    authorization: str = Header(None)
):
    return {
        "authorization": authorization
    }
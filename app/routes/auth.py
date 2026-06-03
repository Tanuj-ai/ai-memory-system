from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
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

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


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
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    db_user = get_user(
        form_data.username
    )

    if not db_user:
        return {
            "message": "User not found"
        }

    valid = verify_password(
        form_data.password,
        db_user["password"]
    )

    if not valid:
        return {
            "message": "Invalid password"
        }

    token = create_access_token(
        form_data.username
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
    token: str = Depends(
        oauth2_scheme
    )
):

    return {
        "token": token
    }
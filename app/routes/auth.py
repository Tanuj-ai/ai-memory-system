from fastapi import APIRouter
from app.models.user import (
    UserRegister
)

router = APIRouter()

@router.post("/register")
def register(
    user: UserRegister
):

    return {
        "username": user.username,
        "message": "User registered"
    }
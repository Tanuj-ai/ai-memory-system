from fastapi import FastAPI
from app.routes.chat import router
from app.routes.auth import router as auth_router
app = FastAPI()
app.include_router(
    auth_router
)
app.include_router(router)


@app.get("/")
def home():

    return {
        "message": "AI Memory System Running"
    }

from app.database.mongodb import db

@app.get("/all")
def all_memories():
    return list(
        db.memories.find(
            {},
            {"_id": 0}
        )
    )
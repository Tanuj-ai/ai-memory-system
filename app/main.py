from fastapi import FastAPI
from app.database.mongodb import db

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "AI Memory System Running"
    }

@app.get("/test-db")
def test_db():
    db.test.insert_one({"status": "connected"})

    return {
        "message": "MongoDB Connected Successfully"
    }
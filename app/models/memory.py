from pydantic import BaseModel


class MemoryCreate(BaseModel):
    memory: str


class ChatRequest(BaseModel):
    message: str
from pydantic import BaseModel

class MemoryCreate(BaseModel):
    user_id: str
    memory: str


class ChatRequest(BaseModel):
    user_id: str
    message: str
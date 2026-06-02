from fastapi import APIRouter

from app.models.memory import (
    MemoryCreate,
    ChatRequest
)

from app.services.memory_service import (
    create_memory,
    get_memories,
    delete_memory
)

from app.services.context_service import (
    get_user_context
)

from app.services.fake_llm import (
    generate_response
)

router = APIRouter()


@router.post("/chat")
def chat(data: ChatRequest):

    context = get_user_context(
        data.user_id
    )

    response = generate_response(
        data.message,
        context
    )

    return {
        "response": response
    }


@router.post("/memory")
def save_memory(data: MemoryCreate):

    memory_id = create_memory(
        data.user_id,
        data.memory
    )

    return {
        "message": "Memory saved",
        "memory_id": memory_id
    }


@router.get("/memory/{user_id}")
def fetch_memories(user_id: str):

    return get_memories(user_id)


@router.delete("/memory/{memory_id}")
def remove_memory(memory_id: str):

    deleted = delete_memory(memory_id)

    if deleted:
        return {
            "message": "Memory deleted"
        }

    return {
        "message": "Memory not found"
    }
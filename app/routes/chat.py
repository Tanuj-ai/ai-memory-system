from fastapi import APIRouter
from app.services.categorizer import categorize_memory

from app.models.memory import (
    MemoryCreate,
    ChatRequest
)

from app.services.memory_service import (
    create_memory,
    get_memories,
    get_memories_by_category,
    delete_memory
)

from app.services.context_service import (
    get_user_context
)

from app.services.fake_llm import (
    generate_response
)

from app.services.importance_service import calculate_importance
from app.services.memory_extractor import extract_memory

router = APIRouter()


@router.post("/chat")
def chat(data: ChatRequest):

    memory = extract_memory(
        data.message
    )

    if memory:

        importance = calculate_importance(
            memory
        )

        category = categorize_memory(
            memory
        )

        create_memory(
            data.user_id,
            memory,
            importance,
            category
        )

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


@router.get("/memory/{user_id}/{category}")
def fetch_memories_by_category(
    user_id: str,
    category: str
):

    return get_memories_by_category(
        user_id,
        category
    )


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

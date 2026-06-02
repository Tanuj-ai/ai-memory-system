
from fastapi import APIRouter

from app.models.memory import (
    MemoryCreate,
    ChatRequest
)

from app.services.memory_service import (
    create_memory,
    get_memories_by_category,
    delete_memory
)

from app.services.memory_extractor import (
    extract_memory
)

from app.services.importance_service import (
    calculate_importance
)

from app.services.categorizer import (
    categorize_memory
)

from app.services.semantic_search import (
    semantic_search
)

from app.services.prompt_builder import (
    build_prompt
)

from app.services.gemini_service import (
    generate_response
)

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

    memories = semantic_search(
        data.user_id,
        data.message
    )

    prompt = build_prompt(
        data.message,
        memories
    )
    

    response = generate_response(
        prompt
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
@router.get("/search/{user_id}")
def search_memory(
    user_id: str,
    query: str
):

    return semantic_search(
        user_id,
        query
    )
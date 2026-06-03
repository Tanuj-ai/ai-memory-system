from fastapi import APIRouter, Depends

from app.services.auth_service import (
    get_current_user
)

from app.models.memory import (
    MemoryCreate,
    ChatRequest
)

from app.services.forget_detector import (
    is_forget_request
)

from app.services.memory_service import (
    create_memory,
    get_memories_by_category,
    delete_memory,
    find_memory_by_text
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
def chat(
    data: ChatRequest,
    username: str = Depends(
        get_current_user
    )
):

    # Forget memory request
    if is_forget_request(
        data.message
    ):

        memory_to_delete = find_memory_by_text(
            username,
            data.message
        )

        if memory_to_delete:

            delete_memory(
                str(memory_to_delete["_id"])
            )

            return {
                "response": "Memory deleted."
            }

        return {
            "response": "Memory not found."
        }

    # Extract and save memory
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
            username,
            memory,
            importance,
            category
        )

    # Search memories
    memories = semantic_search(
        username,
        data.message
    )

    # Build prompt
    prompt = build_prompt(
        data.message,
        memories
    )

    # Gemini response
    response = generate_response(
        prompt
    )

    return {
        "response": response
    }


@router.post("/memory")
def save_memory(
    data: MemoryCreate,
    username: str = Depends(
        get_current_user
    )
):

    memory_id = create_memory(
        username,
        data.memory
    )

    return {
        "message": "Memory saved",
        "memory_id": memory_id
    }


@router.get("/memory/{category}")
def fetch_memories_by_category(
    category: str,
    username: str = Depends(
        get_current_user
    )
):

    return get_memories_by_category(
        username,
        category
    )


@router.delete("/memory/{memory_id}")
def remove_memory(
    memory_id: str
):

    deleted = delete_memory(
        memory_id
    )

    if deleted:

        return {
            "message": "Memory deleted"
        }

    return {
        "message": "Memory not found"
    }


@router.get("/search")
def search_memory(
    query: str,
    username: str = Depends(
        get_current_user
    )
):

    return semantic_search(
        username,
        query
    )
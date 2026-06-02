from app.services.embedding_service import (
    generate_embedding
)

from app.services.qdrant_service import (
    search_memories
)


def semantic_search(
    user_id,
    query
):

    query_embedding = generate_embedding(
        query
    )

    results = search_memories(
        query_embedding
    )

    response = []

    for hit in results:

        response.append({
            "memory":
                hit.payload["memory"],
            "score":
                hit.score
        })

    return response
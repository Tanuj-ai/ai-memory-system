
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
    print("SEMANTIC SEARCH CALLED")
    query_embedding = generate_embedding(
        query
    )

    results = search_memories(
        user_id,
        query_embedding
    )

    print("USER:", user_id)
    print("QUERY:", query)
    print("RESULTS:", results)

    response = []

    for hit in results:

        print("PAYLOAD:", hit.payload)

        response.append({
            "memory": hit.payload["memory"]
        })

    return response
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
    
)

client = QdrantClient(
    host="localhost",
    port=6333
)

collections = client.get_collections()

if not any(
    c.name == "memories"
    for c in collections.collections
):

    client.create_collection(
        collection_name="memories",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

def insert_memory(
    memory_id,
    embedding,
    user_id,
    memory
):

    client.upsert(
        collection_name="memories",
        points=[
            PointStruct(
                id=memory_id,
                vector=embedding,
                payload={
                    "user_id": user_id,
                    "memory": memory,
                    "category": category,
                    "importance": importance
                }
            )
        ]
    )

def search_memories(
    user_id,
    query_embedding,
    limit=5
):

    results = client.query_points(
        collection_name="memories",
        query=query_embedding,
        limit=limit,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(
                        value=user_id
                    )
                )
            ]
        )
    )

    return results.points
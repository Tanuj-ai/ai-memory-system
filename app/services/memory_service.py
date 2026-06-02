from app.database.mongodb import db
from bson import ObjectId
from datetime import datetime
from app.services.embedding_service import (
    generate_embedding
)
def create_memory(user_id, memory, importance=0.5, category="general"):
    embedding = generate_embedding(
    memory
    )

    existing_memory = db.memories.find_one({
        "user_id": user_id,
        "memory": memory
    })

    if existing_memory:
        return "already_exists"

    result = db.memories.insert_one({
    "user_id": user_id,
    "memory": memory,
    "importance": importance,
    "category": category,
    "embedding": embedding,
    "created_at": datetime.utcnow()
})

    return str(result.inserted_id)


def get_memories(user_id):

    memories = list(
        db.memories.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("importance", -1)
    )

    return memories


def delete_memory(memory_id):

    result = db.memories.delete_one(
        {"_id": ObjectId(memory_id)}
    )

    return result.deleted_count
def get_memories_by_category(user_id, category):

    memories = list(
        db.memories.find(
            {
                "user_id": user_id,
                "category": category
            },
            {"_id": 0}
        )
    )

    return memories
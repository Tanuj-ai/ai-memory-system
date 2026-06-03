from app.database.mongodb import db
from bson import ObjectId
from datetime import datetime
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import insert_memory
def create_memory(
    user_id,
    memory,
    importance=0.5,
    category="general"
):

    embedding = generate_embedding(
        memory
    )

    result = db.memories.insert_one({
    "user_id": user_id,
    "memory": memory,
    "importance": importance,
    "category": category,
    "created_at": datetime.utcnow()
})

    memory_id = str(
        result.inserted_id
    )

    qdrant_id = abs(
        hash(memory_id)
    )

    db.memories.update_one(
        {
            "_id": result.inserted_id
        },
        {
            "$set": {
                "qdrant_id": qdrant_id
            }
        }
    )

    insert_memory(
        qdrant_id,
        embedding,
        user_id,
        memory,
        category,
        importance
    )

    return memory_id

    # Insert vector into Qdrant
    insert_memory(
    abs(hash(memory_id)),
    embedding,
    user_id,
    memory,
    category,
    importance
)
def find_memory_by_text(
    user_id,
    text
):

    return db.memories.find_one({
        "user_id": user_id,
        "memory": {
            "$regex": text,
            "$options": "i"
        }
    })

def get_memories(user_id):

    memories = list(
      db.memories.find(
    {"user_id": user_id},
    {
        "_id": 0,
        "embedding": 0
    }
)
    )

    return memories


def delete_memory(
    memory_id
):

    memory = db.memories.find_one(
        {
            "_id": ObjectId(memory_id)
        }
    )

    if not memory:
        return False

    from app.services.qdrant_service import (
        delete_memory_vector
    )

    if "qdrant_id" in memory:

        delete_memory_vector(
            memory["qdrant_id"]
        )

    result = db.memories.delete_one(
        {
            "_id": ObjectId(memory_id)
        }
    )

    return result.deleted_count > 0
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
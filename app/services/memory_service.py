from app.database.mongodb import db
from bson import ObjectId


def create_memory(user_id, memory):
    result = db.memories.insert_one({
        "user_id": user_id,
        "memory": memory
    })

    print("Inserted ID:", result.inserted_id)

    return str(result.inserted_id)


def get_memories(user_id):
    memories = list(
        db.memories.find(
            {"user_id": user_id},
            {"_id": 0}
        )
    )

    return memories


def delete_memory(memory_id):
    result = db.memories.delete_one(
        {"_id": ObjectId(memory_id)}
    )

    return result.deleted_count
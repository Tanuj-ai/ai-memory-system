from app.database.mongodb import db


def get_user_context(user_id):

    memories = list(
        db.memories.find(
            {"user_id": user_id},
            {"_id": 0}
        )
    )

    context = ""

    for memory in memories:
        context += f"- {memory['memory']}\n"

    return context
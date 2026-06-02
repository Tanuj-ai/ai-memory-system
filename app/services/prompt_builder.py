def build_prompt(
    user_message,
    memories
):

    memory_text = "\n".join(
        [
            f"- {m['memory']}"
            for m in memories
        ]
    )

    return f"""
You are a personal AI assistant.

The following facts are known about the user:

{memory_text}

Answer the user's question using these facts whenever relevant.

User Question:
{user_message}
"""
def generate_response(message, context):

    return f"""
User Memory:
{context}

Current Message:
{message}
"""
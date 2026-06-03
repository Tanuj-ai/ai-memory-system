def is_forget_request(message):

    message = message.lower()

    keywords = [
        "forget",
        "delete",
        "remove"
    ]

    return any(
        keyword in message
        for keyword in keywords
    )
def is_update_request(
    message
):

    message = message.lower()

    keywords = [
        "actually",
        "instead",
        "changed",
        "correction"
    ]

    return any(
        keyword in message
        for keyword in keywords
    )
def extract_memory(message):

    trigger_phrases = [
        "i am",
        "i'm",
        "i like",
        "i love",
        "i play",
        "i study",
        "my name is"
    ]

    message_lower = message.lower()

    for phrase in trigger_phrases:
        if phrase in message_lower:
            return message

    return None
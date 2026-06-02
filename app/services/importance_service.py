def calculate_importance(memory):

    memory = memory.lower()

    high_value = [
        "my name is",
        "i am",
        "i study",
        "i work",
        "i live"
    ]

    medium_value = [
        "i play",
        "i like",
        "i love"
    ]

    for phrase in high_value:
        if phrase in memory:
            return 0.9

    for phrase in medium_value:
        if phrase in memory:
            return 0.7

    return 0.3
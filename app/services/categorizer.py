def categorize_memory(memory):

    memory = memory.lower()

    if "study" in memory or "mca" in memory:
        return "education"

    if "play" in memory or "volleyball" in memory:
        return "hobby"

    if "name" in memory:
        return "identity"

    return "general"
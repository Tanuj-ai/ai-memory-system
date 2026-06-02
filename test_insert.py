from app.services.qdrant_service import (
    insert_memory
)

insert_memory(
    1,
    [0.1] * 384,
    "tanuj",
    "I play volleyball"
)

print("Inserted")
# test_insert_real.py

from app.services.embedding_service import (
    generate_embedding
)

from app.services.qdrant_service import (
    insert_memory
)

embedding = generate_embedding(
    "I like volleyball"
)

insert_memory(
    1,
    embedding,
    "tanuj",
    "I like volleyball"
)

print("Inserted")
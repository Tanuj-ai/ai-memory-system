from app.services.embedding_service import (
    generate_embedding
)

vector = generate_embedding(
    "I play volleyball"
)

print(len(vector))
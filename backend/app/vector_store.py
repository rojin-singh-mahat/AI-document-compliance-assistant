from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient( url = "http://localhost:6333" )

COLLECTION_NAME = "documents"

def create_collection():
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name = COLLECTION_NAME,
            vectors_config = VectorParams(
                size = 384,
                distance = Distance.COSINE
            )
        )

def store_chunks(chunks, embeddings):
    points = []

    for i, (chunk, embeddings) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id = i,
                vector = embeddings,
                payload = {
                    "text" : chunk,
                    "chunk_index" : i
                }
            )
        )

    client.upsert( collection_name = COLLECTION_NAME, points = points)
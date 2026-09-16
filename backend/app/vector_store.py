from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from uuid import uuid4

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

def delete_collection(COLLECTION_NAME):
    """
    CAUTION: deletes the entire qdrant collection
    """
    client.delete_collection(COLLECTION_NAME)
    print("COllection ", COLLECTION_NAME, " was deleted.")

def store_chunks(chunks, embeddings, document_id, filename):
    points = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        chunk_id = str(uuid4())

        points.append(
            PointStruct(
                id = chunk_id,
                vector = embedding,
                payload = {
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": i,
                    "text": chunk
                }
            )
        )

    client.upsert( collection_name = COLLECTION_NAME, points = points)

def search_chunks(query_embedding, document_id = None, limit = 3):
    search_filter = None

    if document_id:
        search_filter = {
            "must": [
                {
                    "key": "document_id",
                    "match": { "value": document_id}
                }
            ]
        }

    results = client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_embedding,
        query_filter = search_filter,
        limit = limit,
        with_payload = True
    ).points

    return results
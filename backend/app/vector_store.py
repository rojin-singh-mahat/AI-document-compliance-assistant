from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from uuid import uuid4

client = QdrantClient( url = "http://localhost:6333" )

COLLECTION_NAME = "documents"

def create_collection():
    """
    Creates the Qdrant document collection if it does not already exist.
    """
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
    Deletes the specified Qdrant collection.

    Warning:
        This permanently deletes all vectors and payloads in the collection.

    Parameters:
        COLLECTION_NAME (str): Name of the collection to delete.
    """
    client.delete_collection(COLLECTION_NAME)
    print("COllection ", COLLECTION_NAME, " was deleted.")

def store_chunks(chunks, embeddings, document_id, filename):
    """
    Stores document chunks and their embeddings in Qdrant.

    Parameters:
        chunks (list[str]): Document chunks.
        embeddings (list): Embedding vectors corresponding to each chunk.
        document_id (str): Unique ID of the document.
        filename (str): Original document filename.
    """
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

def search_chunks(query_embedding, document_id=None, limit=3):
    """
    Searches Qdrant for chunks similar to a query embedding.

    Parameters:
        query_embedding (list): Embedding vector of the search query.
        document_id (str, optional): ID of the document to search within.
        limit (int): Maximum number of results to return.

    Returns:
        list: Matching Qdrant points with their payloads and scores.
    """
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
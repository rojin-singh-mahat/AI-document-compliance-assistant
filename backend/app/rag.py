from app.embeddings import generate_embeddings
from app.vector_store import search_chunks

def retrieve_context(query, document_id = None, limit = 3):
    query_embedding = generate_embeddings(query)

    results = search_chunks(
        query_embedding = query_embedding,
        document_id = document_id,
        limit = limit
    )

    context = []

    for result in results:
        context.append(
            {
                "text": result.payload["text"],
                "filename": result.payload["filename"],
                "chunk_index": result.payload["chunk_index"],
                "score": result.score
            }
        )

    return context

def build_context(results):
    return "\n\n".join(
        result["text"] for result in results
    )
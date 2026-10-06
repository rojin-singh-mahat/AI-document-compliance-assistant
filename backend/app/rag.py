from app.embeddings import generate_embeddings
from app.vector_store import search_chunks

def retrieve_context(query, document_id=None, limit=3):
    """
    Retrieves the most relevant document chunks for a query.

    Parameters:
        query (str): User's question or search query.
        document_id (str, optional): ID of the document to search within.
        limit (int): Maximum number of chunks to retrieve.

    Returns:
        list[dict]: Retrieved chunks with their text, filename,
        chunk index, and similarity score.
    """
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
    """
    Combines retrieved chunks into a single context string.

    Parameters:
        results (list[dict]): Retrieved document chunks.

    Returns:
        str: Combined text used as context for the LLM.
    """
    return "\n\n".join(
        result["text"] for result in results
    )
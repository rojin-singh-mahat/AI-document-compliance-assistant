from app.embeddings import generate_embeddings
from app.vector_store import search_chunks

query = "what tests were perfromed in the web application?"

query_embedding = generate_embeddings(query)

document_id = "2ea2b20e-4d7d-416d-8014-4145b0341ffa"

results = search_chunks(query_embedding, document_id)

for result in results:
    print(f"\nScore: {result.score:.4f}")
    print(f"File: {result.payload['filename']}")
    print(f"Document: {result.payload['document_id']}")
    print(f"Text: {result.payload['text'][:300]}...")

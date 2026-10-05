from app.vector_store import search_chunks
from app.embeddings import generate_embeddings

query = "What are the company's responsibilities for protecting personal data?"

query_embedding = generate_embeddings([query])[0]

print(type(query_embedding))
print(type(query_embedding[0]))
print(len(query_embedding))

document_id = "2ea2b20e-4d7d-416d-8014-4145b0341ffa"

results = search_chunks(
    query_embedding,
    document_id=document_id,
    limit=3
)

for result in results:
    print(f"\nScore: {result.score:.4f}")
    print(f"File: {result.payload['filename']}")
    print(f"Chunk: {result.payload['chunk_index']}")
    print(f"Document: {result.payload['document_id']}")
    print(f"Text: {result.payload['text'][:300]}...")
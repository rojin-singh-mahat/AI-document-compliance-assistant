from app.rag import retrieve_context, build_context
from app.llm import generate_asnwer

query = "What problem does the project aim to solve?"

document_id = "2ea2b20e-4d7d-416d-8014-4145b0341ffa"

results = retrieve_context(
    query,
    document_id=document_id,
    limit=3
)

print("\n=== RETRIEVED CHUNKS ===")

for result in results:
    print(f"\nScore: {result['score']}")
    print(f"File: {result['filename']}")
    print(f"Chunk: {result['chunk_index']}")
    print(f"Text: {result['text']}")

context = build_context(results)

answer = generate_asnwer(query, context)

print("\n=== ANSWER ===")
print(answer)
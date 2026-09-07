from vector_store import client, COLLECTION_NAME
from embeddings import generate_embedding

query = "What are the company's responsibilities for pretecting personal data?"

query_embedding = generate_embedding([query])[0]

results = client.query_points(
    collection_name = COLLECTION_NAME,
    query = query_embedding,
    limit = 3,
    with_payload = True,
).points

print("\n QUery: ", query)
print("\n Results:")

for result in results:
    print(f"\n Score: {result.score:.4f}")
    print(result.payload["text"])
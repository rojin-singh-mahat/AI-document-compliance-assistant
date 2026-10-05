from app.vector_store import client, COLLECTION_NAME

results = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=100,
    with_payload=True,
)[0]

for point in results:
    payload = point.payload

    print(
        f"ID: {point.id} | "
        f"Document: {payload['document_id']} | "
        f"File: {payload['filename']} | "
        f"Chunk: {payload['chunk_index']}"
    )
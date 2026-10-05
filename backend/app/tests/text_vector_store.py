from embeddings import generate_embedding
from vector_store import client, COLLECTION_NAME, create_collection, store_chunks

chunks = [
    "The company must comply with data protection regulations.",
    "Personal information must be stored securely.",
    "Users have right to access their personal information."
]

embeddings = generate_embedding(chunks)

create_collection()

store_chunks(chunks, embeddings)

print("Chunks have been stored successfully.")

print(client.count(
    collection_name = COLLECTION_NAME,
    exact = True
))
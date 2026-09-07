from main import chunk_text
from embeddings import generate_embedding

text = """
The company must comply with data protection regulations.

Personal information must be stored securely.

Users have the right to request access to their personal information.
"""

chunks = chunk_text(text)
embeddings = generate_embedding(chunks)

print("number of chunks: ", len(chunks))
print("number of embeddings: ", len(embeddings))

for i, embedding in enumerate(embeddings):
    print(f"Chunk {i + 1}:")
    print("Text:", chunks[i])
    print("Vector dimensions:", len(embedding))
    print()
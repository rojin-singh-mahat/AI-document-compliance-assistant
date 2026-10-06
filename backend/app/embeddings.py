from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(text):
    """
    Generates vector embeddings using the all-MiniLM-L6-v2 model.

    Parameters:
        text (str or list[str]): Text to embed.

    Returns:
        list: Generated embedding vector(s).
    """
    embedding = model.encode(text)

    return embedding.tolist()
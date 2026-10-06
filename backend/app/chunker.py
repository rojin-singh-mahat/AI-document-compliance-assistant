import re
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    """
    Counts the number of tokens in the given text.

    Parameters:
        text (str): Text to tokenize.

    Returns:
        int: Number of tokens in the text.
    """
    return len(tokenizer.encode(text))

def split_text(text, max_tokens=500, overlap=50):
    """
    Splits text into chunks using recursive splitting and overlap.

    Parameters:
        text (str): Text to split.
        max_tokens (int): Maximum number of tokens per chunk.
        overlap (int): Number of overlapping tokens between chunks.

    Returns:
        list[str]: List of text chunks.
    """
    if overlap >= max_tokens:
        raise ValueError("overlap must be smaller than max_tokens")
    
    separators = ["\n\n", "\n", ". ", " "]

    content_tokens = max_tokens - overlap

    chunks = recursive_split(text, separators, content_tokens)

    return add_overlap(chunks, overlap)

def recursive_split(text, separators, max_tokens):
    """
    Recursively splits text until chunks fit within the token limit.

    Parameters:
        text (str): Text to split.
        separators (list[str]): Separators used during recursive splitting.
        max_tokens (int): Maximum number of tokens per chunk.

    Returns:
        list[str]: List of text chunks.
    """
    text = text.strip() # remove trailing whitespaces
    if not text: # no text? return nothing
        return []

    if count_tokens(text) <= max_tokens: # the text is already small enuff; no splitting needed
        return [text]

    if not separators: # separator array is empty; hard split
        return hard_split(text, max_tokens)

    # separate text
    separator = separators[0]

    parts = text.split(separator)

    if len(parts) == 1: # if the separator didn't split anything; try the next separator
        return recursive_split(text, separators[1:], max_tokens)

    chunks = []
    current = ""

    for part in parts:
        part = part.strip()

        if not part:
            continue

        candidate = (current + separator + part # add the separated parts one by one to a candidate string
                     if current
                     else part)

        if count_tokens(candidate) <= max_tokens: #check if the candidate string exceeds teh token limit
            current = candidate
        else:
            if current:
                chunks.append(current)

            if count_tokens(part) <= max_tokens:
                current = part
            else: # if the part is still too big; split it further by the next level of separator
                chunks.extend( recursive_split( part, separators[1:], max_tokens))
                current = "" # once everything is done, empty the current variable
    if current:
        chunks.append(current)

    return chunks

def hard_split(text, max_tokens):
    """
    Splits text into chunks based on the token limit.

    Parameters:
        text (str): Text to split.
        max_tokens (int): Maximum number of tokens per chunk.

    Returns:
        list[str]: List of separated text chunks.
    """
    tokens = tokenizer.encode(text)
    chunks = []

    for start in range(0, len(tokens), max_tokens):
        chunk_token = tokens[start:start + max_tokens]
        chunks.append(tokenizer.decode(chunk_token))

    return chunks

def add_overlap(chunks, overlap):
    """
    Adds overlapping tokens to each chunk after the first.

    Parameters:
        chunks (list[str]): Text chunks.
        overlap (int): Number of tokens to overlap between chunks.

    Returns:
        list[str]: Chunks with overlapping text.
    """
    if not chunks or overlap <= 0:
        return chunks

    new_chunk = [chunks[0]] # start with the first chunk

    for i in range(1, len(chunks)):
        previous_chunk = chunks[i-1]
        current_chunk = chunks[i]

        previous_tokens = tokenizer.encode(previous_chunk)
        overlap_tokens = previous_tokens[-overlap:]
        overlap_text = tokenizer.decode(overlap_tokens)

        combined_chunk = (overlap_text + " " + current_chunk).strip()

        new_chunk.append(combined_chunk)

    return new_chunk

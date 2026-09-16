import re
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(tokenizer.encode(text))

def split_text(text, max_tokens = 500, overlap = 50):
    if overlap >= max_tokens:
        raise ValueError("overlap must be smaller than max_tokens")
    
    separators = ["\n\n", "\n", ". ", " "]

    content_tokens = max_tokens - overlap

    chunks = recursive_split(text, separators, content_tokens)

    return add_overlap(chunks, overlap)

def recursive_split(text, separators, max_tokens):
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
    tokens = tokenizer.encode(text)
    chunks = []

    for start in range(0, len(tokens), max_tokens):
        chunk_token = tokens[start:start + max_tokens]
        chunks.append(tokenizer.decode(chunk_token))

    return chunks

def add_overlap(chunks, overlap):
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

import re
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")


def remove_table_of_contents(text):
    lines = text.splitlines()

    toc_start = None
    toc_end = None

    # Find the start of the table of contents
    for i, line in enumerate(lines):
        if line.strip().lower() in {"contents", "table of contents"}:
            toc_start = i
            break

    # No TOC found
    if toc_start is None:
        return text

    # Find the first real section after the TOC
    for i in range(toc_start + 1, len(lines)):
        if re.match(r"^\s*introduction\b", lines[i], re.IGNORECASE):
            toc_end = i
            break

    # If we couldn't determine where the TOC ends,
    # don't delete anything.
    if toc_end is None:
        return text

    # Keep everything before the TOC and everything after it
    cleaned_lines = lines[:toc_start] + lines[toc_end:]

    return "\n".join(cleaned_lines)
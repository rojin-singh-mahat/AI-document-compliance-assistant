from chunker import split_text, count_tokens, add_overlap

text = """
Paragraph A is about compliance and data protection.

Paragraph B is about automated workflows and API security. This paragraph contains a lot more information about automated workflows, API security, authentication, authorization, database systems, data validation, monitoring, logging, and secure communication between different services.

Paragraph C is about infrastructure and database limits.
"""

chunks = split_text(text, max_tokens=20, overlap = 5)

for i, chunk in enumerate(chunks):
    print(f"\nCHUNK {i}")
    print(chunk)
    print("TOKENS:", count_tokens(chunk))

chunks = [
    "one two three four five",
    "six seven eight nine ten",
    "eleven twelve thirteen fourteen fifteen"
]

result = add_overlap(chunks, 2)

for chunk in result:
    print(chunk)
    print("TOKENS:", count_tokens(chunk))
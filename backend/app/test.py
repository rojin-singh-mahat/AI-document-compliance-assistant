import pymupdf
from collections import Counter

file_path = "uploads/RAG_Noisy_Document_Example.pdf"

document = pymupdf.open(file_path)
for page_number, page in enumerate(document):
    text = page.get_text("text", sort=True).strip()

    print(f"\n--- PAGE {page_number + 1} ---")
    print(text)

top_lines = []
bottom_lines = []

for page in document:
    text = page.get_text("text", sort=True).strip()

    if not text:
        continue

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        continue

    top_lines.append(lines[0])
    bottom_lines.append(lines[-1])

document.close()

print("\nTOP LINES:")
for line, count in Counter(top_lines).most_common(20):
    if count > 1:
        print(count, repr(line))

print("\nBOTTOM LINES:")
for line, count in Counter(bottom_lines).most_common(20):
    if count > 1:
        print(count, repr(line))
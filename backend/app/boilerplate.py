from collections import defaultdict
import pymupdf

def find_repeated_blocks(file_path):
    """
    Finds repeated blocks of text in a PDF file.

    Parameters:
        file_path (str): Path to the PDF file.

    Returns:
        list[dict]: Repeated blocks with their position, location,
        number of occurrences, and text.
    """
    coordinate_tracker = defaultdict(list)

    with pymupdf.open(file_path) as document:
        total_pages = len(document)

        for page in document:
            page_height = page.rect.height
            blocks = page.get_text("blocks")

            for block in blocks:
                x0,y0, x1,y1, text, *_ = block
                text = text.strip()
                if not text:
                    continue

                position = (round(x0), round(y0),
                            round(x1), round(y1))
                
                coordinate_tracker[position].append({"text": text, "page_height": page_height})

    repeated_blocks = []
    for position, instances in coordinate_tracker.items():
        if len(instances)/total_pages < 0.5:
            continue

        y0 = position[1]
        page_height = instances[0]["page_height"]

        if y0 < page_height *0.15:
            location  = "header"
        elif y0 > page_height * 0.85:
            location = "footer"
        else:
            continue

        repeated_blocks.append({
            "position": position,
            "location": location,
            "occurrences": len(instances),
            "texts": [item["text"] for item in instances]
        })

    return repeated_blocks

def get_boilerplate_positions(file_path):
    """
    Finds the positions of repeated boilerplate blocks in a PDF.

    Parameters:
        file_path (str): Path to the PDF file.

    Returns:
        set[tuple]: Positions of repeated blocks on the PDF pages.
    """
    repeated_blocks = find_repeated_blocks(file_path)
    return {
        item["position"] for item in repeated_blocks
    }

def extract_clean_pages(file_path):
    """
    Extracts text from a PDF while removing repeated boilerplate
    and table of contents/figures pages.

    Parameters:
        file_path (str): Path to the PDF file.

    Returns:
        list[dict]: Cleaned page text with its corresponding page number.
    """
    positions = get_boilerplate_positions(file_path)
    cleaned_pages = []

    with pymupdf.open(file_path) as document:
        for page_number, page in enumerate(document, start=1):
            cleaned_blocks = []

            for block in page.get_text("blocks"):
                x0, y0, x1, y1, text, *_ = block
                position = (round(x0),round(y0),
                            round(x1),round(y1))

                if position in positions:
                    continue

                text = text.strip()
                if text:
                    cleaned_blocks.append(text)
            cleaned_text = "\n\n".join(cleaned_blocks)
            first_line = cleaned_text.splitlines()[0] if cleaned_text.strip() else ""
            first_words = first_line.split()[:3]
            heading = " ".join(word.strip().lower() for word in first_words)

            if heading.startswith("table of contents"):
                continue
            if heading.startswith("contents"):
                continue
            if heading.startswith("table of figures"):
                continue
            if cleaned_text:
                cleaned_pages.append({
                    "page_number": page_number,
                    "text": cleaned_text
                })
    return cleaned_pages

if __name__ == "__main__":
    pdf_path = r"C:\Users\rojin\Downloads\RAG_Noisy_Document_Example.pdf"
    repeated = find_repeated_blocks(pdf_path)
   
    positions = get_boilerplate_positions(pdf_path)
    print("\nPositions to remove:", positions)
    for item in repeated:
        print(f"\nLocation: {item['location']}")
        print("\nPosition: ", item["position"])
        print("\nOccurences: ", item["occurrences"])

        for text in item["texts"]:
            print(repr(text))

    pages = extract_clean_pages(pdf_path)
    for page in pages:
        print(f"\n--- Page {page["page_number"]} ---")
        print(page["text"])
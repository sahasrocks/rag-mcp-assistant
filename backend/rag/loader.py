import os
from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def load_documents_from_folder(folder_path="documents"):
    all_text = []

    if not os.path.exists(folder_path):
        return ""

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

        elif filename.endswith(".pdf"):
            content = extract_text_from_pdf(file_path)

        else:
            continue

        if content.strip():
            content_with_header = (
                f"\n\n--- FILE: {filename} ---\n\n{content}"
            )
            all_text.append(content_with_header)

    return "\n".join(all_text)
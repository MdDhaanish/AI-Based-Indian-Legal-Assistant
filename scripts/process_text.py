import os
import re
import json

# Folder paths
EXTRACTED_DIR = "extracted_text"
OUTPUT_DIR = "processed_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_text(file_path):
    """Load text from a .txt file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def clean_text(text):
    """Basic cleanup: remove extra spaces, line breaks, and footers."""
    text = re.sub(r'\s+', ' ', text)          # collapse multiple spaces
    text = re.sub(r'Page\s*\d+', '', text)    # remove page numbers
    text = text.strip()
    return text

def split_into_sections(text):
    """
    Split IPC/CrPC text into sections based on headings like 'Section 1', 'Sec. 1', etc.
    Returns a dictionary: { 'Section 1': 'Text of Section 1 ...', ... }
    """
    # Regex patterns that match section headings
    pattern = r'(?:Section|Sec\.?)\s+(\d+[A-Z]?)'
    sections = re.split(pattern, text)
    
    structured = {}
    if len(sections) < 2:
        # If no clear section pattern, store everything as one chunk
        structured["Full_Text"] = text
        return structured

    # sections = ["", "1", "Text of Sec 1...", "2", "Text of Sec 2...", ...]
    for i in range(1, len(sections), 2):
        sec_number = sections[i]
        sec_text = sections[i+1].strip() if i+1 < len(sections) else ""
        structured[f"Section {sec_number}"] = sec_text

    return structured

def process_all_texts():
    """Convert all extracted text files into structured JSON files."""
    for filename in os.listdir(EXTRACTED_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(EXTRACTED_DIR, filename)
            base_name = filename.replace(".txt", "")
            json_path = os.path.join(OUTPUT_DIR, f"{base_name}.json")

            print(f"Processing {filename} ...")

            raw_text = load_text(file_path)
            cleaned = clean_text(raw_text)
            structured = split_into_sections(cleaned)

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(structured, f, indent=4, ensure_ascii=False)

            print(f"✅ Saved structured data to {json_path}\n")

if __name__ == "__main__":
    process_all_texts()

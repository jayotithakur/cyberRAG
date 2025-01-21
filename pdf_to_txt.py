import fitz  # PyMuPDF
import os
import re

# Set your directories
PDF_DIR = "./data/full_pdf_dataset"
OUTPUT_DATA_DIR = "./data/full_text_data/"

# Ensure output directory exists
os.makedirs(OUTPUT_DATA_DIR, exist_ok=True)

# Process each PDF file
for pdf_file in os.listdir(PDF_DIR):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        pdf_base_name = os.path.splitext(pdf_file)[0]

        # Replace invalid characters in the file name for Windows
        safe_pdf_base_name = re.sub(r'[\\/*?:"<>|]', "_", pdf_base_name)

        # Open the PDF using PyMuPDF
        doc = fitz.open(pdf_path)

        # Process each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # Page numbers are 0-indexed
            text = page.get_text("text")

            # Clean the extracted text: Remove non-ASCII characters or replace problematic characters
            text = ''.join([c if ord(c) < 128 else ' ' for c in text])  # Remove non-ASCII characters

            # Define the output file with a sanitized name
            output_file = os.path.join(OUTPUT_DATA_DIR, f"{safe_pdf_base_name}_page_{page_num + 1}.txt")

            # Write text to file with encoding handling (ignore errors)
            try:
                with open(output_file, "w", encoding="utf-8", errors="ignore") as f:
                    f.write(text)
                print(f"Outputting to: {output_file}")
            except Exception as e:
                print(f"Error writing {output_file}: {e}")

        # Close the document
        doc.close()

print("Conversion process completed!")

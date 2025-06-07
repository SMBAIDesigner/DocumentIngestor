import os
import pdfplumber
import pytesseract
from PIL import Image

def convert_pdf_to_md(pdf_path, output_dir):
    """
    Converts a PDF file to a Markdown file.

    Args:
        pdf_path (str): The path to the PDF file.
        output_dir (str): The directory to save the Markdown file.
    
    Returns:
        str: The path to the created markdown file, or None on failure.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(pdf_path)
    file_name, _ = os.path.splitext(base_name)
    md_path = os.path.join(output_dir, f"{file_name}.md")

    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\\n\\n"
                
                # Placeholder for OCR logic on images within the PDF
                # for img in page.images:
                #     # process image...
                #     pass

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(full_text)

    print(f"Successfully converted {pdf_path} to {md_path}")
    return md_path 
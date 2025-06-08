import os
import pdfplumber
import pytesseract
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def convert_pdf_to_md(pdf_path, output_dir):
    """
    Converts a single PDF file to a Markdown file.

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
                    full_text += page_text + "\n\n"
                
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

def batch_convert_pdfs(input_dir, output_dir):
    """
    Converts all PDF files in a given directory to Markdown files.

    Args:
        input_dir (str): The path to the directory containing PDF files.
        output_dir (str): The path to the directory to save Markdown files.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Input path '{input_dir}' is not a valid directory.")
        return

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in '{input_dir}'.")
        return
        
    print(f"Found {len(pdf_files)} PDF(s) to convert in '{input_dir}'.")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        convert_pdf_to_md(pdf_path, output_dir)
        
    print("\nBatch conversion complete.")

if __name__ == "__main__":
    # Get paths from environment variables
    pdf_input_directory = os.getenv('PDF_DIR')
    markdown_output_directory = os.getenv('MARKDOWN_DIR')

    if not pdf_input_directory or not markdown_output_directory:
        print("Error: Required environment variables PDF_INPUT_DIRECTORY and MARKDOWN_OUTPUT_DIRECTORY must be set")
        exit(1)

    batch_convert_pdfs(pdf_input_directory, markdown_output_directory)
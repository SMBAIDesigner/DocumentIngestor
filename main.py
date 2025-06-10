import os
import sys
import glob
import psycopg2

# Add the src directory to the Python path to allow for package imports
# This is necessary so the script can find the 'taskmaster_ai' package
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from taskmaster_ai import convert_pdf_to_md, summarize_text, vectorize_text

# --- Project Structure Configuration ---
# Define root, data, and output directories based on the script's location
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(PROJECT_ROOT, 'data', 'pdfs')
MARKDOWN_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed_markdown')
# ------------------------------------

# --- Database Configuration ---
# Replace with your actual database credentials
DB_HOST = "localhost"
DB_NAME = "pdf_documents"
DB_USER = "postgres"
DB_PASS = "password"
# -----------------------------

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        print("Please ensure PostgreSQL is running and the credentials are correct.")
        return None

def store_document_in_db(conn, filename, summary, full_text, vector):
    """Stores the processed document data into the database."""
    sql = """
    INSERT INTO documents (original_filename, summary_text, full_content, summary_vector)
    VALUES (%s, %s, %s, %s);
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (filename, summary, full_text, vector))
        conn.commit()
        print(f"Successfully stored {filename} in the database.")
    except Exception as e:
        conn.rollback()
        print(f"Error storing {filename} in database: {e}")

def process_pdf_directory(pdf_dir, markdown_dir):
    """
    Processes all PDF files in a directory, converts them, summarizes,
    vectorizes, and stores them in the database.
    """
    print(f"Starting to process PDFs in: {pdf_dir}")
    pdf_paths = glob.glob(os.path.join(pdf_dir, "*.pdf"))

    if not pdf_paths:
        print(f"No PDF files found in '{pdf_dir}'.")
        return

    db_conn = get_db_connection()
    if not db_conn:
        return

    for pdf_path in pdf_paths:
        print(f"\\n--- Processing {os.path.basename(pdf_path)} ---")
        
        md_path = convert_pdf_to_md(pdf_path, markdown_dir)
        
        if not md_path or not os.path.exists(md_path):
            print(f"Failed to create markdown for {pdf_path}")
            continue
            
        with open(md_path, "r", encoding="utf-8") as f:
            full_text = f.read()

        print("Generating summary...")
        summary = summarize_text(full_text)
        if "Error:" in summary:
            print(f"Skipping {os.path.basename(pdf_path)} due to summarization error.")
            continue
        print(f"Summary: {summary}")

        print("Generating vector embedding...")
        vector = vectorize_text(summary)
        if not vector:
            print(f"Skipping {os.path.basename(pdf_path)} due to vectorization error.")
            continue
        print("Vector generated successfully.")

        store_document_in_db(
            db_conn,
            os.path.basename(pdf_path),
            summary,
            full_text,
            vector
        )

    db_conn.close()
    print("\\n--- All PDFs processed. ---")

def setup_directories():
    """Creates necessary data directories if they don't exist."""
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(MARKDOWN_DIR, exist_ok=True)
    if not os.listdir(PDF_DIR):
         print(f"Created '{PDF_DIR}'. Please add your PDF files there.")

if __name__ == '__main__':
    setup_directories()
    process_pdf_directory(PDF_DIR, MARKDOWN_DIR) 
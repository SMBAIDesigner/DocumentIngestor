# TaskMaster-AI PDF Processing

This project provides a pipeline to process a directory of PDF files. It extracts the text, generates an AI-powered summary, converts the summary into a vector embedding, and stores all the information in a PostgreSQL database with vector support.

## Project Structure

```
my_project/
├── src/
│   └── taskmaster_ai/
│       ├── __init__.py
│       ├── ai_summarizer.py
│       ├── pdf_converter.py
│       └── text_vectorizer.py
├── scripts/
│   ├── init_db.sql
│   └── main.py
├── data/
│   ├── pdfs/           # <-- Place your PDF files here
│   └── processed_markdown/
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Setup and Usage

### 1. Prerequisites
- Python 3.8+
- PostgreSQL with the `pgvector` extension installed.
- Tesseract OCR engine (optional, for PDFs with images).

### 2. Installation

First, create and activate a virtual environment. Using `uv` is recommended:
```sh
# Create the virtual environment
uv venv

# Activate the environment (PowerShell)
.venv\Scripts\Activate.ps1
# Or (bash/zsh)
# source .venv/bin/activate
```

Install the project in editable mode. This allows you to run the scripts while also making your package importable.
```sh
uv pip install -e .
```
This will install all dependencies listed in `pyproject.toml` and `requirements.txt`.

### 3. Database Setup
1.  Ensure your PostgreSQL server is running.
2.  Create a database (e.g., `pdf_documents`).
3.  Connect to your database and run the `init_db.sql` script to create the necessary table and extension:
    ```sh
    psql -d your_db_name -U your_user_name -f scripts/init_db.sql
    ```

### 4. Configure the Pipeline
Open `scripts/main.py` and update the database connection details in the configuration section:
```python
# --- Database Configuration ---
DB_HOST = "localhost"
DB_NAME = "pdf_documents"
DB_USER = "your_user_name"
DB_PASS = "your_password"
# -----------------------------
```

### 5. Running the Pipeline
1.  Place all the PDF files you want to process into the `data/pdfs/` directory.
2.  Run the main script from the project root:
    ```sh
    python scripts/main.py
    ```

The script will iterate through the PDFs, process them, and store the results in your database.

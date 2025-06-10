# Document Ingestor

A Python-based document processing system that converts PDF documents to markdown format and provides document analysis capabilities.

## Features

- PDF to Markdown conversion
- OCR support for image-based PDFs
- Document text extraction
- Environment-based configuration

## Prerequisites

- Python 3.13 or higher
- Tesseract OCR (for OCR functionality)
- PostgreSQL (for database operations)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd DocumentIngestor
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```env
PDF_INPUT_DIRECTORY=path/to/pdf/input
MARKDOWN_OUTPUT_DIRECTORY=path/to/markdown/output
```

## Project Structure

```bash
DocumentIngestor/
├── data/ # Data directories for PDFs and markdown files
├── src/ # Source code
├── tests/ # Test files
├── scripts/ # Utility scripts
├── requirements.txt # Python dependencies
└── pyproject.toml # Project configuration
```

## Usage

### Converting PDFs to Markdown

The main functionality is provided by `src/pdf_converter.py`. To convert PDFs:

1. Place your PDF files in the input directory specified in your `.env` file
2. Run the converter:
```bash
python src/pdf_converter.py
```

The converted markdown files will be saved in the output directory specified in your `.env` file.

## Dependencies

- PyMuPDF: PDF processing
- pdfplumber: PDF text extraction
- transformers: Text processing
- sentence-transformers: Text embedding
- psycopg2-binary: PostgreSQL database adapter
- pytesseract: OCR capabilities
- Pillow: Image processing
- python-dotenv: Environment variable management

## Development

### Setting up the development environment

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your environment variables in `.env`

### Running tests

```bash
python -m pytest tests/
```
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Ensure the src directory is in the path to allow package imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from taskmaster_ai import convert_pdf_to_md

class TestPDFConverter(unittest.TestCase):

    @patch('src.taskmaster_ai.pdf_converter.pdfplumber.open')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    def test_convert_pdf_to_md_success(self, mock_makedirs, mock_os_exists, mock_file_open, mock_pdfplumber_open):
        """
        Test successful conversion of a text-based PDF to Markdown.
        """
        # Arrange: Set up the mock for pdfplumber
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "This is a line of text from the PDF."
        
        mock_pdf_instance = MagicMock()
        mock_pdf_instance.pages = [mock_page, mock_page] # Simulate a 2-page PDF
        
        mock_pdf_context_manager = MagicMock()
        mock_pdf_context_manager.__enter__.return_value = mock_pdf_instance
        mock_pdfplumber_open.return_value = mock_pdf_context_manager

        pdf_path = "/fake/dir/sample.pdf"
        output_dir = "/fake/output"

        # Act: Call the function to be tested
        result_path = convert_pdf_to_md(pdf_path, output_dir)

        # Assert: Check that the behavior was correct
        # 1. Check that pdfplumber was called with the correct path
        mock_pdfplumber_open.assert_called_once_with(pdf_path)
        
        # 2. Check that the output file was written to with the correct content
        expected_content = "This is a line of text from the PDF.\\n\\n" * 2
        mock_file_open.assert_called_once_with(os.path.join(output_dir, "sample.md"), "w", encoding="utf-8")
        mock_file_open().write.assert_called_once_with(expected_content)

        # 3. Check that the function returns the correct path
        self.assertEqual(result_path, os.path.join(output_dir, "sample.md"))

    @patch('src.taskmaster_ai.pdf_converter.pdfplumber.open', side_effect=Exception("Test PDF error"))
    def test_convert_pdf_to_md_failure(self, mock_pdfplumber_open):
        """
        Test that the function handles exceptions gracefully and returns None.
        """
        # Arrange
        pdf_path = "/fake/dir/broken.pdf"
        output_dir = "/fake/output"

        # Act
        result_path = convert_pdf_to_md(pdf_path, output_dir)

        # Assert
        # 1. Check that the error was handled
        mock_pdfplumber_open.assert_called_once_with(pdf_path)
        
        # 2. Check that the function returns None on failure
        self.assertIsNone(result_path)

if __name__ == '__main__':
    unittest.main() 
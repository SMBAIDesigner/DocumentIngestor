import os
import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from taskmaster_ai import summarize_text

class TestAISummarizer(unittest.TestCase):

    @patch('src.taskmaster_ai.ai_summarizer.pipeline')
    def test_summarize_text_success(self, mock_pipeline):
        """
        Test successful text summarization with a mocked pipeline.
        """
        # Arrange
        # Configure the mock to return a predictable summary
        mock_pipeline.return_value.return_value = [{'summary_text': 'This is a test summary.'}]
        
        input_text = "This is a long piece of text that needs to be summarized."
        expected_summary = 'This is a test summary.'
        
        # Act
        result = summarize_text(input_text)
        
        # Assert
        # 1. Check that the pipeline was called with the correct model
        mock_pipeline.assert_called_with("summarization", model="csebuetnlp/mT5-small-sum")
        
        # 2. Check that the summarizer was called with the input text
        mock_pipeline.return_value.assert_called_with(input_text, max_length=150, min_length=30, do_sample=False)
        
        # 3. Check that the result matches the expected summary
        self.assertEqual(result, expected_summary)

    @patch('src.taskmaster_ai.ai_summarizer.pipeline')
    def test_summarize_text_truncation(self, mock_pipeline):
        """
        Test that the summary is correctly truncated to the max_length.
        """
        # Arrange
        long_summary = "This is a very long summary that definitely exceeds the character limit and must be truncated."
        mock_pipeline.return_value.return_value = [{'summary_text': long_summary}]
        
        input_text = "Some input text."
        
        # Act
        # Request a max_length of 20
        result = summarize_text(input_text, max_length=20)
        
        # Assert
        self.assertEqual(result, long_summary[:20])
        self.assertEqual(len(result), 20)
        
    @patch('src.taskmaster_ai.ai_summarizer.pipeline', side_effect=Exception("Model loading failed"))
    def test_summarize_text_failure(self, mock_pipeline):
        """
        Test that the function handles exceptions and returns an error message.
        """
        # Arrange
        input_text = "Some input text."

        # Act
        result = summarize_text(input_text)

        # Assert
        self.assertEqual(result, "Error: Could not generate summary.")

if __name__ == '__main__':
    unittest.main() 
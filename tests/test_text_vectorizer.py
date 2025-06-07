import os
import unittest
from unittest.mock import patch
import numpy as np

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from taskmaster_ai import vectorize_text

class TestTextVectorizer(unittest.TestCase):

    @patch('src.taskmaster_ai.text_vectorizer.model')
    def test_vectorize_text_success(self, mock_model):
        """
        Test successful text vectorization with a mocked model.
        """
        # Arrange
        # Configure the mock model's encode method to return a numpy array
        expected_vector = np.array([0.1, 0.2, 0.3, 0.4])
        mock_model.encode.return_value = expected_vector
        
        input_text = "This is a test sentence."
        
        # Act
        result_vector = vectorize_text(input_text)
        
        # Assert
        # 1. Check that the model's encode method was called with the input text
        mock_model.encode.assert_called_once_with(input_text)
        
        # 2. Check that the result is the expected list of floats
        self.assertEqual(result_vector, expected_vector.tolist())
        self.assertIsInstance(result_vector, list)

    @patch('src.taskmaster_ai.text_vectorizer.model')
    def test_vectorize_text_failure(self, mock_model):
        """
        Test that the function handles exceptions and returns None.
        """
        # Arrange
        # Configure the mock to raise an exception when called
        mock_model.encode.side_effect = Exception("Encoding failed")
        
        input_text = "This will fail."
        
        # Act
        result_vector = vectorize_text(input_text)
        
        # Assert
        self.assertIsNone(result_vector)

if __name__ == '__main__':
    unittest.main() 
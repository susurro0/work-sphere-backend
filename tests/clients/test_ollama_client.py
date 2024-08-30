import unittest
from unittest.mock import patch, MagicMock

from app.clients.OllamaClient import OllamaClient


class TestOllamaClient(unittest.TestCase):

    @patch('app.clients.OllamaClient.ollama.Client')  # Mock the ollama.Client class
    def test_generate_text(self, MockClient):
        # Arrange
        mock_client_instance = MockClient.return_value
        mock_client_instance.chat.return_value = {
            'message': {'content': 'Default parameter response'}
        }

        client = OllamaClient(host="http://mocked-host")
        combined_prompt = "Test prompt"

        # Act
        result = client.generate_text(combined_prompt)

        # Assert
        mock_client_instance.chat.assert_called_once_with(model='llama3.1', messages=[
            {'role': 'user', 'content': combined_prompt},
        ])
        self.assertEqual(result, 'Default parameter response')

    @patch('app.clients.OllamaClient.ollama.Client')  # Replace with actual module path
    def test_generate_text_error_handling(self, MockClient):
        # Arrange
        mock_instance = MockClient.return_value
        mock_instance.chat.side_effect = Exception("Mocked exception")
        combined_prompt = "Test prompt"

        client = OllamaClient(host="http://mocked-host")

        # Act
        result = client.generate_text(combined_prompt)

        # Assert
        self.assertEqual(result, "")

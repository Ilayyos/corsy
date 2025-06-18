import unittest
from unittest.mock import patch

from core.utils import extractHeaders


class TestExtractHeaders(unittest.TestCase):
    def test_valid_headers(self):
        headers = "User-Agent: UA\nAccept: text/html\n"
        expected = {"User-Agent": "UA", "Accept": "text/html"}
        self.assertEqual(extractHeaders(headers), expected)

    def test_ignores_blank_and_missing_colon(self):
        headers = "User-Agent: UA\n\nInvalidLine\nAccept: text/html"
        expected = {"User-Agent": "UA", "Accept": "text/html"}
        self.assertEqual(extractHeaders(headers), expected)

    def test_warning_on_malformed(self):
        headers = "Header: value\nMalformed"
        with patch('builtins.print') as mock_print:
            result = extractHeaders(headers, warn=True)
            self.assertEqual(result, {"Header": "value"})
            mock_print.assert_called_once()
            self.assertIn('Malformed', mock_print.call_args[0][0])


if __name__ == '__main__':
    unittest.main()

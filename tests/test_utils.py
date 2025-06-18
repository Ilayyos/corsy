import unittest
from core.utils import extractHeaders

class ExtractHeadersTests(unittest.TestCase):
    def test_ignore_lines_without_colon_newline(self):
        header_str = 'User-Agent: test\nBadLine\nAccept: */*'
        result = extractHeaders(header_str)
        self.assertEqual(result.get('User-Agent'), 'test')
        self.assertEqual(result.get('Accept'), '*/*')
        self.assertNotIn('BadLine', result)

    def test_ignore_lines_without_colon_escaped(self):
        header_str = 'User-Agent: test\\nBadLine\\nAccept: */*'
        result = extractHeaders(header_str)
        self.assertEqual(result.get('User-Agent'), 'test')
        self.assertEqual(result.get('Accept'), '*/*')
        self.assertNotIn('BadLine', result)

if __name__ == '__main__':
    unittest.main()

import unittest
from extract_title import *


class TestExtractTitle(unittest.TestCase):
    def test_valid_header(self):
        md = " # My Page "
        header = extract_title(md)
        self.assertEqual(header, "My Page")
    
    
    def test_valid_header_with_more_lines(self):
        md = """
        some text that should be ignored
        
        #     My Page
        some other text
        
        ## maybe another heading
        """
        header = extract_title(md)
        self.assertEqual(header, "My Page")
    
    
    def test_invalid_header(self):
        md = " ## My Page "
        self.assertRaises(Exception, lambda: extract_title(md))



if __name__ == "__main__":
    unittest.main()
import unittest
from block_markdown import *
from blocknode import *



class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



class TestBlockType(unittest.TestCase):
    def test_heading(self):
        md_block = markdown_to_blocks("""
## This is a heading of level 2
""")
        result = block_to_block_type(md_block[0])
        self.assertEqual(result, BlockType.HEADING)
    
    
    def test_code(self):
        md_block = markdown_to_blocks("""
```
def func(value):
    print(value)
```
""")
        result = block_to_block_type(md_block[0])
        self.assertEqual(result, BlockType.CODE)
    
    
    def test_quote(self):
        md_block = markdown_to_blocks("""
> Writing Tests is a huge Pain.
> Seriously....
""")
        result = block_to_block_type(md_block[0])
        self.assertEqual(result, BlockType.QUOTE)
    
    
    def test_ulist(self):
        md_block = markdown_to_blocks("""
- writing Code
- Wrting UnitTests
""")
        result = block_to_block_type(md_block[0])
        self.assertEqual(result, BlockType.ULIST)
    
    
    def test_olist(self):
        md_block = markdown_to_blocks("""
1. Wake up
2. Get ready
3. Go to work
""")
        result = block_to_block_type(md_block[0])
        self.assertEqual(result, BlockType.OLIST)
    
    def test_paragraph(self):
        md_block = markdown_to_blocks("""
#This should be a paragraph
""")
        result = block_to_block_type(md_block[0])
        self.assertEqual(result, BlockType.PARAGRAPH)
    
        
        

if __name__ == "__main__":
    unittest.main()
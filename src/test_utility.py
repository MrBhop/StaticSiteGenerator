import unittest
from utility import *
from textnode import TextNode, TextType

class TestUtility(unittest.TestCase):
    def test_split_md_delimiter(self):
        md = [TextNode('This is a text with **bold** text.', TextType.TEXT)]
        result = [TextNode('This is a text with ', TextType.TEXT), TextNode('bold', TextType.BOLD), TextNode(' text.', TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(md, "**", TextType.BOLD), result)

    def test_split_md_delimiter_multi_replace(self):
        md = [TextNode('**This** is some text. **I** want multiple instances to be replaced here.', TextType.TEXT)]
        result = [
            TextNode('This', TextType.BOLD),
            TextNode(' is some text. ', TextType.TEXT),
            TextNode('I', TextType.BOLD),
            TextNode(' want multiple instances to be replaced here.', TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(md, "**", TextType.BOLD), result)
    
    def test_split_md_delimiter_invalid_md(self):
        md = [TextNode("This is some **invalid markdown", TextType.TEXT)]

        self.assertRaises(Exception, lambda: split_nodes_delimiter(md, "**", TextType.BOLD))
    
    def test_split_md_delimiter_multiple_nodes(self):
        md = [
            TextNode("This is some bold text.", TextType.BOLD),
            TextNode("I am _always_ writing the same text in these.", TextType.TEXT)
        ]
        result = [
            TextNode('This is some bold text.', TextType.BOLD),
            TextNode('I am ', TextType.TEXT),
            TextNode('always', TextType.ITALIC),
            TextNode(' writing the same text in these.', TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(md, "_", TextType.ITALIC), result)
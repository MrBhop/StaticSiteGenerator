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


    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_no_value(self):
        matches = extract_markdown_images("This is a [link](youtube.com) to nothing.")
        self.assertEqual([], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is a [link](youtube.com) to nothing.")
        self.assertEqual([("link", "youtube.com")], matches)
    
    def test_extract_markdown_links_no_value(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)
    

    def test_extract_image(self):
        node = [TextNode("This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        result = [
            TextNode('This is a text with an ', TextType.TEXT),
            TextNode('image', TextType.IMAGE, 'https://i.imgur.com/zjjcJKZ.png'),
            TextNode(' and another ', TextType.TEXT),
            TextNode('second image', TextType.IMAGE, 'https://i.imgur.com/3elNhQu.png')
        ]
        self.assertEqual(split_nodes_image(node), result)
    
    def test_extract_image_no_match(self):
        node = [TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        result = [TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        self.assertEqual(split_nodes_image(node), result)
    
    def test_extract_image_only_image(self):
        node = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        result = [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(split_nodes_image(node), result)
    

    def test_extract_link(self):
        node = [TextNode("This is a text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        result = [
            TextNode('This is a text with a ', TextType.TEXT),
            TextNode('link', TextType.LINK, 'https://i.imgur.com/zjjcJKZ.png'),
            TextNode(' and another ', TextType.TEXT),
            TextNode('link', TextType.LINK, 'https://i.imgur.com/3elNhQu.png')
        ]
        self.assertEqual(split_nodes_link(node), result)
    
    def test_extract_link_no_match(self):
        node = [TextNode("This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        result = [TextNode("This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        self.assertEqual(split_nodes_link(node), result)
    
    def test_extract_link_only_link(self):
        node = [TextNode("[link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        result = [TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(split_nodes_link(node), result)
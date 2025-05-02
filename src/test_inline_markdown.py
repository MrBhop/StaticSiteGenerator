import unittest
from inline_markdown import *
from textnode import TextNode, TextType
import re



class TestSplitInlineMarkdownText(unittest.TestCase):
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



class TestCompareRegexIterator(unittest.TestCase):
    def test_correct_match(self):
        pattern = r"\b\w+?\b"
        test_string = "This is 1 string."
        result = get_iterator_and_count(pattern, test_string)
        expected = [("This",), ("is",), ("1",), ("string",)]
        self.assertTrue(compare_regex_iterator(result, expected))
    
    
    def test_incorrect_mach(self):
        pattern = r"\d+?"
        test_string = "This is a string."
        result = get_iterator_and_count(pattern, test_string)
        expected = ["a match"]
        self.assertFalse(compare_regex_iterator(result, expected))
    
    
    def test_match_with_groups_correct(self):
        pattern = r"\{(\d+?):(\d+?)\}"
        test_string = "{1:2} (3:4) [5:6]"
        result = get_iterator_and_count(pattern, test_string)
        expected = [("1", "2")]
        self.assertTrue(compare_regex_iterator(result, expected))
    
    
    def test_match_with_groups_incorrect(self):
        pattern = r"\{(\d+?):(\d+?)\}"
        test_string = "{1:2} (3:4) [5:6]"
        result = get_iterator_and_count(pattern, test_string)
        expected = [("1", "3")]
        self.assertFalse(compare_regex_iterator(result, expected))



class TestSplitInlineMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        result = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertTrue(compare_regex_iterator(result, expected))
    

    def test_extract_markdown_images_no_match(self):
        result = extract_markdown_images("This is a [link](youtube.com) to nothing.")
        expected = []
        self.assertTrue(compare_regex_iterator(result, expected))
    

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
    

    def test_extract_image_whole_string_matches(self):
        node = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        result = [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(split_nodes_image(node), result)
    
    
    def test_extract_image_same_content_twice(self):
        input = [TextNode("![image](https://i.imgur.com/zjjcJKZ.png): An Image, idk. ![image](https://i.imgur.com/zjjcJKZ.png): not the same ;)", TextType.TEXT)]
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(": An Image, idk. ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(": not the same ;)", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_image(input), expected)
    
    
    
class TestSplitInlineMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        result = extract_markdown_links("This is a [link](youtube.com) to nothing.")
        expected = [("link", "youtube.com")]
        self.assertTrue(compare_regex_iterator(result, expected))
    

    def test_extract_markdown_links_no_match(self):
        result = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        expected = []
        self.assertTrue(compare_regex_iterator(result, expected))
    

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
    
    
    def test_extract_link_whole_string_matches(self):
        node = [TextNode("[link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        result = [TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(split_nodes_link(node), result)
    
    
    def test_extract_link_same_content_twice(self):
        input = [TextNode("[youtube](https://youtube.com): Youtube. [youtube](https://youtube.com): not youtube ;)", TextType.TEXT)]
        expected = [
            TextNode("youtube", TextType.LINK, "https://youtube.com"),
            TextNode(": Youtube. ", TextType.TEXT),
            TextNode("youtube", TextType.LINK, "https://youtube.com"),
            TextNode(": not youtube ;)", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link(input), expected)



# utility functions:
def compare_regex_iterator(input, expected_list):
    iterotor, match_count = input
    
    if match_count != len(expected_list):
        return False
    
    for item in expected_list:
        if not isinstance(item, tuple):
            raise ValueError("expected_list must be a list of tuples")
        
        result = next(iterotor, None)
        
        if len(item) == 1:
            if item[0] != result.group(0):
                return False
        else:
            for i in range(0, len(item)):
                if item[i] != result.group(i + 1):
                    return False

    return True
        


if __name__ == "__main__":
    unittest.main()
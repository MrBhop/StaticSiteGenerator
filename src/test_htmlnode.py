import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html = HTMLNode(props={"href":"youtube.com", "class":"link"})
        result = ' href="youtube.com" class="link"'
        self.assertEqual(html.props_to_html(), result)
    
    def test_props_to_html_empty(self):
        html = HTMLNode()
        result = ""
        self.assertEqual(html.props_to_html(), result)
    
    def test_props_to_html2(self):
        html = HTMLNode(props={"type":"input", "name":"first-name", "id":"first-name", "placeholder":"First Name"})
        result= ' type="input" name="first-name" id="first-name" placeholder="First Name"'
        self.assertEqual(html.props_to_html(), result)



if __name__ == "__main__":
    unittest.main()
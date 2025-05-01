import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        result = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), result)
    
    def test_parent_to_html(self):
        node = ParentNode(
            "p", 
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        result = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), result)
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
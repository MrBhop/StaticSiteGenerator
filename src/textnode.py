from enum import Enum
from htmlnode import LeafNode



class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "img"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    

    def __eq__(self, value):
        if self.text != value.text:
            return False
        
        if self.text_type != value.text_type:
            return False
        
        if self.url != value.url:
            return False
        
        return True

    
    def to_html_node(self):
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href":self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src":self.url, "alt":self.text})
            case _:
                raise Exception("Text node has unsupported text_type")


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def text_node_to_html_node(text_node):
    return text_node.to_html_node()
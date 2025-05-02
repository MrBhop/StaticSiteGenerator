from enum import Enum
from htmlnode import LeafNode



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "CODE"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"



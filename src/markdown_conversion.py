from htmlnode import *
from inline_markdown import *
from blocknode import *
from textnode import *


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in markdown_blocks:
        children.append(BlockNode(block).to_html_node())
    
    return ParentNode("div", children)
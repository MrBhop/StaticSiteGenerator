import re
from enum import Enum
from htmlnode import LeafNode
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_text_node
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    CODE_CHILD = "code child"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"
    LISTITEM = "list item"


class BlockNode:
    def __init__(self, markdown_block, block_type=None):
        if block_type == None:
            block_type, heading_level = block_to_block_type(markdown_block)
            markdown_block = remove_markdown_tags(markdown_block, block_type)
        else:
            heading_level = None
            
        self.__html_tag = block_type_to_html_tag(block_type, heading_level)
        
        match block_type:
            case BlockType.CODE:
                self.children = [BlockNode(markdown_block, BlockType.CODE_CHILD)]
            case BlockType.CODE_CHILD:
                self.children = [TextNode(markdown_block, TextType.TEXT)]
            case BlockType.ULIST | BlockType.OLIST:
                self.children = list(map(lambda line: BlockNode(line, BlockType.LISTITEM), markdown_block.split("\n")))
            case _:
                self.children = text_to_text_node(markdown_block)
    
    
    def to_html_node(self):
        return ParentNode(self.__html_tag, self.__children_to_html_node())
    
    
    def __children_to_html_node(self):
        return list(map(lambda node: node.to_html_node(), self.children))


    def __repr__(self):
        return f"BlockNode({self.__html_tag(), self.markdown})"


def block_node_to_html_node(block_node):
    return block_node.to_html_node()


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = map(lambda block: block.strip(), blocks)
    return list(filter(lambda block: len(block) > 0, stripped_blocks))


def block_to_block_type(markdown_block):
    heading_match = re.match(r"\s*?(#{1,6})\s+?\w", markdown_block)
    if heading_match != None:
        heading_level = len(heading_match.group(1))
        return BlockType.HEADING, heading_level
    elif markdown_block[:3] == "```" and markdown_block[-3:] == "```":
        return BlockType.CODE, None
    elif regex_matches_every_line_of_markdown_block(r"\s*?>", markdown_block):
        return BlockType.QUOTE, None
    elif regex_matches_every_line_of_markdown_block(r"\s*?-\s", markdown_block):
        return BlockType.ULIST, None
    elif markdown_block_is_ordered_list(markdown_block):
        return BlockType.OLIST, None
    else:
        return BlockType.PARAGRAPH, None


def regex_matches_every_line_of_markdown_block(pattern, markdown_block):
    for line in markdown_block.split("\n"):
        if re.match(pattern, line) == None:
            return False
    
    return True


def markdown_block_is_ordered_list(markdown_block):
    i = 0
    for line in markdown_block.split("\n"):
        i += 1
        
        if re.match(r"\s*?" + str(i) + r"\.\s", line) == None:
            return False
    
    return True


def block_type_to_html_tag(block_type, heading_level):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return f"h{heading_level}"
        case BlockType.CODE:
            return "pre"
        case BlockType.CODE_CHILD:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.ULIST:
            return "ul"
        case BlockType.OLIST:
            return "ol"
        case BlockType.LISTITEM:
            return "li"
        case _:
            raise Exception("Block node has unsupported block_type")


def remove_markdown_tags(markdown, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            output = markdown
            output = remove_line_breaks(output)
        case BlockType.HEADING:
            output = remove_regex_pattern(r"(?<!\n)^\s*?(#){1,6}\s+?", markdown)
        case BlockType.CODE:
            output = remove_regex_pattern(r"(^(?<!\n)```\n|```$(?!\n))", markdown)
        case BlockType.QUOTE:
            output = remove_regex_pattern(r"^\s*?>\s+?", markdown)
            output = remove_line_breaks(output)
        case BlockType.ULIST:
            output = remove_regex_pattern(r"^\s*?-\s+?", markdown)
        case BlockType.OLIST:
            output = remove_regex_pattern(r"^\s*?\d+?\.\s+?", markdown)
        case _:
            raise Exception("Block node has unsupported block_type")
    
    return output


def remove_regex_pattern(pattern, text):
    return re.sub(pattern, "", text, flags=re.MULTILINE)

def remove_line_breaks(text):
    return text.replace("\n", " ")
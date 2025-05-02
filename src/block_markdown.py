from blocknode import BlockType
import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = map(lambda block: block.strip(), blocks)
    return list(filter(lambda block: len(block) > 0, stripped_blocks))


def block_to_block_type(markdown_block):
    if re.match(r"\s*?#{1,6}\s+?\w", markdown_block) != None:
        return BlockType.HEADING
    elif markdown_block[:3] == "```" and markdown_block[-3:] == "```":
        return BlockType.CODE
    elif regex_matches_every_line_of_markdown_block(r"\s*?>", markdown_block):
        return BlockType.QUOTE
    elif regex_matches_every_line_of_markdown_block(r"\s*?-\s", markdown_block):
        return BlockType.ULIST
    elif markdown_block_is_ordered_list(markdown_block):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH


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
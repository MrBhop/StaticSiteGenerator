from textnode import TextNode, TextType
import re



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        sections = node_text.split(delimiter)

        if len(sections) % 2 == 0:
            raise Exception(f"missing: closing {delimiter} in '{node_text}'")

        for i in range(0, len(sections)):
            current_text = sections[i]

            if current_text == "":
                continue
                
            if i % 2 == 0:
                type = node.text_type
            else:
                type = text_type
            
            new_nodes.append(TextNode(current_text, type))

    return new_nodes


def get_iterator_and_count(pattern, text):
    return re.finditer(pattern, text), len(re.findall(pattern, text))

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return get_iterator_and_count(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return get_iterator_and_count(pattern, text)


def split_nodes_image(old_nodes):
    return __split_nodes_with_function(old_nodes, extract_markdown_images, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return __split_nodes_with_function(old_nodes, extract_markdown_links, TextType.LINK)


def __split_nodes_with_function(old_nodes, extractor_function, text_type):
    new_nodes = []

    for node in old_nodes:
        image_matches, match_count = extractor_function(node.text)

        if node.text_type != TextType.TEXT or match_count == 0:
            new_nodes.append(node)
            continue
        
        if node.text == "":
            continue
        
        i = -1
        for match in image_matches:
            i += 1

            # first iteration.
            if i == 0:
                # check if the match is the start of the string.
                if match.start(0) != 0:
                    new_nodes.append(TextNode(node.text[:match.start(0)], TextType.TEXT))
            else:
                new_nodes.append(TextNode(node.text[last_match.end(0):match.start(0)], TextType.TEXT))
            
            new_nodes.append(TextNode(match.group(1), text_type, match.group(2)))

            # last iteration.
            if i == match_count - 1:
                # check if the match end before the end of the string.
                if match.end(0) < len(node.text):
                    new_nodes.append(TextNode(node.text[match.end(0):], TextType.TEXT))
            
            # store match for next iteration.
            last_match = match
    
    return new_nodes


def text_to_text_node(text):
    original_node = TextNode(text, TextType.TEXT)
    
    with_links = split_nodes_link([original_node])
    with_images = split_nodes_image(with_links)
    with_code = split_nodes_delimiter(with_images, "`", TextType.CODE)
    with_bold = split_nodes_delimiter(with_code, "**", TextType.BOLD)
    with_italic = split_nodes_delimiter(with_bold, "_", TextType.ITALIC)
    
    return with_italic
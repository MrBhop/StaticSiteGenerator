from textnode import TextNode, TextType

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
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = map(lambda block: block.strip(), blocks)
    return list(filter(lambda block: len(block) > 0, stripped_blocks))
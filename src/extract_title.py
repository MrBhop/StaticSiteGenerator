import re


def extract_title(markdown):
    title_match = re.search(r"^\s*?#\s+?(.*?)(\n|$)", markdown, flags=re.MULTILINE)
    
    if title_match == None:
        raise ValueError("markdown does not contain a level 1 heading")

    return title_match.group(1).strip()
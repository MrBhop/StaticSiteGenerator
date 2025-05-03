from markdown_conversion import markdown_to_html_node
from extract_title import extract_title
import os
import re


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")
    
    md_file = open(from_path)
    markdown = md_file.read()
    md_file.close()
    
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()
    
    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    new_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    
    dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    output_file = open(dest_path, "w")
    output_file.write(new_html)
    output_file.close()


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        current_source = os.path.join(dir_path_content, item)
        current_destination = os.path.join(dest_dir_path, item)
        
        if os.path.isdir(current_source):
            generate_page_recursive(current_source, template_path, current_destination)
        else:
            generate_page(current_source, template_path, replace_file_extension(current_destination, "html"))


def replace_file_extension(file_name, new_extension):
    if "." not in file_name:
        return f"{file_name}.{new_extension}"
    return re.sub(r"(?<=\.)\w+?$", new_extension, file_name)
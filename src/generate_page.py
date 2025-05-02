from markdown_conversion import markdown_to_html_node
from extract_title import extract_title
import os


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
        os.mkdirs(dir_path)
    
    output_file = open(dest_path, "w")
    output_file.write(new_html)
    output_file.close()
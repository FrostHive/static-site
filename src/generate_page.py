import os
from markdown_to_html import extract_title, markdown_to_html_node

def generate_page(from_path: str, template_path, dest_path: str, base_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_text = ""
    template_text = ""

    with open(from_path, 'r') as markdown_file:
        markdown_text = markdown_file.read()

    with open(template_path, 'r') as template_file:
        template_text = template_file.read()

    html_title = extract_title(markdown_text)

    converted_node = markdown_to_html_node(markdown_text)
    converted_text = converted_node.to_html()

    complete_text = template_text.replace("{{ Title }}", html_title).replace("{{ Content }}", converted_text)

    complete_text = complete_text.replace("href=\"/", f"href=\"/{base_path}").replace("src=\"/", f"src=\"/{base_path}")
    full_path = os.path.abspath(dest_path)
    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path))

    print (f"Opening {full_path} to write in.")
    with open(full_path, 'w') as final_file:
        final_file.write(complete_text)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str):
    for item in os.listdir(dir_path_content):
        original_path = os.path.join(dir_path_content, item)
        new_destination = os.path.join(dest_dir_path, f"{item[:-2]}html")
        if os.path.isfile(original_path) and item.endswith(".md"):
            print(f"Found file: {item}")
            generate_page(original_path, template_path, new_destination, base_path)
        if os.path.isdir(original_path):
            print(f"Found directory: {item}")
            generate_pages_recursive(original_path, template_path, os.path.join(dest_dir_path, item), base_path)

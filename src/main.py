import os
import shutil
from md_to_html import markdown_to_html_node

def have_heading(md):
    lines = md.split('\n')
    for line in lines:
        if line.startswith('# '):
            return True
    return False

def extract_title(markdown):
    if not have_heading(markdown):
        raise ValueError("Markdown must include a heading for a title.")

    lines = markdown.split("\n")
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return 'No Title'

def generate_page(from_path, template_path, dest_path):
    with open(from_path, 'r') as markdown_file:
        md_content = markdown_file.read()

    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    html_node = markdown_to_html_node(md_content)
    html_content = html_node.to_html()  # assuming html_node is an instance of HTMLNode

    title = extract_title(md_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as output_file:
        output_file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        if os.path.isdir(from_path):
            new_dest_path = os.path.join(dest_dir_path, item)
            os.makedirs(new_dest_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, new_dest_path)
        elif from_path.endswith('.md'):
            dest_file = os.path.splitext(item)[0] + '.html'
            dest_path = os.path.join(dest_dir_path, dest_file)
            generate_page(from_path, template_path, dest_path)


def copy_directory_contents(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            copy_directory_contents(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)

def copy_static(static_directory, public_directory):
    if os.path.exists(public_directory):
        shutil.rmtree(public_directory)
    copy_directory_contents(static_directory, public_directory)

def main():
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_directory = os.path.dirname(current_script_dir)
    public_directory = os.path.join(project_directory, 'public')
    static_directory = os.path.join(project_directory, 'static')
    content_directory = os.path.join(project_directory, 'content')
    template_path = os.path.join(project_directory, 'template.html')

    copy_static(static_directory, public_directory)
    generate_pages_recursive(content_directory, template_path, public_directory)

if __name__ == "__main__":
    main()

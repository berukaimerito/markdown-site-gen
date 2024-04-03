import os
import shutil
from md_to_html import markdown_to_html_node



def have_heading(md):
    lines = md.split('\n')
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line.lstrip().startswith('# ') or stripped_line[1:].strip():
            return True
    return False


def extract_title(markdown):
    if have_heading(markdown) == False:
        raise ValueError("Markdown must include a heading. All pages need h1 header.")

    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line.startswith('# '):
            return stripped_line[1:].strip()
    return 'Unknown Heading'


def generate_page(from_path, template_path, dest_path):

    # Read the markdown file at from_path and store the contents in a variable.
    with open(from_path, 'r') as markdown_file:
        md_content = markdown_file.read()

    # Read the template file at template_path and store the contents in a variable.
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    # Use your markdown_to_html_node function and .to_html() method to convert the markdown file to HTML.
    html_node = markdown_to_html_node(md_content)
    html_content = html_node.to_html()  # assuming html_node is an instance of HTMLNode

    # Use the extract_title function to grab the title of the page.
    title = extract_title(md_content)

    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    template_content  = template_content.replace("{{ Title }}", title)
    template_content =  template_content.replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as output_file:
        output_file.write(template_content)





def copy_directory_contents(src, dest):
    """
    Recursively copy all files and directories from src to dest.
    """
    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        # Recursively copy directories
        if os.path.isdir(src_path):
            copy_directory_contents(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)
            print(f"Copied {src_path} to {dest_path}")


def copy_static():
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_directory = os.path.dirname(current_script_dir)
    public_directory = os.path.join(project_directory, 'public')
    static_directory = os.path.join(project_directory, 'static')
    print(f"Project directory: {project_directory}")
    print(f"Static directory: {static_directory}")
    print(f"Public directory: {public_directory}")

    # Ensure the public directory is cleared before copying
    if os.path.exists(public_directory):
        shutil.rmtree(public_directory)
    os.makedirs(public_directory)
    copy_directory_contents(static_directory, public_directory)

def main():
    # First, copy static files
    copy_static()
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()

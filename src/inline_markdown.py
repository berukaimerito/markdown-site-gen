import re

from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_image, text_type_link

def extract_markdown_images(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    print(f"Extracting Images: Found {len(matches)} images")
    return matches

def extract_markdown_links(text):
    pattern = r'\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    print(f"Extracting Links: Found {len(matches)} links")
    return matches

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    print(f"Processing split_nodes_delimiter for delimiter: {delimiter} and text_type: {text_type}")
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        parts = re.split(f'\\{delimiter}(.*?)\\{delimiter}', node.text, flags=re.DOTALL)
        toggle = False
        for part in parts:
            if toggle:
                new_nodes.append(TextNode(part, text_type))
            else:
                if part:  # avoid adding empty strings
                    new_nodes.append(TextNode(part, text_type_text))
            toggle = not toggle
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    print("Processing split_nodes_image")
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
        else:
            last_idx = 0
            for alt, src in images:
                image_markdown = f"![{alt}]({src})"
                start_pos, end_pos = node.text.find(image_markdown, last_idx), last_idx + len(image_markdown)
                if start_pos > last_idx:
                    new_nodes.append(TextNode(node.text[last_idx:start_pos], text_type_text))
                new_nodes.append(TextNode(alt, text_type_image, src))
                last_idx = end_pos
            if last_idx < len(node.text):
                new_nodes.append(TextNode(node.text[last_idx:], text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    print("Processing split_nodes_link")
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
        else:
            last_idx = 0
            for text, url in links:
                link_markdown = f"[{text}]({url})"
                start_pos, end_pos = node.text.find(link_markdown, last_idx), last_idx + len(link_markdown)
                if start_pos > last_idx:
                    new_nodes.append(TextNode(node.text[last_idx:start_pos], text_type_text))
                new_nodes.append(TextNode(text, text_type_link, url))
                last_idx = end_pos
            if last_idx < len(node.text):
                new_nodes.append(TextNode(node.text[last_idx:], text_type_text))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    print("Final nodes after processing:", nodes)
    return nodes

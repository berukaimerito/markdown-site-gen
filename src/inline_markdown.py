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
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        # Escape special regex characters in the delimiter
        escaped_delimiter = re.escape(delimiter)
        # Use the escaped delimiter in the regex pattern
        parts = re.split(f'({escaped_delimiter}.*?{escaped_delimiter})', old_node.text)
        for part in parts:
            if part.startswith(delimiter) and part.endswith(delimiter):
                new_nodes.append(TextNode(part[len(delimiter):-len(delimiter)], text_type))
            else:
                new_nodes.append(TextNode(part, text_type_text))
    return new_nodes


def split_nodes_image(old_nodes):
        new_nodes = []
        for node in old_nodes:
            if node.text_type != text_type_text:
                new_nodes.append(node)
                continue

            parts = node.text.split('![')
            new_nodes.append(TextNode(parts[0], text_type_text))
            for part in parts[1:]:
                if '](' in part:
                    alt_text, rest = part.split('](', 1)
                    url, rest = rest.split(')', 1)
                    new_nodes.append(TextNode(alt_text, text_type_image, url))
                    new_nodes.append(TextNode(rest, text_type_text))
                else:
                    # This handles the case where there is no valid image markdown after '![...'
                    new_nodes.append(TextNode('![' + part, text_type_text))

        return new_nodes

def split_nodes_link(old_nodes):
        new_nodes = []
        for node in old_nodes:
            if node.text_type != text_type_text:
                new_nodes.append(node)
                continue

            parts = node.text.split('[')
            new_nodes.append(TextNode(parts[0], text_type_text))
            for part in parts[1:]:
                if '](' in part:
                    link_text, rest = part.split('](', 1)
                    url, rest = rest.split(')', 1)
                    new_nodes.append(TextNode(link_text, text_type_link, url))
                    new_nodes.append(TextNode(rest, text_type_text))
                else:
                    # This handles the case where there is no valid link markdown after '[...'
                    new_nodes.append(TextNode('[' + part, text_type_text))

        return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    return nodes

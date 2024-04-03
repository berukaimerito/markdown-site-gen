from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import  text_node_to_html_node
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_paragraph,
    block_type_ordered_list,
    block_type_unordered_list,
    block_type_quote
)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(node) for node in text_nodes]
    return children



def quote_block_to_html(block):
    children = text_to_children(block.replace('> ', ''))
    return ParentNode("blockquote", children)

def unordered_list_to_html(block):
    items = block.split('\n')
    list_items = [ParentNode("li", text_to_children(item.strip('- *'))) for item in items]
    return ParentNode("ul", list_items)

def ordered_list_to_html(block):
    items = block.split('\n')
    list_items = [ParentNode("li", text_to_children(item[item.index('.')+2:])) for item in items]
    return ParentNode("ol", list_items)

def code_block_to_html(block):
    code_content = '\n'.join(block.split('\n')[1:-1])
    return ParentNode("pre", [LeafNode("code", code_content)])

def heading_to_html(block):
    level = min(block.count('#'), 6)
    text = block.strip("# ")
    return ParentNode(f"h{level}", text_to_children(text))

def paragraph_to_html(block):
    return ParentNode("p", text_to_children(block))

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_quote:
            html_blocks.append(quote_block_to_html(block))
        elif block_type == block_type_unordered_list:
            html_blocks.append(unordered_list_to_html(block))
        elif block_type == block_type_ordered_list:
            html_blocks.append(ordered_list_to_html(block))
        elif block_type == block_type_code:
            html_blocks.append(code_block_to_html(block))
        elif block_type == block_type_heading:
            html_blocks.append(heading_to_html(block))
        elif block_type == block_type_paragraph:
            html_blocks.append(paragraph_to_html(block))
        else:
            raise ValueError(f"Unhandled block type: {block_type}")
    return ParentNode("div", html_blocks)

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = [markdown_to_html_node(block) for block in blocks]
    html_output = "".join(node.to_html() for node in block_nodes)
    return html_output

# Add your HTMLNode and TextNode implementation details as needed.

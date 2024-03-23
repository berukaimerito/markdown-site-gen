from sys import _current_frames
from textnode import TextNode

def strip_delimiters(node_text, delimiter):
    if node_text.startswith(delimiter) and node_text.endswith(delimiter):
        return node_text[len(delimiter):-len(delimiter)]
    return node_text

# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     valid_nodes = {
#         "text_type_text": "text",
#         "text_type_code": "code",
#         "text_type_italic": "italic",
#         "text_type_bold": "bold"
#     }
#     if not delimiter:
#         raise ValueError("Invalid delimeter.")

#     values = old_nodes.text.split(" ")
#     nodes = []
#     inside_delimiter = False
#     current_text = []

#     for i,v in enumerate(values):
#         if v.startswith(delimiter) or inside_delimiter:
#             if v.endswith(delimiter):
#                 inside_delimiter = False
#                 current_text.append(v)
#                 deli_node = " ".join(node for node in current_text)
#                 nodes.append(deli_node)
#                 current_text = []
#             else:
#                 inside_delimiter = True
#                 current_text.append(v)
#         else:
#             nodes.append(v)

#     final_nodes = []
#     text_node = ""

#     for node_text in nodes:
#         if delimiter in node_text:
#         # If there's accumulated text, create a TextNode for it first
#             if text_node:
#                 final_nodes.append(TextNode(text_node.strip(), "text"))
#                 text_node = ""  # Reset the accumulator
#             clean_text = strip_delimiters(node_text, delimiter)
#             final_nodes.append(TextNode(clean_text, text_type))
#         else:
#             text_node += node_text + " "

#     # After the loop, check if there's any remaining text to be added as a TextNode
#     if text_node:
#         final_nodes.append(TextNode(text_node.strip(), "text"))

#     print(final_nodes)
#     return final_nodes
# def split_nodes_delimiter(text, delimiter, text_type):
#     parts = text.split(delimiter)
#     nodes = []
#     inside_delimiter = False

#     for part in parts:
#         # Toggle the inside_delimiter flag to know when you're entering or exiting a bold text segment
#         if inside_delimiter:
#             # The part is bold text
#             nodes.append(TextNode(part, text_type))
#         else:
#             # The part is regular text
#             # Ensure leading and trailing spaces are preserved by checking if the part is non-empty
#             if part:
#                 nodes.append(TextNode(part, "text"))
#         inside_delimiter = not inside_delimiter

#     print(nodes)
#     return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Check if the node is of type 'text' and requires processing
        if node.text_type == "text":
            start = 0  # Start index of the current segment
            while start < len(node.text):
                # Find the next occurrence of the delimiter
                open_delim = node.text.find(delimiter, start)
                if open_delim == -1:  # No more delimiters found
                    new_nodes.append(TextNode(node.text[start:], "text", node.url))
                    break

                # Add text before the delimiter as a 'text' node
                if open_delim > start:
                    new_nodes.append(TextNode(node.text[start:open_delim], "text", node.url))

                # Find the closing delimiter
                close_delim = node.text.find(delimiter, open_delim + len(delimiter))
                if close_delim == -1:  # No closing delimiter found
                    # Treat the rest of the text as regular text if no closing delimiter is found
                    new_nodes.append(TextNode(node.text[open_delim:], "text", node.url))
                    break
                else:
                    # Add text within delimiters as a new node of the specified type
                    delim_text = node.text[open_delim + len(delimiter):close_delim]
                    new_nodes.append(TextNode(delim_text, text_type, node.url))
                    start = close_delim + len(delimiter)
        else:
            # For nodes not of type 'text', add them directly to the new list
            new_nodes.append(node)

    print(new_nodes)
    return new_nodes


if __name__ == "__main__":
    dummy_obj = TextNode("This is a text node", "bold", "https://www.boot.dev")
    node = TextNode("This is text with a `code block` word", "text")
    new_nodes = split_nodes_delimiter([node], "`", "code")
    print(repr(dummy_obj))

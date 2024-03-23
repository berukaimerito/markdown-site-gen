from leafnode import LeafNode
from textnode import TextNode

def text_node_to_html_node(text_node):
    type_key = f"text_type_{text_node.text_type}"
    node_dict = {
        "text_type_text" : "text",
        "text_type_bold" : "bold",
        "text_type_italic" : "italic",
        "text_type_code" : "code",
        "text_type_link" : "link",
        "text_type_image" : "image"
    }

    if node_dict.get(type_key, None) == None:
        raise KeyError(f"Type of {text_node} doesn't exist.")

    if node_dict.get(type_key) == "text":
        obj = LeafNode(tag=None, value=text_node.text)
        return obj.to_html()
    if node_dict.get(type_key) == "bold":
        obj = LeafNode(tag="b", value=text_node.text)
        return obj.to_html()
    if node_dict.get(type_key) == "italic":
        return LeafNode(tag="i", value=text_node.text)
    if node_dict.get(type_key) == "code":
        return LeafNode(tag="code", value=text_node.text)
    if node_dict.get(type_key) == "link":
        props_dict = {"href": text_node.url}
        return LeafNode(tag="a", value=text_node.text, props=props_dict)
    if node_dict.get(type_key) == "image":
        props_dict = {"src": text_node.url , "alt": text_node.text}
        return LeafNode(tag="img", value="", props=props_dict)

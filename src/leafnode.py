from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        if value == None:
            raise ValueError("Leaf node must have a value.")
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.props == other.props:
            return True
        return False

    def to_html(self):
        if not self.tag or self.tag.strip() == "":
            return f"{self.value}"
        else:
            props_html = self.props_to_html()
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

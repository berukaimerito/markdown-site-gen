from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        if children is None or not isinstance(children, list) or not children:
                   raise ValueError("Parent node must have a non-empty list of children.")
        super().__init__(tag, None, children, props)

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (self.tag == other.tag and
            self.children == other.children and
            self.props == other.props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag must be provided")
        props_html = self.props_to_html()
        children_html = ''.join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"


    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

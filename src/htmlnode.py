class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag # A string representing html tag name
        self.value = value # A string representing the value of the HTML tag
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        if self.tag:
            opening_tag = f"<{self.tag}{self.props_to_html()}>"
            closing_tag = f"</{self.tag}>"
            children_html = ''.join(child.to_html() for child in self.children)
            return f"{opening_tag}{self.value if self.value else ''}{children_html}{closing_tag}"

    def props_to_html(self):
        result = ""
        if self.props:
            for key, props_value in self.props.items():
                result += f' {key}="{props_value}"'
        return result

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


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
            if self.tag is None:
                raise ValueError("Tag must be provided")
            props_html = self.props_to_html()
            children_html = ''.join(child.to_html() for child in self.children)
            html_output = f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
            return html_output


    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


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
                if self.tag in ["img", "input", "br", "hr"]:  # Self-closing tags
                    html_output = f"<{self.tag}{props_html} />"
                    if self.tag == "img":
                        print(f"Converting image node to HTML: <img src='{self.props.get('src')}' alt='{self.props.get('alt')}' />")
                else:
                    html_output = f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
                return html_output

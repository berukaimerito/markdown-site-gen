class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag # A string representing html tag name
        self.value = value # A string representing the value of the HTML tag
        self.children = children if children is not None else []
        self.props = props

    def to_html(self):
        raise NotImplementedError("Function is not implemented")

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

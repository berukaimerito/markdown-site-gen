import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
        # Create an HTML node with a "div" tag, no value, and no children
    div_node_1 = HTMLNode("div")
    div_node_4 = HTMLNode("div")

        # Create another HTML node with a "div" tag, a class property, and no children
    div_node_2 = HTMLNode("div", props={"class": "container"})

        # Create an HTML node with a "p" tag, some text as value, and no children
    p_node_1 = HTMLNode("p", "This is a paragraph")

        # Create an HTML node with a "div" tag, no value, and some children
    div_node_3 = HTMLNode(
            "div",
            children=[
                HTMLNode("p", "This is a child paragraph 1"),
                HTMLNode("p", "This is a child paragraph 2"),
            ],
        )

        # Create an HTML node with a "ul" tag, no value, and some children
    ul_node = HTMLNode(
            "ul",
            children=[
                HTMLNode("li", "First item"),
                HTMLNode("li", "Second item"),
                HTMLNode("li", "Third item"),
            ],
        )

        # Put all the created nodes in a list

    html_nodes = [div_node_1, div_node_2, p_node_1, div_node_3, ul_node]
    html_nodes_len = len(html_nodes)

    def test_props_to_html(self):
        expected_output = ' class="container"'
        self.assertEqual(self.div_node_2.props_to_html(), expected_output)
           # Test with a node without properties
        self.assertEqual(self.div_node_1.props_to_html(), "")

    def print_nodes(self):
        for node in self.html_nodes:
            print(node) # Automatically calls __repr__ method due to the print function

    def test_eq(self):
        self.assertEqual(self.div_node_4, self.div_node_1)
        self.assertNotEqual(self.div_node_1, self.div_node_2)


if __name__ == "__main__":
    unittest.main()

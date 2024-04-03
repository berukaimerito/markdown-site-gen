import unittest
from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):

    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    node_simple = ParentNode(
        "div",
        [
            LeafNode("h1", "Header Text"),
            LeafNode("p", "Paragraph Text"),
        ]
    )

    node_nested = ParentNode(
        "div",
        [
            ParentNode(
            "ul",
            [
                LeafNode("li", "List item 1"),
                LeafNode("li", "List item 2")
            ]
        ),

        ]

    )
    node_mixed = ParentNode(
        "article",
        [
            LeafNode("h2", "Article Header"),
            LeafNode(None, "Some introductory text without a tag."),
            ParentNode(
                "section",
                [
                    LeafNode("p", "Section paragraph."),
                    LeafNode(None, "Another text snippet."),
                ]
            ),
        ]
    )

    node_props = ParentNode(
        "footer",
        [
            LeafNode("a", "Click here", {"href": "https://example.com", "target": "_blank"}),
            LeafNode("span", "Copyright ©", {"style": "color: #ccc;"}),
        ]
    )

    nodes_list = [node_nested, node_mixed, node_simple, node, node_props]

    node_mixed_string = "<article><h2>Article Header</h2>Some introductory text without a tag.<section><p>Section paragraph.</p>Another text snippet.</section></article>"
    node_simple_string = "<div><h1>Header Text</h1><p>Paragraph Text</p></div>"
    node_string = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
    node_nested_string = "<div><ul><li>List item 1</li><li>List item 2</li></ul><p>Paragraph in div</p></div>"
    node_props_string = '<footer><a href="https://example.com" target="_blank">Click here</a><span style="color: #ccc;">Copyright ©</span></footer>'

    node_string_list = [node_nested_string, node_mixed_string, node_simple_string, node_string, node_props_string]

    list_len = len(node_string_list)

    def test_eq(self):
        self.assertEqual(self.node.to_html(), self.node_string)
        self.assertEqual(self.node_simple.to_html(), self.node_simple_string)
        self.assertNotEqual(self.node_nested.to_html(), self.node_nested_string)
        self.assertEqual(self.node_mixed.to_html(), self.node_mixed_string)
        self.assertEqual(self.node_props.to_html(), self.node_props_string)

    def test_to_hmtl(self):
        generated_html = self.nodes_list[2].to_html()
        expected_html = self.node_string_list[2]
        self.assertEqual(generated_html, expected_html)

if __name__ == "__main__":
    unittest.main()

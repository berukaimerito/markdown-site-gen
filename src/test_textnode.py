import unittest
from textnode import TextNode
from main import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode("This is an anohter text node", "italic")
        node4 = TextNode("This is an anohter text node", "bold")
        self.assertEqual(node, node2)
        #self.assertEqual(node3, node4)
    def test_split_code_delimiter(self):
        node_code = TextNode("This is text with a `code block` word", "text")
        expected_code = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text")
        ]

        new_nodes_code = split_nodes_delimiter([node_code], "`", "code")
        self.assertEqual(len(new_nodes_code), len(expected_code))

        for new_node, expected_node in zip(new_nodes_code, expected_code):
            self.assertEqual(new_node.text, expected_node.text)
            self.assertEqual(new_node.text_type, expected_node.text_type)
    def test_split_italc_delimiter(self):
        node_italic = TextNode("This is text with *italic* word", "text")
        expected_italic = [
            TextNode("This is text with ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word", "text")
        ]

        new_nodes_italic = split_nodes_delimiter([node_italic], "*", "italic")
        self.assertEqual(len(new_nodes_italic), len(expected_italic))

        for new_node, expected_node in zip(new_nodes_italic, expected_italic):
            self.assertEqual(new_node.text, expected_node.text)
            self.assertEqual(new_node.text_type, expected_node.text_type)

    def test_split_bold_delimiter(self):
        node_bold = TextNode("This is text with **bold** word", "text")
        expected_bold = [
            TextNode("This is text with ", "text"),
            TextNode("bold", "bold"),
            TextNode(" word", "text")
        ]

        new_nodes_bold = split_nodes_delimiter([node_bold], "**", "bold")
        self.assertEqual(len(new_nodes_bold), len(expected_bold))

        for new_node, expected_node in zip(new_nodes_bold, expected_bold):
            self.assertEqual(new_node.text, expected_node.text)
            self.assertEqual(new_node.text_type, expected_node.text_type)


if __name__ == "__main__":
    unittest.main()

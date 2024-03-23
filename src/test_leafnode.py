from leafnode import LeafNode
import unittest


class TestLeafNode(unittest.TestCase):
    leaf_node = "<p>I am just a paragraph leaf me alone</p>"
    leaf_node_2 = "<p>This is a paragraph of text.</p>"
    leaf_node_3 = '<a href="https://www.google.com">Click me!</a>'
    leaf_node_obj_1 = LeafNode("p", "This is a paragraph of text.")
    leaf_node_obj_2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    leaf_node_obj_3 = LeafNode("p", "This is a paragraph of text.")

    def test_eq(self):
        self.assertEqual(self.leaf_node_obj_1, self.leaf_node_obj_3)
        self.assertNotEqual(self.leaf_node_obj_2, self.leaf_node_obj_3)

    def test_to_html(self):
        expected_output = self.leaf_node_2
        self.assertEqual(self.leaf_node_obj_2.to_html(), self.leaf_node_3)
        self.assertEqual(self.leaf_node_obj_3.to_html(), self.leaf_node_2)

if __name__ == "__main__":
    unittest.main()

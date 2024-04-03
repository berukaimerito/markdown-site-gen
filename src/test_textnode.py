import unittest
from textnode import TextNode
from inline_markdown import split_nodes_delimiter, extract_markdown_links,extract_markdown_images, split_nodes_image, split_nodes_links

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

    def test_split_italic_delimiter(self):
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

    def test_extract_markdown_links(self):
        node1 = TextNode("Check out [Google](https://www.google.com) for more information.", "text")
        node2 = TextNode("Here's a link to [GitHub](https://github.com) - a platform for hosting and reviewing code.", "text")
        node3 = TextNode("Discover more about Python at [Python.org](https://www.python.org).", "text")
        node4 = TextNode("Markdown is simple! Here's how to create a [link](https://example.com).", "text")

        text_links = [node1.text, node2.text, node3.text, node4.text]
        expected_list_of_tuples = [
            [('Google', 'https://www.google.com')],
            [('GitHub', 'https://github.com')],
            [('Python.org', 'https://www.python.org')],
            [('link', 'https://example.com')]
        ]

        for text, expected_links in zip(text_links, expected_list_of_tuples):
            extracted_links = extract_markdown_links(text)
            self.assertEqual(len(extracted_links), len(expected_links))
            for extracted_link, expected_link in zip(extracted_links, expected_links):
                self.assertEqual(extracted_link, expected_link)

    def test_extract_markdown_images(self):
         node1 = TextNode("Check out this awesome logo! ![Logo](https://example.com/logo.png)", "text")
         node2 = TextNode("Here's an image of a cat ![Cat Image](https://example.com/cat.png 'A Cute Cat')", "text")
         node3 = TextNode("Documentation includes a diagram ![Diagram](https://example.com/diagram.png)", "text")
         node4 = TextNode("Markdown allows embedding images ![Image](https://example.com/image.png 'Title')", "text")
         # List of the text from each node
         text_images = [node1.text, node2.text, node3.text, node4.text]
         # Expected results for image extraction
         expected_list_of_tuples = [
             [('Logo', 'https://example.com/logo.png')],
             [('Cat Image', 'https://example.com/cat.png')],
             [('Diagram', 'https://example.com/diagram.png')],
             [('Image', 'https://example.com/image.png')]
         ]

         for text, expected_images in zip(text_images, expected_list_of_tuples):
             exctracted_images = extract_markdown_images(text)
             self.assertEqual(len(exctracted_images), len(expected_images))
             for extracted_image, expected_image in zip(exctracted_images, expected_images):
                 self.assertEqual(extracted_image, expected_image)

    def test_split_node_images(self):
        node1 = TextNode("Welcome to the tutorial! ![Tutorial Image](https://i.imgur.com/tutorial.png) Follow these steps to get started.", "text",)
        node2 = TextNode("Check out our gallery ![Gallery Image 1](https://i.imgur.com/gallery1.png) and don't miss the special collection ![Special Collection](https://i.imgur.com/special.png).","text",)
        node3 = TextNode("For more information, visit our site ![Site Logo](https://i.imgur.com/siteLogo.png). Join our community ![Community Logo](https://i.imgur.com/community.png) to connect with others.","text",)

        nodes = [node1, node2, node3]
        expected_list_of_text_objects = [
            [
                TextNode("Welcome to the tutorial! ", "text"),
                TextNode("![Tutorial Image](https://i.imgur.com/tutorial.png)", "image"),
                TextNode(" Follow these steps to get started.", "text"),
            ],
            [
                TextNode("Check out our gallery ", "text"),
                TextNode("![Gallery Image 1](https://i.imgur.com/gallery1.png)", "image"),
                TextNode(" and don't miss the special collection ", "text"),
                TextNode("![Special Collection](https://i.imgur.com/special.png)", "image"),
                TextNode(".", "text"),
            ],
            [
                TextNode("For more information, visit our site ", "text"),
                TextNode("![Site Logo](https://i.imgur.com/siteLogo.png)", "image"),
                TextNode(". Join our community ", "text"),
                TextNode("![Community Logo](https://i.imgur.com/community.png)", "image"),
                TextNode(" to connect with others.", "text"),
            ],
        ]


        for node, expected_nodes in zip(nodes, expected_list_of_text_objects):
            extracted_nodes = split_nodes_image([node])
            self.assertEqual(len(extracted_nodes), len(expected_nodes))
            for extracted_node, expected_tuple in zip(extracted_nodes, expected_nodes):
                 self.assertEqual(extracted_node, expected_tuple)

    def test_split_node_links(self):
        node1 = TextNode("Here's a [Google](https://www.google.com) link and a [GitHub](https://github.com) link.", "text")
        node2 = TextNode("Follow our [Twitter](https://twitter.com) and visit our [Website](https://example.com).", "text")
        node3 = TextNode("For documentation, see [Docs](https://docs.example.com). For support, join our [Discord](https://discord.com).", "text")

        nodes = [node1, node2, node3]
        expected_list_of_text_objects = [
            [
                TextNode("Here's a ", "text"),
                TextNode("[Google](https://www.google.com)", "link"),
                TextNode(" link and a ", "text"),
                TextNode("[GitHub](https://github.com)", "link"),
                TextNode(" link.", "text"),
            ],
            [
                TextNode("Follow our ", "text"),
                TextNode("[Twitter](https://twitter.com)", "link"),
                TextNode(" and visit our ", "text"),
                TextNode("[Website](https://example.com)", "link"),
                TextNode(".", "text"),
            ],
            [
                TextNode("For documentation, see ", "text"),
                TextNode("[Docs](https://docs.example.com)", "link"),
                TextNode(". For support, join our ", "text"),
                TextNode("[Discord](https://discord.com)", "link"),
                TextNode(".", "text"),
            ],
        ]

        for node, expected_nodes in zip(nodes, expected_list_of_text_objects):
            extracted_nodes = split_nodes_links([node], "text")
            self.assertEqual(len(extracted_nodes), len(expected_nodes))
            for extracted_node, expected_node in zip(extracted_nodes, expected_nodes):
                self.assertEqual(extracted_node.text, expected_node.text)
                self.assertEqual(extracted_node.text_type, expected_node.text_type)


if __name__ == "__main__":
    unittest.main()

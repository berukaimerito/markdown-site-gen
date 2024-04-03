import unittest
from block_markdown import markdown_to_blocks

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Test case 1: Standard separation with more than two newlines in between
        test_markdown_str_1 = "This is **bolded** paragraph\n\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"
        expected_blocks_1 = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]

        # Test case 2: Blocks with only whitespaces or empty
        test_markdown_str_2 = "This is content\n\n  \n\n\n\nAnother block of content"
        expected_blocks_2 = [
            "This is content",
            "Another block of content"
        ]

        # Test case 3: Single block without newlines
        test_markdown_str_3 = "Just a single block without newlines"
        expected_blocks_3 = [
            "Just a single block without newlines"
        ]

        self.assertListEqual(markdown_to_blocks(test_markdown_str_1), expected_blocks_1, "Failed Test 1")
        self.assertListEqual(markdown_to_blocks(test_markdown_str_2), expected_blocks_2, "Failed Test 2")
        self.assertListEqual(markdown_to_blocks(test_markdown_str_3), expected_blocks_3, "Failed Test 3")

if __name__ == '__main__':
    unittest.main()

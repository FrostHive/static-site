import unittest
from markdown_functions import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_blocks_leading_and_trailing_spaces(self):
        md = "   First block.   \n\n  Second block. \n\nThird block.  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "First block.",
            "Second block.",
            "Third block."
        ])


    def test_markdown_blocks_extra_newlines(self):
        md = "This is a test block.\n\n\n\nThis is another test block.\n\n\nThis is the final test block."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is a test block.",
            "This is another test block.",
            "This is the final test block."
        ])


    def test_markdown_blocks_leading_and_trailing_newlines(self):
        md = "\n\nTest block 1.\n\nTest block 2.\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Test block 1.",
            "Test block 2."
        ])

    def test_markdown_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_whitespace_only(self):
        md = "    \n \n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

class TestBlockToType(unittest.TestCase):

    def test_heading_block(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_block_with_multiple_hashes(self):
        block = "### Subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_inline(self):
        block = "```print('inline code')```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> This is another quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is a normal paragraph.\nIt has multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_partial_quote_paragraph_block(self):
        block = "> This is a quote\nBut this line is not"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_partial_unordered_list_paragraph_block(self):
        block = "- Item one\nNot an item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_wrong_ordered_list_block(self):
        block = "0. First item\n2. Skipped number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_with_trailing_spaces(self):
        block = "# Heading with space    "
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

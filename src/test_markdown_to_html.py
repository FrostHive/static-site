import unittest
from markdown_to_html import markdown_to_html_node, extract_title

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_levels(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
> with _italic_ and **bold** inside
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with <i>italic</i> and <b>bold</b> inside</blockquote></div>"
        )

    def test_blockquote_2(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""

    def test_unordered_list(self):
        md = """
- First item
- Second **bold** item
- Third with `code`
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second <b>bold</b> item</li><li>Third with <code>code</code></li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. First _italic_ item
2. Second item with `code`
3. Third **bold** item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First <i>italic</i> item</li><li>Second item with <code>code</code></li><li>Third <b>bold</b> item</li></ol></div>"
        )

    def test_multiple_headings_and_lists(self):
        md = """
# Main Heading

Some intro text.

## Subsection A

1. Item A1
2. Item A2 with `code`

## Subsection B

- Bullet B1
- Bullet B2 with _italic_
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div>"
            "<h1>Main Heading</h1>"
            "<p>Some intro text.</p>"
            "<h2>Subsection A</h2>"
            "<ol>"
            "<li>Item A1</li>"
            "<li>Item A2 with <code>code</code></li>"
            "</ol>"
            "<h2>Subsection B</h2>"
            "<ul>"
            "<li>Bullet B1</li>"
            "<li>Bullet B2 with <i>italic</i></li>"
            "</ul>"
            "</div>"
        )

class TestExtractTitle(unittest.TestCase):
    def test_valid_title_first_line(self):
        md = "# My Document Title\nSome text below"
        result = extract_title(md)
        self.assertEqual(result, "My Document Title")

    def test_valid_title_with_leading_whitespace(self):
        md = "   #    Indented Title\nMore content"
        result = extract_title(md)
        self.assertEqual(result, "Indented Title")

    def test_valid_title_not_first_line(self):
        md = """
Some intro text here

# Actual Title

And some more content
"""
        result = extract_title(md)
        self.assertEqual(result, "Actual Title")

    def test_no_title_raises_exception(self):
        md = """
## Subtitle Only

Some paragraph

### Even smaller title
"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header line.")

    def test_empty_string_raises_exception(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_title_with_extra_hashes(self):
        md = """
### Not a match
# Valid Title Here
## Another one
"""
        result = extract_title(md)
        self.assertEqual(result, "Valid Title Here")

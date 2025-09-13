import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_diff_texttype(self):
        node = TextNode("This is a test node", TextType.LINK_TEXT, "random_url")
        node2 = TextNode("This is a test node", TextType.IMAGE_TEXT, "random_url")
        self.assertNotEqual(node, node2)

    def test_has_url(self):
        node = TextNode("This is a test node", TextType.LINK_TEXT, "random_url")
        self.assertTrue(node.url)

    def test_no_url(self):
        node = TextNode("This is a test node", TextType.ITALIC_TEXT)
        self.assertFalse(node.url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_link(self):
        node = TextNode("This is a test node", TextType.LINK_TEXT, "random_url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a test node")
        self.assertEqual(html_node.props, {"href": node.url})

if __name__ == "__main__":
    unittest.main()

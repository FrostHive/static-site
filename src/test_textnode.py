import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from text_functions import extract_markdown_links, split_nodes_delimiter, extract_markdown_images, split_nodes_link, split_nodes_image, text_to_textnodes

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

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_base(self):
        node = TextNode("This is a test node with **bold text**.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is a test node with ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(".", TextType.PLAIN_TEXT)
            ]
        )

    def test_split_nodes_italic(self):
        node = TextNode("This is a test node with **bold text**.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is a test node with ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(".", TextType.PLAIN_TEXT)
            ]
        )

    def test_split_nodes_code(self):
        node = TextNode("This is a test node with `code text`.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is a test node with ", TextType.PLAIN_TEXT),
            TextNode("code text", TextType.CODE_TEXT),
            TextNode(".", TextType.PLAIN_TEXT)
            ]
        )

    def test_split_nodes_double(self):
        node = TextNode("This is a test node with **double **bold text****.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is a test node with ", TextType.PLAIN_TEXT),
            TextNode("double ", TextType.BOLD_TEXT),
            TextNode("bold text****.", TextType.PLAIN_TEXT)
            ]
        )

    def test_split_nodes_multiple(self):
        node = TextNode("This is a test node with `code text`.", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a test node with `more code text`.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is a test node with ", TextType.PLAIN_TEXT),
            TextNode("code text", TextType.CODE_TEXT),
            TextNode(".", TextType.PLAIN_TEXT),
            TextNode("This is a test node with ", TextType.PLAIN_TEXT),
            TextNode("more code text", TextType.CODE_TEXT),
            TextNode(".", TextType.PLAIN_TEXT)
            ]
        )

    def test_split_node_unmatched_bold(self):
        node = TextNode("This is **unmatched bold.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [node])

    def test_split_node_unmatched_code(self):
        node = TextNode("Here is `code without end.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_link(self):
        link_text = "This is test text with a [test link](https://www.boot.dev/lessons/ab12db79-fc4e-46f1-81d2-4694e7f3b8f6)."
        old_node = TextNode(link_text, TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([old_node])
        self.assertListEqual(new_nodes, [
            TextNode("This is test text with a ", TextType.PLAIN_TEXT),
            TextNode("test link", TextType.LINK_TEXT, "https://www.boot.dev/lessons/ab12db79-fc4e-46f1-81d2-4694e7f3b8f6"),
            TextNode(".", TextType.PLAIN_TEXT)
        ])

    def test_split_nodes_link_multiple(self):
        link_text = "This is test text with a [test link](https://www.boot.dev/lessons/ab12db79-fc4e-46f1-81d2-4694e7f3b8f6) and another [test link](https://www.boot.dev/lessons/bd4a35b7-e7a5-4ae3-96d7-051695ebd3da)."
        old_node = TextNode(link_text, TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([old_node])
        self.assertListEqual(new_nodes, [
            TextNode("This is test text with a ", TextType.PLAIN_TEXT),
            TextNode("test link", TextType.LINK_TEXT, "https://www.boot.dev/lessons/ab12db79-fc4e-46f1-81d2-4694e7f3b8f6"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("test link", TextType.LINK_TEXT, "https://www.boot.dev/lessons/bd4a35b7-e7a5-4ae3-96d7-051695ebd3da"),
            TextNode(".", TextType.PLAIN_TEXT)
        ])

    def test_split_nodes_no_link(self):
        link_text = "This is test text with no test link."
        old_node = TextNode(link_text, TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([old_node])
        self.assertListEqual(new_nodes, [old_node])

    def test_split_nodes_link_with_par(self):
        text = "[some (link)](http://example.com)"
        node = TextNode(text, TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("some (link)", TextType.LINK_TEXT, "http://example.com")
        ])

    def test_split_nodes_link_bad_syntax(self):
        bad_link = "This is a bad [link](missing-end"
        node = TextNode(bad_link, TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_image(self):
        image_text = "This is test text with a ![test image](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Single.jpg)."
        old_node = TextNode(image_text, TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([old_node])
        self.assertListEqual(new_nodes, [
            TextNode("This is test text with a ", TextType.PLAIN_TEXT),
            TextNode("test image", TextType.IMAGE_TEXT, "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Single.jpg"),
            TextNode(".", TextType.PLAIN_TEXT)
        ])

    def test_split_nodes_image_multiple(self):
        image_text = "This is test text with a ![test image](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Single.jpg/960px-Banana-Single.jpg) and another ![test image](https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Strawberry_gariguette_DSC03063.JPG)."
        old_node = TextNode(image_text, TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([old_node])
        self.assertListEqual(new_nodes, [
            TextNode("This is test text with a ", TextType.PLAIN_TEXT),
            TextNode("test image", TextType.IMAGE_TEXT, "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Single.jpg/960px-Banana-Single.jpg"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("test image", TextType.IMAGE_TEXT, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Strawberry_gariguette_DSC03063.JPG"),
            TextNode(".", TextType.PLAIN_TEXT)
        ])

    def test_split_nodes_image_bad_syntax(self):
        bad_image = "This is a bad ![image](missing-end"
        node = TextNode(bad_image, TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_no_image(self):
        image_text = "This is test text with no test image."
        old_node = TextNode(image_text, TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([old_node])
        self.assertListEqual(new_nodes, [old_node])

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode(self):
        sample_text = "This is test text with **bold text** and _italic text_ and also `code text` and even a [link](https://www.boot.dev/lessons/21db95df-68e9-4f10-9c76-16142abba580)!"
        nodes = text_to_textnodes(sample_text)
        self.assertEqual(nodes, [
            TextNode("This is test text with ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("italic text", TextType.ITALIC_TEXT),
            TextNode(" and also ", TextType.PLAIN_TEXT),
            TextNode("code text", TextType.CODE_TEXT),
            TextNode(" and even a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK_TEXT, "https://www.boot.dev/lessons/21db95df-68e9-4f10-9c76-16142abba580"),
            TextNode("!", TextType.PLAIN_TEXT)
        ])

    def test_code_with_asterisks_inside(self):
        text = "`code with **asterisks** inside`"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("code with **asterisks** inside", TextType.CODE_TEXT)
        ])

    def test_empty_text(self):
        node = TextNode("", TextType.PLAIN_TEXT)
        new_nodes = text_to_textnodes("")
        self.assertEqual(new_nodes, [node])


class TestExtractMarkdown(unittest.TestCase):

    def test_extract_image(self):
        image_text = "This is test text with a ![test image](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Single.jpg)"
        image_list = extract_markdown_images(image_text)
        self.assertListEqual(image_list, [("test image","https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Single.jpg")])

    def test_extract_link(self):
        link_text = "This is test text with a [test link](https://www.boot.dev/lessons/ab12db79-fc4e-46f1-81d2-4694e7f3b8f6)"
        link_list = extract_markdown_links(link_text)
        self.assertListEqual(link_list, [("test link","https://www.boot.dev/lessons/ab12db79-fc4e-46f1-81d2-4694e7f3b8f6")])


if __name__ == "__main__":
    unittest.main()

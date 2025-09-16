import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_only_tag(self):
        node = HTMLNode(tag="Test tag")
        only_has_tag = not (node.value and node.children and node.props)
        self.assertTrue(only_has_tag)

    def text_props_to_html(self):
        node = HTMLNode(
            props={"href": "https://www.boot.def",
                "target": "_blank"
            }
        )
        str_to_print = node.props_to_html()
        self.assertIsInstance(node.props, dict)

    def test_has_children(self):
        node = HTMLNode(children=[HTMLNode(tag="Test tag")])
        self.assertTrue(node.children)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Header 1")
        self.assertEqual(node.to_html(), "<h1>Header 1</h1>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Test bold text")
        self.assertEqual(node.to_html(), "<b>Test bold text</b>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("p", "child3")
        child_node4 = LeafNode("i", "child4")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3, child_node4])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>child2</b><p>child3</p><i>child4</i></div>")

    def test_to_html_with_no_chldren(self):
        parent_node = ParentNode("h3", [])

        self.assertRaises(ValueError, parent_node.to_html)

    def test_child_not_leafnode(self):
        child_node = HTMLNode(tag="p", value="Random Text")
        parent_node = ParentNode("h1", [child_node])
        self.assertRaises(NotImplementedError, parent_node.to_html)

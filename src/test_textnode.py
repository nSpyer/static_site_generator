import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    #test two completely identical nodes to verify sameness
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    #test two nodes with different type values
    def test_uneq_type_value(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    #test two nodes with differing strings but same text type
    def test_uneq_text_value(self):
        node = TextNode("String A", TextType.PLAIN)
        node2 = TextNode("String B", TextType.PLAIN)

    # test two nodes with differing url values
    def test_uneq_url(self):
        node = TextNode("This is a text node", TextType.PLAIN, "https://www.boot.dev")
        node2= TextNode("THis is a text node", TextType.PLAIN, "https://www.boot.dev/lessons")

    #test that repr(node) matches expected string format
    def test_uneq_repr(self):
        node = TextNode("This is a text node", TextType.PLAIN, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.PLAIN, "https://www.boot.dev")

class TestTextNodeToHTMLNode(unittest.TestCase):
 
    # Test that TextType.PLAIN -> LeafNode(None, text)
    def test_plain_text(self):
        node = TextNode("This is a PLAIN node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a PLAIN node")

    # Test that TextType.Bold -> LeafNode("b", text)
    def test_bold(self):
        text = "This is a BOLD node"
        node = TextNode(text, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        correct_node = LeafNode("b", "This is a BOLD node")
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, correct_node.value)

    # Test that TextType.ITALIC -> LeafNode("i", text)
    def test_italic(self):
        text = "This is an ITALIC node"
        node = TextNode(text, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        correct_node = LeafNode("i", "This is an ITALIC node")
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, correct_node.value)
 
    # TextType.CODE -> LeafNode("code", text)
    def test_code(self):
        text = "This is a CODE node"
        node = TextNode(text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        correct_node = LeafNode("code", "This is a CODE node")
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, correct_node.value)

    # TextType.LINK -> LeafNode("a", anchor_text, {"href": url})
    # check html_node.props["href"] == url
    def test_link(self):
        text = "This is anchor text"
        url = "https://www.google.com"
        link_node = TextNode(text, TextType.LINK, url)
        html_node = text_node_to_html_node(link_node)
        correct_node = LeafNode("a", text, {"href":f"{url}"})
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, correct_node.value)
        self.assertEqual(html_node.props, correct_node.props)

    # TextType.IMAGE -> LeafNode("img", "", {"src": url, "alt": alt_text})
    # check html_node.value == "" and props contain both src and alt
    def test_image(self):
        text = "This is alt text"
        url = "https://www.google.com/image.png"
        link_node = TextNode(text, TextType.IMAGE, url)
        html_node = text_node_to_html_node(link_node)
        correct_node = LeafNode("img", "", {"src":f"{url}", "alt":f"{text}"})
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, correct_node.value)
        self.assertEqual(html_node.props, correct_node.props)

    # Test that a text node with an invalid type raises an exception
    def test_invalid_type_raises(self):
        text = "MMMmmm. Muffins."
        with self.assertRaises(Exception):
            invalid_node = TextNode(text, TextType.MUFFINS)
            text_node_to_html_node(invalid_node)


if __name__ == "__main__":
    unittest.main()

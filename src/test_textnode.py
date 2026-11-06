import unittest
from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()

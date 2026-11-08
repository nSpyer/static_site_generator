import unittest
from textnode import TextNode, TextType, text_node_to_html_node


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
    
    #TextType.PLAIN -> LeafNode(None, text)
    def test_plain_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    # TextType.Bold -> LeafNode("b", text)
    def test_bold(self):
    # TODO: TextType.BOLD -> LeafNode("b", text)
        pass

    def test_italic(self):
        # TODO: TextType.ITALIC -> LeafNode("i", text)
        pass

    def test_code(self):
        # TODO: TextType.CODE -> LeafNode("code", text)
        pass

    def test_link(self):
        # TODO: TextType.LINK -> LeafNode("a", anchor_text, {"href": url})
        # check html_node.props["href"] == url
        pass

    def test_image(self):
        # TODO: TextType.IMAGE -> LeafNode("img", "", {"src": url, "alt": alt_text})
        # check html_node.value == "" and props contain both src and alt
        pass

    def test_invalid_type_raises(self):
        # TODO: construct a TextNode-like object/mock with an invalid text_type
        # or monkeypatch text_type, assert raises Exception
        pass



if __name__ == "__main__":
    unittest.main()

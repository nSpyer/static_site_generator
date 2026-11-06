import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    # test props_to_html with multiple props
        #assert the returned string matches expected format
    def test_all_props(self):
        child_1 = HTMLNode("child 1 tag", "child 1 value")
        child_2 = HTMLNode("child 2 tag", "child 2 value")
        children = [child_1, child_2]
        props_dict = {"src": "banner.png",
                      "alt": "Mountain sunrise",
                      "width": "800",
                      "height": "300",
        }
        node = HTMLNode("tag text", "value text", children, props_dict)
        cmp_str = ' src="banner.png" alt="Mountain sunrise" width="800" height="300"'
        self.assertEqual(node.props_to_html(), cmp_str)

    #assert that a node with no props returns an empty string with props_to_html()
    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    #assert that a tag is reproduced correctly on it's own
    def test_tag_prop_(self):
        node = HTMLNode("tag text")
        self.assertEqual(node.__repr__(), "tag: tag text")

    #assert that a value is reproduced correctly on it's own
    def test_value_prop(self):
        node = HTMLNode(None, "value text")
        self.assertEqual(node.__repr__(), "value: value text")

    # is this not circular and therefore pointless?
    def test_children_prop(self):
        child_one = HTMLNode("span", "first")
        child_two = HTMLNode("span", "second")
        children = [child_one, child_two]
        parent = HTMLNode("div", children=children)
        self.assertEqual(parent.children, children)

    #tests proper formatting of self.props -- also circular and kind of pointless
    def test_props_prop(self):
        node = HTMLNode(None, None, None, {"src": "banner.png",
                                           "alt": "Mountain sunrise",
                                           "width": "800",
                                            "height": "300"})
        self.assertEqual(node.__repr__(), f"props: {node.props}")

    def test_empty_props_dict(self):
        node = HTMLNode(None, None, None, {})
        self.assertEqual(node.__repr__(), "props: {}")


    #test that to_html raises NotImplementedError
        #use self.assertRaises(NotImplementedError) as a "context manager"
    def test_not_implemented(self):
        node = HTMLNode("tag text", "value text")
        with self.assertRaises(NotImplementedError):
            node.to_html()


import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    
    #HTMLNode tests--------------------
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
    


    #LeafNode Tests----------------
    #tests a simple bit of paragraph text formatting
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(),"<p>Hello, world!</p>")

    #test a tag with props
    def test_tag_with_props_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"} )
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    # test raw text with no tag converted to HTML with LeafNode
    def test_raw_text_w_no_tag(self):
        node = LeafNode(None, "just text")
        self.assertEqual(node.to_html(), "just text")

    # missing value raises an Error
    def test_missing_value_raises_value_error(self):
        node = LeafNode("tag", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # test different HTML tags.... <b>, <h1>, <i>

    #ParentNode tests -------------
    #tests html conversion of a parent node with one child
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    #tests html conversion of a parent_node with one child which has one child
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    #test html conversion of a parent_node with multiple children

    #test html conversion of a parent_node with a great grandchild

    #test html conversion of a parent_node with both LeafNode and ParentNode
    # instances as direct siblings in its children
    
    #missing tag validation - verify that calling .to_html() raises a ValueError when
    #tag is None or an empty string using assertRaises(ValueError)

    #missing children validation = verify calling .to_html() raises a ValueError when
    # children is None

    # nodes w/ props - a parentnode initialized with a props dict
    # ensures HTML attributes render correclty on the parent tag alongside its children

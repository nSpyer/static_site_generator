import unittest
from inline_markdown import (split_nodes_delimiter, 
        extract_markdown_images, 
        split_nodes_image, 
        extract_markdown_links,
        split_nodes_link,
        text_to_textnodes,
)
from textnode import TextNode, TextType
from htmlnode import HTMLNode

class TestSplitNodesDelimiter(unittest.TestCase):

#test a single delimiter pair in the middle of text
    def test_single_delimiter_pair(self):
        text = "This is text with a **bolded phrase** in the middle."
        correct_result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle.", TextType.PLAIN),
        ]
        old_node = [TextNode(text, TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_node, "**", TextType.BOLD)
        self.assertEqual(correct_result, new_nodes)

#test a delimiter at the very start of the text 
    def test_delimiter_at_start(self):
        text = "**This** is text with a bolded phrase at the beginning."
        correct_result = [
            TextNode("This", TextType.BOLD),
            TextNode(" is text with a bolded phrase at the beginning.", TextType.PLAIN),
        ]
        old_node = [TextNode(text, TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_node, "**", TextType.BOLD)
        self.assertEqual(correct_result, new_nodes)

#test a delimiter at the very end of the text
    def test_delimiter_at_end(self):
        text = "This is text with a bolded phrase at the **end.**"
        correct_result = [
            TextNode("This is text with a bolded phrase at the ", TextType.PLAIN),
            TextNode("end.", TextType.BOLD),
        ]
        old_node = [TextNode(text, TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_node, "**", TextType.BOLD)
        self.assertEqual(correct_result, new_nodes)

#multiple delimiter pairs in the same text (non-nested)
    def test_multiple_non_nested_delimiter_pairs(self):
        text = "This is **text** with **multiple bolded phrases** in the middle."
        correct_result = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with ", TextType.PLAIN),
            TextNode("multiple bolded phrases", TextType.BOLD),
            TextNode(" in the middle.", TextType.PLAIN),
        ]
        old_node = [TextNode(text, TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_node, "**", TextType.BOLD)
        self.assertEqual(correct_result, new_nodes)

# test all delimiter types, bold (**), italic(_), and code(`)
    def test_bold_delimiter(self):
        text = "This is a **bold** delimiter test."
        correct_result = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" delimiter test.", TextType.PLAIN),
        ]
        old_node = [TextNode(text, TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_node, "**", TextType.BOLD)
        self.assertEqual(correct_result, new_nodes)

    def test_italic_delimiter(self):
        text = "This is an _italic_ delimiter test."
        correct_result = [
            TextNode("This is an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" delimiter test.", TextType.PLAIN),
        ]
        old_node = [TextNode(text, TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_node, "_", TextType.ITALIC)
        self.assertEqual(correct_result, new_nodes)

    def test_code_delimiter(self):
        text = "This is a `code` delimiter test."
        correct_result = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" delimiter test.", TextType.PLAIN),
        ]
        old_node = [TextNode(text, TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(old_node, "`", TextType.CODE)
        self.assertEqual(correct_result, new_nodes)

# test text with no delimiters at all remains unchanged as a single node
    def test_no_delimiters(self):
        node = TextNode("text with no delimiters", TextType.PLAIN)
        node_split = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(node, node_split[0])


#test unmatched/missing closing delimiter raises an exception
    def test_exception_for_unmatched_closing_delimiter(self):
        text = "This is text with an **unmatched closing delimiter."
        old_node = [TextNode(text, TextType.PLAIN)]
        with self.assertRaises(ValueError):
            split_node = split_nodes_delimiter(old_node, "**", TextType.BOLD)

#test an input list with multiple old nodes, checkin the new list properly combines
    #the results of each
    def test_mutltiple_old_nodes(self):
        text_a = "This is **text A**."
        text_b = "This is **text B**."
        old_node_a = TextNode(text_a, TextType.PLAIN)
        old_node_b = TextNode(text_b, TextType.PLAIN)
        old_nodes = [old_node_a, old_node_b]
        split_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        correct_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text A", TextType.BOLD),
            TextNode(".", TextType.PLAIN),
            TextNode("This is ", TextType.PLAIN),
            TextNode("text B", TextType.BOLD),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertListEqual(split_nodes, correct_nodes)


class TestRegex(unittest.TestCase):
    # tests that the extraction function for markdown image text returns the correct tuple
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    # same as above function but tests links instead of images
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [anchor text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("anchor text", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestSplitNodesImage(unittest.TestCase):
    # image format for markdown is ![alt_text](url)
    def test_single_image(self):
        node_md = TextNode("![This is alt text](https://www.google.com/image.png)", TextType.PLAIN)
        old_nodes = [node_md]
        return_node = split_nodes_image(old_nodes)
        node_a = TextNode("This is alt text", TextType.IMAGE, "https://www.google.com/image.png")
        self.assertEqual(return_node[0], node_a)

    def test_multiple_images(self):
        node_md = TextNode("This is one image: ![This is alt text](https://www.google.com/image.png) and this is another: ![This is also alt text](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN)
        old_nodes = [node_md]
        return_nodes = split_nodes_image(old_nodes)
        node_a = TextNode("This is one image: ", TextType.PLAIN)
        node_b = TextNode("This is alt text", TextType.IMAGE, "https://www.google.com/image.png")
        node_c = TextNode(" and this is another: ", TextType.PLAIN)
        node_d = TextNode("This is also alt text", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        new_nodes = [node_a, node_b, node_c, node_d]
        self.assertEqual(return_nodes, new_nodes)

    #test markdown test with no images to extract, should return original node unchanged
    def test_text_with_no_images(self):
        node_md = TextNode("This text has no images!", TextType.PLAIN)
        old_nodes = [node_md]
        return_nodes = split_nodes_image(old_nodes)
        self.assertEqual(return_nodes[0], node_md) 

    #if an image has no alt text, it is technically valid and considered decorative
    def test_for_empty_image_alt_text(self):
        pass

        #include both a markdown image and a markdown link, and ensure the function
        #only grabs what it should
    def test_images_vs_links(self):
        text = "This is an ![image](https://www.google.com/image.png) and this is a [link](https://www.google.com)."
        node = [TextNode(text, TextType.PLAIN)]
        split_nodes = split_nodes_image(node)
        correct_nodes = [
            TextNode("This is an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://www.google.com/image.png"),
            TextNode(" and this is a [link](https://www.google.com).", TextType.PLAIN),
        ]
        self.assertEqual(split_nodes, correct_nodes)



class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes(self):
        md_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        return_nodes = text_to_textnodes(md_text)
        correct_result = [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertEqual(return_nodes, correct_result)



class TestSplitNodesLink(unittest.TestCase):
    # link format for markdown is [alt_text](url)
    def test_single_link(self):
        node_md = TextNode("[This is anchor text](https://www.google.com)", TextType.PLAIN)
        old_nodes = [node_md]
        return_node = split_nodes_link(old_nodes)
        node_a = TextNode("This is anchor text", TextType.LINK, "https://www.google.com")
        self.assertEqual(return_node[0], node_a)

    def test_multiple_links(self):
        node_md = TextNode("This is one link: [This is anchor text](https://www.google.com) and this is another: [This is also anchor text](https://www.boot.dev)", TextType.PLAIN)
        old_nodes = [node_md]
        return_nodes = split_nodes_link(old_nodes)
        node_a = TextNode("This is one link: ", TextType.PLAIN)
        node_b = TextNode("This is anchor text", TextType.LINK, "https://www.google.com")
        node_c = TextNode(" and this is another: ", TextType.PLAIN)
        node_d = TextNode("This is also anchor text", TextType.LINK, "https://www.boot.dev")
        new_nodes = [node_a, node_b, node_c, node_d]
        self.assertEqual(return_nodes, new_nodes)

    #test markdown test with no images to extract, should return original node unchanged
    def test_text_with_no_links(self):
        node_md = TextNode("This text has no links!", TextType.PLAIN)
        old_nodes = [node_md]
        return_nodes = split_nodes_link(old_nodes)
        self.assertEqual(return_nodes[0], node_md) 

    #if an image has no alt text, it is technically valid and considered decorative
    def test_for_empty_link_anchor_text(self):
        pass

        #include both a markdown image and a markdown link, and ensure the function
        #only grabs what it should
    def test_links_vs_images(self): 
        text = "This is an ![image](https://www.google.com/image.png) and this is a [link](https://www.google.com)."
        node = [TextNode(text, TextType.PLAIN)]
        split_nodes = split_nodes_link(node)
        correct_nodes = [
            TextNode("This is an ![image](https://www.google.com/image.png) and this is a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://www.google.com"),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(split_nodes, correct_nodes)


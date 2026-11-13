import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, split_nodes_image, extract_markdown_links, text_to_textnodes
from textnode import TextNode, TextType


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

# test that a node that's already a non-TEXT type passes through unchanged
    def test_non_text_node(self):
        pass

#test multiple nodes in the input, where only some are TEXT type
    def test_mixed_node_types(self):
        pass

# test text with no delimiters at all remain unchanged as a single node
    def test_no_delimiters(self):
        pass

#test unmatched/missing closing delimiter raises an exception
    def test_exception_for_unmatched_closing_delimiter(self):
        pass

#test an input list with multiple old nodes, checkin the new list properly combines
    #the results of each
    def test_mutltiple_old_nodes(self):
        pass

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

    def test_image_at_start_of_text(self): #proven true with test_single_image_test
        pass

    def test_image_at_end_of_text(self): #proven true with test_single_image_test
        pass

    def test_only_image_text(self): #proven true with test_single_image test
        pass

    def test_for_empty_alt_text(self):
        pass

    def test_multiple_nodes_at_once(self): # a list with more than one text node
        pass

    def test_node_that_is_not_text_type_text(self): #should not even be processed
        pass

    def test_links_vs_images(self): #include both a markdown image and a markdown link, and ensure the function
        #only grabs what it should
        pass

    #same but use the opposite TextType as above
    def test_images_vs_links(self):
        pass

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

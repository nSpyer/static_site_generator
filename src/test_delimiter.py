import unittest
from delimiter import split_nodes_delimiter
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
            TextNode("", TextType.PLAIN),
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
            TextNode("", TextType.PLAIN),
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
        pass

    def test_italic_delimiter(self):
        pass

    def test_code_delimiter(self):
        pass

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

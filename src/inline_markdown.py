from textnode import TextNode, TextType
import re

# create TextNodes from raw markdown strings.
# Takes a list of TextNodes, a delimiter specifier for **bold**, _italic_, or `code`, and
# a target text_type to match the delimiter.  returns a new list of TextNodes
# does not support nested inline elements (e.g. bold AND italic)
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        # if not plaintext, then just append the node
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        #split the plaintext with the supplied delimiter
        split_node = node.text.split(delimiter)
 
        # a correctly split node will always have an odd number of text strings in the list before empty strings are pruned
        if len(split_node) % 2 == 0:
            raise Exception("delimiter error: matching closing delimiter not found")
            
            #create and append
            # even indexed strings become TextNode(string, TextType.PLAIN)
        for i in range(len(split_node)):
            if i % 2 == 0:
                if split_node[i] != "":
                    node_i = TextNode(split_node[i], TextType.PLAIN)
                    new_nodes.append(node_i)
            else:
                # odd indexed strings become TextNode(string, text_type)
                if split_node[i] != "":
                    node_i = TextNode(split_node[i], text_type)
                    new_nodes.append(node_i)

    return new_nodes

# regex matches for image format: ![alt text](url)
def extract_markdown_images(text: str) -> list(tuple[str, str]):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

#regex matches for text link format: [anchor text](url)
def extract_markdown_links(text: str) -> list(tuple[str, str]):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

# Splits raw markdown into TextNodes based on images
# Images in markdown follow ![alt text](url)
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        images = extract_markdown_images(remaining_text)

        #if no image, return a list with the original node in it
        if len(images) == 0:
            new_nodes.append(node)
            continue

        #if not plaintext, then just append the node
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        for image in images:
            alt_text = image[0]
            url = image[1]
            md_delimiter = f"![{alt_text}]({url})" #the delimiter markdown has to be assembled
            split_node = remaining_text.split(f"{md_delimiter}", 1) #this will return everything around the markdown, length is always 2

            # create and add node for text before markdown delimiter
            if split_node[0] != "":
                node_h = TextNode(split_node[0], TextType.PLAIN)
                new_nodes.append(node_h)
            # create and append new image node
            node_i = TextNode(alt_text, TextType.IMAGE, url)
            new_nodes.append(node_i)
            remaining_text = split_node[1]

    # append remaining_text if it exists
        if remaining_text != "":
            node_j = TextNode(remaining_text, TextType.PLAIN)
            new_nodes.append(node_j)

    return new_nodes

# Splits raw markdown into TextNodes based on links
# Links in markdown follow [anchor text](url)
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        links = extract_markdown_links(remaining_text)

        #if no link, return a list with the original node in it
        if len(links) == 0:
            new_nodes.append(node)
            continue

        #if not plaintext, then just append the node
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        for link in links:
            anchor_text = link[0]
            url = link[1]
            md_delimiter = f"[{anchor_text}]({url})" #the delimiter markdown has to be assembled
            split_node = remaining_text.split(f"{md_delimiter}", 1) #this will return everything around the markdown, length is always 2

            # create node and append it if preceding text exists
            if split_node[0] != "":
                node_h = TextNode(split_node[0], TextType.PLAIN)
                new_nodes.append(node_h)
            # the new link node should be created and appended
            node_i = TextNode(anchor_text, TextType.LINK, url)
            new_nodes.append(node_i)
            remaining_text = split_node[1] #vital step

        #any remaining_text is appended after the inner loop finishes
        if remaining_text != "":
            node_j = TextNode(remaining_text, TextType.PLAIN)
            new_nodes.append(node_j)

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes = [TextNode(text, TextType.PLAIN)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

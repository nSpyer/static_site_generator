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

        #because of the way split() works with delimiters, it creates an empty string "" at the beginning
        # of a plaintext string when the first word is wrapped in the delimiter
        # the same happens if the last word is wrapped in the delimiter, but with the empty
        # string at the end of the word.  thus a correctly split node will always have an odd number
        # of nodes
        if len(split_node) % 2 == 0:
            raise Exception("delimiter error: matching closing delimiter not found")
            
            #create and append
            # even indexed strings become TextNode(string, TextType.PLAIN)
        for i in range(len(split_node)):
            if i % 2 == 0:
                node_i = TextNode(split_node[i], TextType.PLAIN)
                new_nodes.append(node_i)
            else:
                # odd indexed strings become TextNode(string, text_type)
                node_i = TextNode(split_node[i], text_type)
                new_nodes.append(node_i)

    return new_nodes

# regex matches for image format: ![alt text](url)
# the return at index 0 of matches is the alt text
# the return at index 1 of matches is the url
def extract_markdown_images(text: str) -> list(str):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

#regex matches for text link format: [anchor text](url)
# the return at index 0 of matches is the anchor text
# the return at index 1 of matches is the url
def extract_markdown_links(text: str) -> list(str):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

#splits raw markdown into TextNodes based on images
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:

    #it will work kind of like the split_nodes_delimiter function, but with the extraction function
    #use extract_markdown_images(old_node.text) in a loop
    #images in markdown follow ![alt text](url)

    new_nodes = []
    for node in old_nodes:

        #if no image, return a list with the original node in it
        if extract_markdown_images(node.text) == "":
            new_nodes.append(node)
            continue

        #if not plaintext, then just append the node
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        md_delimiter = extract_markdown_images(node.text) #this is wrong, it is an array of text, url
        #the delimiter markdown has to be assembled
        split_node = node.text.split(f"{md_delimiter}", 1) #this will return everything around the markdown assembled

    # the extraction extracts the markdown link, then split() can be used with that markdown as
    # the delimiter, thus splitting the text before and after it so that it can be placed on either end
    # of the new node created and appended.  that means split_nodes's length should always be 2, ranging from
    # index[0] to index[1]
    #
    # index[0] can be added to the new_nodes array, but NOT index[1], else that will mess up the order
    #
    # the new image node should be created
    #   node_ i = TextNode(node.text, node.IMAGE, node.url)
    #
    #then node_i gets appended to new_nodes
    
    #then index[1]is appended


    #
    #if no image, return a list with the original node in it
    #don't append any TextNodes that have empty text to the final list

#splits raw markdown into TextNodes based on links
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    #will be nearly identical to the function above
    pass


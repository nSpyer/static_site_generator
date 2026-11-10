# create TextNodes from raw markdown strings.
# Takes a list of TextNodes, a delimiter specifier for **bold**, _italic_, or `code`, and
# a target text_type to match the delimiter.  returns a new list of TextNodes
# does not support nested inline elements (e.g. bold AND italic)
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes := []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception("delimiter error: matching closing delimiter not found")
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



def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    pass
    
    #create an empty list to build the return value, which will be extended with each
    #iterative loop using .extend()

    #loop over each node in old_nodes list
         #if old node is NOT a TextType.PLAIN, add it "as is" to the return list
            # use continue so it doesn't get split

        #split the text of the node with .split() into a new list
            # if a matching closing delimiter is not found (aka len(list) % 2 == 0)
                # raise exception with helpful error message
            # even indexed strings become TextNode(string, TextType.PLAIN)
            # odd indexed strings become TextNode(string, text_type)
        
        #loop over the list of nodes just created
            #if the list member is an empty string, do nothing
            #if it is not an empty string, extend the return list with that member's node


    #return new list of nodes

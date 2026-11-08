from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold" #**bold**
    ITALIC = "italic" #_Italic_
    CODE = "code" #`Code`
    LINK = "link" #[anchor text](url)
    IMAGE = "image" #![alt text](url)


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        if (self.text == other.text and 
            self.text_type == other.text_type and
            self.url == other.url):
                return True
        else:
            return False

    def __repr__(self) -> str:
        if self.url != None:
            return "TextNode(" + self.text + ", " + self.text_type.value + ", " + self.url + ")"
        else:
            return "TextNode(" + self.text + ", " + self.text_type.value + ", " + "" + ")"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":f"{text_node.url}", "alt":f"{text_node.text}"})
        case _:
            raise Exception("invalid LeafNode text_type")


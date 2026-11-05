import textnode

def main():
    dummy = textnode.TextNode("dummy link text to boot.dev", textnode.TextType.LINK_TEXT, "https://www.boot.dev")
    print(dummy)

main()

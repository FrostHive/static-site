from textnode import TextNode, TextType


def main():
    new_textnode = TextNode("Some test text", TextType.LINK_TEXT, "https://hollowknight.com")
    print(new_textnode)
main()

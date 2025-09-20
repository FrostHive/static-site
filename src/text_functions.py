import re
from textnode import TextNode, TextType

def text_to_textnodes(text:str):
    old_node = TextNode(text, TextType.PLAIN_TEXT)
    new_nodes = split_nodes_delimiter([old_node], "`", TextType.CODE_TEXT)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD_TEXT)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN_TEXT:
            split_nodes = split_nodes_delimiter_helper(node, delimiter, text_type)
            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_delimiter_helper(old_node, delimiter, text_type):
    new_nodes = []
    has_delimiter = old_node.text.count(delimiter) % 2 == 0 and old_node.text.count(delimiter) >= 2
    if has_delimiter:
        text_list = old_node.text.split(delimiter, 2)
        new_node1 = TextNode(text_list[0], TextType.PLAIN_TEXT)
        new_node2 = TextNode(text_list[1], text_type)
        new_node3 = TextNode("".join(text_list[2:]), TextType.PLAIN_TEXT)
        for new_node in [new_node1, new_node2]:
            if new_node.text != "":
                new_nodes.append(new_node)
        if new_node3.text != "":
            if new_node3.text.count(delimiter) >= 2:
                new_nodes.extend(split_nodes_delimiter_helper(new_node3, delimiter, text_type))
            else:
                new_nodes.append(new_node3)
    else:
        new_nodes.append(old_node)

    return new_nodes

def split_nodes_link(old_nodes:list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        link_list = extract_markdown_links(node.text)
        if len(link_list) <= 0 or node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            new_text = node.text
            for link_tupl in link_list:
                new_text_list = new_text.split(f"[{link_tupl[0]}]({link_tupl[1]})", 1)
                new_node1 = TextNode(new_text_list[0], TextType.PLAIN_TEXT)
                new_node2 = TextNode(link_tupl[0], TextType.LINK_TEXT, link_tupl[1])
                if new_node1.text != "":
                    new_nodes.append(new_node1)
                new_nodes.append(new_node2)
                del new_text_list[0]
                new_text = "".join(new_text_list)
            if new_text != "":
                last_node = TextNode(new_text, TextType.PLAIN_TEXT)
                new_nodes.append(last_node)
    return new_nodes

def split_nodes_image(old_nodes:list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        image_list = extract_markdown_images(node.text)
        if len(image_list) <= 0 or node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            new_text = node.text
            for image_tupl in image_list:
                new_text_list = new_text.split(f"![{image_tupl[0]}]({image_tupl[1]})", 1)
                new_node1 = TextNode(new_text_list[0], TextType.PLAIN_TEXT)
                new_node2 = TextNode(image_tupl[0], TextType.IMAGE_TEXT, image_tupl[1])
                if new_node1.text != "":
                    new_nodes.append(new_node1)
                new_nodes.append(new_node2)
                del new_text_list[0]
                new_text = "".join(new_text_list)
            if new_text != "":
                last_node = TextNode(new_text, TextType.PLAIN_TEXT)
                new_nodes.append(last_node)
    return new_nodes

def extract_markdown_images(text: str):
    image_text_list = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_text_list

def extract_markdown_links(text: str):
    image_text_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_text_list

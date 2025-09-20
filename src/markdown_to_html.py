import enum
from htmlnode import HTMLNode, ParentNode
from markdown_functions import BlockType, markdown_to_blocks, block_to_block_type
from text_functions import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_html_node(markdown: str):
    markdown_blocks = markdown_to_blocks(markdown)
    block_nodes = blocks_to_html_nodes(markdown_blocks)
    root_node = ParentNode("div", block_nodes)
    return root_node

def extract_title(markdown: str):
    markdown_lines = markdown.splitlines()
    header_line = ""

    for line in markdown_lines:
        if line.lstrip().startswith("# "):
            header_line = line.strip()
            break

    if header_line == "":
        raise Exception("No h1 header line.")

    return header_line.lstrip("# ")

def blocks_to_html_nodes(block_list: list[str]):
    list_of_html_nodes = []
    for block in block_list:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                header_node = heading_to_html_node(block)
                list_of_html_nodes.append(header_node)

            case BlockType.CODE:
                code_node = code_to_html_node(block)
                wrapper_node = ParentNode("pre", [code_node])
                list_of_html_nodes.append(wrapper_node)

            case BlockType.QUOTE:
                quote_node = quote_to_html_node(block)
                list_of_html_nodes.append(quote_node)

            case BlockType.UNORDERED_LIST:
                unordered_list_node = u_list_to_html_node(block)
                list_of_html_nodes.append(unordered_list_node)

            case BlockType.ORDERED_LIST:
                ordered_list_node = o_list_to_html_node(block)
                list_of_html_nodes.append(ordered_list_node)

            case BlockType.PARAGRAPH:
                children_nodes = text_to_children_nodes(block, BlockType.PARAGRAPH)
                paragraph_node = ParentNode("p", children_nodes)
                list_of_html_nodes.append(paragraph_node)

            case _:
                raise Exception(f"There isn't any BlockType that matches {block_type} in blocks_to_textnode")

    return list_of_html_nodes


def heading_to_html_node(block: str) -> HTMLNode:
    heading_level = len(block) - len(block.lstrip("#"))
    inline_text = (block.lstrip("#").strip())
    children_html_nodes = text_to_children_nodes(inline_text, BlockType.HEADING)
    parent_node = ParentNode(f"h{heading_level}", children_html_nodes)
    return parent_node

def code_to_html_node(block: str) -> HTMLNode:
    lines = block.splitlines()
    lines = lines[1: -1]
    clean_block = '\n'.join(lines) + "\n"
    text_node = TextNode(clean_block, TextType.CODE_TEXT)
    return text_node_to_html_node(text_node)

def quote_to_html_node(block: str) -> HTMLNode:
    children_nodes = text_to_children_nodes(block, BlockType.QUOTE)
    parent_node = ParentNode("blockquote", children_nodes)
    return parent_node

def u_list_to_html_node(block: str) -> HTMLNode:
    children_nodes = text_to_children_nodes(block, BlockType.UNORDERED_LIST)
    parent_node = ParentNode("ul", children_nodes)
    return parent_node

def o_list_to_html_node(block: str) -> HTMLNode:
    children_nodes = text_to_children_nodes(block, BlockType.ORDERED_LIST)
    for node in children_nodes:
        node.tag = "li"
    parent_node = ParentNode("ol", children_nodes)
    return parent_node

def text_to_children_nodes(block: str, block_type:BlockType) -> list[HTMLNode]:
    children_nodes = []

    lines = block.splitlines()

    match block_type:
        case BlockType.QUOTE:
            cleaned_lines = [line.strip()[2:] for line in lines]
            clean_nodes = lines_to_inline_nodes(cleaned_lines)
            children_nodes.extend(clean_nodes)
        case BlockType.UNORDERED_LIST:
            for x, line in enumerate(lines):
                grandchildren_nodes = []

                line = line.strip()
                lines[x] = line[2:]
                text_nodes = text_to_textnodes(lines[x])
                for text_node in text_nodes:
                    child_node = text_node_to_html_node(text_node)
                    grandchildren_nodes.append(child_node)

                children_nodes.append(ParentNode("li", grandchildren_nodes))
        case BlockType.ORDERED_LIST:
            for x, line in enumerate(lines):
                grandchildren_nodes = []

                line = line.strip()
                lines[x] = line[3:]
                text_nodes = text_to_textnodes(lines[x])
                for text_node in text_nodes:
                    child_node = text_node_to_html_node(text_node)
                    grandchildren_nodes.append(child_node)

                children_nodes.append(ParentNode("li", grandchildren_nodes))
        case _:
            cleaned_lines = [line.strip() for line in lines]
            clean_nodes = lines_to_inline_nodes(cleaned_lines)
            children_nodes.extend(clean_nodes)

    return children_nodes

def lines_to_inline_nodes(lines: list[str]) -> list[HTMLNode]:
    node_list = []

    clean_block = " ".join(lines).strip("\n")
    text_nodes = text_to_textnodes(clean_block)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        node_list.append(html_node)

    return node_list

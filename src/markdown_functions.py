import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

HEADING_RE = re.compile(r"^(#{1,6})\s+.+$")

def markdown_to_blocks(markdown: str) -> list[str]:
    block_of_lines = markdown.strip().split("\n\n")
    clean_block = []
    for x in range(len(block_of_lines)):
        block_of_lines[x] = block_of_lines[x].strip()
        if block_of_lines[x] != "":
            clean_block.append(block_of_lines[x])

    return clean_block

def block_to_block_type(markdown_block: str) -> BlockType:
    if HEADING_RE.match(markdown_block):
        return BlockType.HEADING

    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE

    # Other blocks are line-by-line
    markdown_lines = markdown_block.split("\n")

    is_quote_block = True
    for line in markdown_lines:
        if not line.startswith("> "):
            is_quote_block = False
            break
    if is_quote_block:
        return BlockType.QUOTE

    is_unordered_list = True
    for line in markdown_lines:
        if not line.startswith("- "):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for x in range(len(markdown_lines)):
        if not markdown_lines[x].startswith(str(x + 1) + ". "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

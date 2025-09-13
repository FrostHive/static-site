class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        full_string = ""
        if(self.props):
            for prop in self.props:
                full_string += f" {prop}={self.props[prop]}"
        return full_string

class LeafNode(HTMLNode):

    def __init__(self, tag: str, value: str, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError(f"{self} has no value.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError(f"{self} doesn't have a tag.")
        if not self.children:
            raise ValueError(f"{self} is a ParentNode, but its children variable doesn't exist.")
        else:
            complete_str = ""
            for node in self.children:
                complete_str += node.to_html()
            return f"<{self.tag}>{complete_str}</{self.tag}>"

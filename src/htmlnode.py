class HTMLNode:
    def __init__(self, tag: str | None = None, 
                 value: str | None = None, 
                 children: list | None = None, 
                 props: dict[str, str] | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html()")

    def props_to_html(self) -> str:
        if self.props is None or self.props is {}:
            return ""
        formatted = ""
        for prop in self.props:
            formatted += f' {prop}="{self.props[prop]}"'
        return formatted

    def __repr__(self) -> str:
        repr = ""
        if self.tag != None:
            repr += f"tag: {self.tag}"
        if self.value != None:
            repr += f"value: {self.value}"
        if self.children != None:
            repr += f"children: {self.children}"
        if self.props != None:
            repr += f"props: {self.props}"
        return repr



from dataclasses import dataclass
from typing import Any

@dataclass
class Entry:
    prefix: str | None
    title: str
    lines: list[str]
    url: str | None
    ldistance: int

    def new():
        return Entry(
            prefix = '',
            title = '',
            lines = [],
            url = None,
            ldistance = 0
        )

    def display(self) -> str:
        return [
            self.title if self.prefix is None else f"{self.prefix}.{self.title}",
            ''.join(self.lines)
        ]
    
    def with_attr(self, attr_name: str, value: Any):
        copy = self
        setattr(copy, attr_name, value)
        return copy

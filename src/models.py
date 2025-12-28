from dataclasses import dataclass, asdict

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int

    def to_dict(self) -> dict:
        return asdict(self)

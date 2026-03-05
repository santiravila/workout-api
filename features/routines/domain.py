from typing import Self


class Routine:
    def __init__(self, name: str, id: int | None = None):
        self.id = id
        self.name = name

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}    
from dataclasses import asdict

from appdemo.modules.content import AvailableLanguage
from pydantic import Field, RootModel
from pydantic.dataclasses import dataclass


@dataclass
class Chunk:
    id: str
    page_number: int
    text: str
    language: AvailableLanguage
    x: int | float
    y: int | float
    w: int | float
    h: int | float


class Chunks(RootModel):
    root: list[Chunk] = Field(default_factory=list)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __dict__(self):
        return list(map(asdict, self.root))

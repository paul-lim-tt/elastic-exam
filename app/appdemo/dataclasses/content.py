
from pydantic import BaseModel, Field

type number = int | float
POLYGON_LENGTH = 8

class _BoundingRegion(BaseModel):
    pageNumber: int
    polygon: list[number] = Field(
        ..., min_length=POLYGON_LENGTH, max_length=POLYGON_LENGTH
    )


class _Page(BaseModel):
    pageNumber: int
    width: number
    height: number
    unit: str



class _Paragraph(BaseModel):
    content: str
    boundingRegions: list[_BoundingRegion]


class ExtractedContent(BaseModel):

    pages: list[_Page]
    paragraphs: list[_Paragraph]
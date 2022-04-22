from decimal import Decimal
from typing import List,Optional
from pydantic import BaseModel


class Artist(BaseModel):
    id: int
    name: str


class Chapter(BaseModel):
    id: Decimal
    slug: str
    name: str
    number: str
    volume: int
    manga_id: int


class Category(BaseModel):
    id: int
    name: str
    slug: str
    
    @property
    def index(self):
        return int(self.slug)

class Status(BaseModel):
    id: int
    label: str


class AnimeManga(BaseModel):
    id: int
    name: str
    slug: str
    status_id: int
    other_names: Optional[str]
    summary: str
    cover: str
    caution: int
    views: int
    type_id: int = None  # type: ignore
    authors: List[Artist]
    artists:Optional[List[Artist]] 
    status: Optional[Status]
    type: Optional[Status]
    categories: List[Category]
    chapters:Optional[List[Chapter]]


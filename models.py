from pydantic import BaseModel
from typing import List, Optional

class Movie(BaseModel):
    title: str
    plot: Optional[str]
    genres: Optional[List[str]]
    runtime: Optional[int]
    cast: Optional[List[str]]
    directors: Optional[List[str]]
    year: Optional[int]

class UpdateMovie(BaseModel):
    plot: Optional[str]
    genres: Optional[List[str]]
    runtime: Optional[int]
    cast: Optional[List[str]]
    directors: Optional[List[str]]
    year: Optional[int]


class Neo4jMovie(BaseModel):
    identity: int
    title: str
    tagline: Optional[str]
    released: int
    elementId: str
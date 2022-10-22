from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class MoviesStructure(BaseModel):
    id: UUID
    imdb_rating: float = None
    genre: list = []
    title: str
    description: Optional[str] = None
    director: list = None
    actors_names: list = None
    writers_names: list = None
    actors: list = None
    writers: list = None
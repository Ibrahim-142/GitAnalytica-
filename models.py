from pydantic import BaseModel
from typing import Dict, List, Any


class ProfileResponse(BaseModel):
    username: str
    name: str | None
    bio: str | None
    followers: int
    following: int
    public_repos: int

    total_stars: int
    languages: Dict[str, int]

    top_repos: List[Any]
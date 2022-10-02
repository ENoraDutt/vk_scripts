from typing import List, Dict

from pydantic import BaseModel


class VkPost(BaseModel):
    id: int
    owner_id: int
    from_id: int
    text: str
    comms: List[Dict]
    likes: List[int]

    class Config:
        extra = "allow"

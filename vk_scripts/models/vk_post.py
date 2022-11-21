from typing import List, Dict

from pydantic import BaseModel


class VkPost(BaseModel):
    post: Dict
    comms: List[Dict] = None
    likes: List[int] = None

    class Config:
        extra = "allow"

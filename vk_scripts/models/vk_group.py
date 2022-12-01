from typing import List, Dict

from pydantic import BaseModel

from enums import GroupTypeEnum


class VkGroupInfo(BaseModel):
    """ Модель группы/паблика/страницы """
    type: GroupTypeEnum
    name: str
    screen_name: str
    id: str

    class Config:
        extra = "allow"


class VkGroup(BaseModel):
    group: VkGroupInfo
    members: List[int]

    @classmethod
    def build(cls, data: Dict):
        return cls(
            group_info=VkGroupInfo(**data["group"]),
            members=data["members"],
        )

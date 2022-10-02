from typing import List

from pydantic import BaseModel

from enums import GroupTypeEnum


class Group(BaseModel):
    """ Модель группы/паблика/страницы """
    type: GroupTypeEnum
    short_name: str
    vk_id: str
    people_active_exchange: List[str]
    url: str


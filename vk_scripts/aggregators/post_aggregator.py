from typing import List, Callable

from vk_scripts.vk_client import VkClient


class PostAggregator:
    """Получает данные по постам и передает их в sender"""

    def __init__(self, vk_client: VkClient, sender: Callable):
        self.client = vk_client
        self.sender = sender

    def aggregate(self, groups: List[str]):
        data = self.client.get_posts_from_groups(groups)
        self.sender(data)

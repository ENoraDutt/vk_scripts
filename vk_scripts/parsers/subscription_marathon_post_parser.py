import pandas as pd

from vk_scripts.vk_client import VkClient


class SubscriptionMarathonPostParser():

    def __init__(self, vk_client: VkClient):
        self._vk_client = vk_client
        self._data_writer = None  # some writer с интерфейсом write data

    def parse_post_vk(self, link: str) -> pd.DataFrame:
        post = self._vk_client.get_post(link)

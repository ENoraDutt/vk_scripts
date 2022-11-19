import pandas as pd

from vk_scripts.vk_client import VkClient


class SubscriptionMarathonPostParser:
    LINK_RE = r"@\w{1,}"

    def __init__(self, vk_client: VkClient):
        self._vk_client = vk_client
        self._data_writer = None  # some writer с интерфейсом write data

    def parse_post_vk(self, link: str) -> pd.DataFrame:
        post = self._vk_client.get_post(link)
        pass

    def _parse_text(self, text: str):
        """ Парсить текст и вытаскивать оттуда ссылки + имена если есть (не обязательно, конечно, но наверное можно через vk client)"""
        pass

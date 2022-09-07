from typing import List
from urllib.parse import urljoin

import requests
from retry import retry

from exceptions import InvalidAccessToken
from models import Group
from vk_exceptions_screamer import VkExceptionsScreamer


class VkClient:
    """ Класс для получения данных из vk api"""

    def __init__(self, screamer: VkExceptionsScreamer, url: str, token: str, version: int):
        self.params = {"access_token": token, "v": version}
        self.screamer = screamer
        self._token = token
        self._version = version
        self._url = url

    def __enter__(self):
        self._check_access_token()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("EXIT")
        pass

    @retry(InvalidAccessToken, tries=2, delay=1)
    def _check_access_token(self):
        """ Проверка токена """

        response = requests.get(urljoin(self._url, "wall", allow_fragments=True), params=self.params)
        self.screamer.verify(response)

    @retry(Exception, tries=2, delay=5)
    def get_notify(self, mine: List[str], groups: List[Group]):
        """ Получить все посты из указанных групп """
        pass

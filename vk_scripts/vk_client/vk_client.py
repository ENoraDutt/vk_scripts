from typing import List, Dict
from urllib.parse import urljoin, urlparse

import requests
from retry import retry

from exceptions import InvalidAccessToken
from vk_exceptions_screamer import VkExceptionsScreamer
from vk_scripts.models import Group, VkPost


class VkClient:
    """
    Класс для получения данных из vk api
    :param screamer: экземпляр класса, проверяющего responses vk api на наличие ошибок
    :param url: url vk api для задокументированных методов
    :param token: access_token приложения для работы с vk api (см. https://dev.vk.com/api/access-token/getting-started) 
    :param version: версия vk api
    """

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

    def vk_request(self, join: str, params: Dict):
        """ 
        Выполняет request и проверяет response на наличие ошибок 
        Пояснение: ошибки записываются в text, но status_code 200 
        """
        response = requests.get(urljoin(self._url, join), params=params)
        self.screamer.verify(response)
        return response

    @retry(InvalidAccessToken, tries=2, delay=1)
    def _check_access_token(self):
        """ Проверка токена """

        response = self.vk_request(join="wall", params=self.params)
        self.screamer.verify(response)

    @retry(Exception, tries=2, delay=5)
    def get_notify(self, groups: List[Group], limit: int = 10) -> List[VkPost]:
        """ 
        Получить все посты из указанных групп
        :param groups: список групп, в которых будут проверять посты
        :param limit: количество постов, которые будут получены из каждой группы
        """
        all_groups = ",".join([f'{g.short_name}' for g in groups])
        execute_params = self.params.copy()
        execute_params["groups"] = all_groups
        execute_params["limit_posts"] = limit
        response = self.vk_request(join="execute.getGroupsPosts", params=execute_params)
        posts = [VkPost(**post) for post in response.json()["response"]["result"]]
        return posts
        
    @retry(Exception, tries=2, delay=5)
    def get_post(self, link: str):
        """
        Получает пост по ссылке
        """
        data = urlparse(link)
        print(data)
        # распарсить ссылку, получить данные

        
        

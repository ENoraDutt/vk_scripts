import re
from typing import List, Dict
from urllib.parse import urljoin

import requests
from retry import retry

from exceptions import InvalidAccessToken, IncorrectLink
from vk_exceptions_screamer import VkExceptionsScreamer
from vk_scripts.models import VkPost, VkGroup


class VkClient:
    """
    Класс для получения данных из vk api
    :param screamer: экземпляр класса, проверяющего responses vk api на наличие ошибок
    :param url: url vk api для задокументированных методов
    :param token: access_token приложения для работы с vk api (см. https://dev.vk.com/api/access-token/getting-started) 
    :param version: версия vk api
    """

    def __init__(self, screamer: VkExceptionsScreamer, url: str, token: str, version: str):
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

    def vk_request(self, join: str, params: Dict = {}):
        """ 
        Выполняет request и проверяет response на наличие ошибок 
        Пояснение: ошибки записываются в text, но status_code 200 
        """
        if not params:
            params = self.params
        response = requests.get(urljoin(self._url, join), params=params)
        self.screamer.verify(response)
        return response

    @retry(InvalidAccessToken, tries=2, delay=1)
    def _check_access_token(self):
        """ Проверка токена """

        response = self.vk_request(join="wall", params=self.params)
        self.screamer.verify(response)

    @retry(Exception, tries=2, delay=5)
    def get_posts_from_groups(self, groups: List[str], limit: int = 10) -> List[VkPost]:
        """ 
        Получить все посты из указанных групп (execute.getGroupsPosts)
        :param groups: список групп, в которых будут проверять посты (short names)
        :param limit: количество постов, которые будут получены из каждой группы
        """
        execute_params = self.params.copy()
        execute_params["groups"] = ",".join(groups)
        execute_params["limit_posts"] = limit
        response = self.vk_request(join="execute.getGroupsPosts", params=execute_params)
        posts = [VkPost(**post) for post in response.json()["response"]["result"]]
        return posts

    @retry(Exception, tries=2, delay=5)
    def get_post(self, link: str) -> VkPost:
        """
        Получает пост по ссылке
        :param link: ссылка на пост
        """
        post_id_regex = r"wall(-\d{1,}_\d{1,})"
        post_id_list = re.findall(post_id_regex, link)
        if post_id_list.__len__() != 1:
            raise IncorrectLink("Post_id not parsed from link (url)")
        get_by_id_param = self.params.copy()
        get_by_id_param["posts"] = post_id_list[0]
        post = self.vk_request(join="wall.getById", params=get_by_id_param).json()["response"]["items"][0]
        return VkPost(**post)

    @retry(Exception, tries=2, delay=5)
    def get_title_by_at(self, at: str):
        """ Получает имя по упомниманию через @ """
        pass

    @retry(Exception, tries=2, delay=5)
    def get_groups(self) -> List[int]:
        """ Получает идентификаторы групп пользователя """
        groups = self.vk_request(join="groups.get").json()["response"]["items"]
        return groups

    @retry(Exception, tries=2, delay=5)
    def get_groups_info(self, groups_id: List[int]):
        """ Получает информацию о группам (в том числе пользователей) по id групп """

        get_groups_param = self.params.copy()
        get_groups_param["groups"] = ",".join([str(g) for g in groups_id])
        groups = self.vk_request(join="execute.getGroupsInfo", params=get_groups_param).json()["response"]["result"]
        return [VkGroup(**g) for g in groups]

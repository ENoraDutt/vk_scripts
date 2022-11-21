from vk_exceptions_screamer import VkExceptionsScreamer
from vk_scripts.models import VkPost
from vk_scripts.parsers.subscription_marathon_post_parser import SubscriptionMarathonPostParser
from vk_scripts.vk_client import VkClient

text = """
@rosinatalia - Наталья Спехова - редактор, автор детской литературы, нон-фикшн; член Союза писателей. Советы для писателей в группе https://vk.com/kak_napisat_knigu
@eleonoragilm - Элеонора Гильм, автор исторической прозы (Эксмо), организатор книжных движей. О творчестве в группе https://vk.com/genskajasaga
@oksana_trivedi_books
(Оксана Триведи), писатель, журналист (современная проза, Young Adult).
@fantasysnezhko (Татьяна Снежко), писатель-фантаст, журналист, автор мифологической трилогии "Заложница Шумера"
"""
import pytest


@pytest.fixture(scope="function")
def vk_post_mock():
    return VkPost(
        post={},
        id="123",
        owner_id="123",
        from_id="234",
        text="",
    )


@pytest.fixture(scope="function")
def vk_client():
    return VkClient(
        screamer=VkExceptionsScreamer(),
        url="https://api.vk.com/method/",
        token="vk1.a",
        version="5.1312",
    )


def test_parse_post_vk__parse_post_vk(mocker, vk_client, vk_post_mock):
    """ Тестирование парсинга поста с нормальными данными"""
    vk_post_mock.text = """@rosinatalia (Наталья Спехова)"""
    mocker.patch.object(vk_client, "get_post", return_value=vk_post_mock)
    parser = SubscriptionMarathonPostParser(vk_client)

    result = parser.parse_post_vk(link="some_correct_link")
    pass


def test_parse_post_vk__parse_link(mocker, vk_client, vk_post_mock):
    """ Тестирование парсинга поста с нормальными данными"""
    vk_post_mock.text = """
@rosinatalia - Наталья Спехова - редактор, автор детской литературы, нон-фикшн; член Союза писателей. Советы для писателей в группе https://vk.com/kak_napisat_knigu
@eleonoragilm - Элеонора Гильм, автор исторической прозы (Эксмо), организатор книжных движей. О творчестве в группе https://vk.com/genskajasaga
@oksana_trivedi_books
(Оксана Триведи), писатель, журналист (современная проза, Young Adult).
@fantasysnezhko (Татьяна Снежко), писатель-фантаст, журналист, автор мифологической трилогии "Заложница Шумера"
"""
    mocker.patch.object(vk_client, "get_post", return_value=vk_post_mock)
    parser = SubscriptionMarathonPostParser(vk_client)

    result = parser.parse_post_vk(link="some_correct_link")
    pass


def test_parse_post_vk__parse_link__doublecated_data():
    """ Тестирование парсинга поста с нормальными данными"""


def test_parse_post_vk__parse_link__empty_text():
    """ Тестирование парсинга поста с нормальными данными"""

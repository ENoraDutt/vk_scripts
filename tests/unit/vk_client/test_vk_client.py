import pytest

from vk_exceptions_screamer import VkExceptionsScreamer
from vk_scripts.models import VkPost
from vk_scripts.vk_client import VkClient


@pytest.fixture(scope="function")
def mock_response(mocker):
    mock_response = mocker.MagicMock()
    post_data = {
        "post": {},
        "likes": [123, 456, 789],
        "posts": "POST",
    }
    mock_response.json.return_value = {"response": {
        "result": [post_data],
        "items": [post_data]
    }}

    return mock_response


@pytest.fixture(scope="function")
def vk_client():
    client = VkClient(
        screamer=VkExceptionsScreamer(),
        url="https://api.vk.com/method/",
        token="vk1.a",
        version="5.1312",
    )
    return client


def test_vk_client__get_posts_from_groups(mocker, vk_client, mock_response):
    """ Проверяет получение постов"""

    mocker.patch.object(vk_client, "vk_request", return_value=mock_response)

    result = vk_client.get_posts_from_groups(groups=["123"])

    vk_client.vk_request.assert_called_once_with(
        join="execute.getGroupsPosts",
        params={
            'access_token': 'vk1.a',
            'groups': '123',
            'limit_posts': 10,
            'v': '5.1312',
        }
    )
    assert isinstance(result[0], VkPost)
    assert result[0].posts == "POST"


@pytest.mark.parametrize("link, result", [
    ("https://vk.com/wall-1_340364", "-1_340364"),
    ("https://vk.com/apiclub?w=wall-1_340364", "-1_340364"),
    ("https://vk.com/apiclub?w=wall-1_340364%2Fall", "-1_340364"),
])
def test_vk_client__get_post__normal_data(mocker, link, result, vk_client, mock_response):
    """ Проверяет получение поста по ссылке """
    mocker.patch.object(vk_client, "vk_request", return_value=mock_response)

    post = vk_client.get_post(link)

    assert isinstance(post, VkPost)
    vk_client.vk_request.assert_called_once_with(
        join="wall.getById",
        params={
            "access_token": "vk1.a",
            "v": "5.1312",
            "posts": result
        })


@pytest.mark.parametrize("link", [
    ("https://vk.com/wall-1_122245455")
])
def test_vk_client__get_post__post_not_found(link):
    """ Проверяет обработку несуществующего поста """
    pass


@pytest.mark.parametrize("link", [
    ("some_fake_urlwall-1_340364")
])
def test_vk_client__get_post__incorrect_link(link):
    """ Проверяет обработку несуществующего поста """
    pass


def test_remove_tests():
    client = VkClient(
        screamer=VkExceptionsScreamer(),
        url="https://api.vk.com/method/",
        token="vk1.a.-ntlSVC143lcQscYYFJ4-FR3TXy_1D9MelauJOCzJ9jtRTYkGZ8h7sJHcBg9jaSWRGU8x9p_ReDd82c6Dzhtlp9HEwcatO-6r96oMlR1ATq35pfhFJ9qYLWjDzwZP1fVusG6ybuwoSehu2q9lQA806WOE-nmk23XkggXmK2FsEOX2ubxlNSNy84X7NatC2o8",
        version="5.1312",
    )
    result = client.get_posts_from_groups(groups=["digridian_gold"])
    pass

import pytest

from vk_exceptions_screamer import VkExceptionsScreamer
from vk_scripts.models import Group, VkPost
from vk_scripts.vk_client import VkClient


@pytest.fixture(scope="function")
def mock_response(mocker):
    mock_response = mocker.MagicMock()
    post_data = {
        "id": 23,
        "owner_id": 23,
        "from_id": 23,
        "text": "text_data",
        "comms": [],
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


def test_vk_client__get_notify(mocker, vk_client, mock_response):
    """ Проверяет получение постов"""

    groups = [Group(
        type="group",
        short_name="public_tasha_alx",
        vk_id="123",
        people_active_exchange=["some_id"],
        url="https://vk.com/public_tasha_alx",
    )]
    mocker.patch.object(vk_client, "vk_request", return_value=mock_response)

    result = vk_client.get_notify(groups=groups)

    vk_client.vk_request.assert_called_once_with(
        join="execute.getGroupsPosts",
        params={
            'access_token': 'vk1.a',
            'groups': 'public_tasha_alx',
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

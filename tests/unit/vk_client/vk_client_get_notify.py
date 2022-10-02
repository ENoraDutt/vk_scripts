import pytest

from vk_exceptions_screamer import VkExceptionsScreamer
from vk_scripts.models import Group, VkPost
from vk_scripts.vk_client import VkClient


@pytest.fixture(scope="function")
def mock_response(mocker):
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {"response": {"result": [{
        "id": 23,
        "owner_id": 23,
        "from_id": 23,
        "text": "text_data",
        "comms": [],
        "likes": [123, 456, 789],
        "posts": "POST",
    }]}}

    return mock_response


def test_vk_client__get_notify(mocker, mock_response):
    """ Проверяет получение постов"""

    groups = [Group(
            type="group",
            short_name="public_tasha_alx",
            vk_id="123",
            people_active_exchange=["some_id"],
            url="https://vk.com/public_tasha_alx",
        )]
    vk_client = VkClient(
        screamer=VkExceptionsScreamer(),
        url="https://api.vk.com/method/",
        token="vk1.a",
        version="5.1312",
    )
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

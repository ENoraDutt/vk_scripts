import pytest

from exceptions import InvalidAccessToken
from vk_exceptions_screamer import VkExceptionsScreamer


@pytest.fixture(scope="function")
def response_mock_obj(mocker):
    response = mocker.MagicMock()
    response.status_code = 200
    response.ok = True
    return response


INVALID_ACCESS_TOKEN_TEXT = """{"error":{"error_code":5,"error_msg":"User authorization failed: invalid access_token (4).","request_params":[{"key":"posts","value":""},{"key":"copy_history_depth","value":""},{"key":"v","value":"5.1312"},{"key":"method","value":"wall.getById"},{"key":"oauth","value":"1"}]}}
"""


@pytest.mark.parametrize("text, wait_exception", [
    (INVALID_ACCESS_TOKEN_TEXT, InvalidAccessToken),
])
def test_vk_exception_screamer_verify(response_mock_obj, text, wait_exception):
    """ Проверяет работу скримера для responce vk api """

    response_mock_obj.text = text
    screamer = VkExceptionsScreamer()

    with pytest.raises(wait_exception) as test_scream:
        screamer.verify(response_mock_obj)

from vk_exceptions_screamer import VkExceptionsScreamer
from vk_scripts.models import Group
from vk_scripts.vk_client import VkClient


def test_vk_client__get_notify(mocker):
    """ Проверяет получение свежих постов без активности по списку групп """

    groups = [
        Group(
            type="group",
            short_name="public_tasha_alx",
            vk_id="123",
            people_active_exchange=["some_id"],
            url="https://vk.com/public_tasha_alx",
        )
    ]

    vk_client = VkClient(
        screamer=VkExceptionsScreamer(),
        url="https://api.vk.com/method/",
        token="vk1.a",
        version="5.1312",
    )
    result = vk_client.get_notify(groups=groups)

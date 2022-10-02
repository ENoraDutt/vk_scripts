from requests import Response, RequestException

from exceptions import InvalidAccessToken, UnknownMethodPassed


class VkExceptionsScreamer:
    """
    Класс для проверки ответа vk api
    Пример: code 200, но auth error (не валидный токен)
    """
    EXCEPTIONS: Exception = [
        InvalidAccessToken,
        UnknownMethodPassed,
    ]

    @classmethod
    def verify(cls, response: Response):
        if not response.ok:
            raise RequestException
        for exception in cls.EXCEPTIONS:
            if exception.check_response(response):
                raise exception

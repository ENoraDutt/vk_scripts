from requests import Response


class InvalidAccessToken(Exception):
    BASE_MESSAGE = "User authorization failed: invalid access_token. "
    HELP_MESSAGE = "Check use time access token. "

    def __init__(self, message: str = ""):
        self._message = message

    def __str__(self):
        return f"{self.BASE_MESSAGE}\n{self.HELP_MESSAGE}{self._message}"

    @staticmethod
    def check_response(response: Response):
        if "User authorization failed: invalid access_token" in response.text:
            return True
        return False

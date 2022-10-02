from requests import Response


class UnknownMethodPassed(Exception):
    BASE_MESSAGE = "Unknown method passed: function not found"
    HELP_MESSAGE = "Check method or execute function"

    def __init__(self, message: str = ""):
        self._message = message

    def __str__(self):
        return f"{self.BASE_MESSAGE}\n{self.HELP_MESSAGE}{self._message}"

    @staticmethod
    def check_response(response: Response):
        if "Unknown method passed: function not found" in response.text:
            return True
        return False

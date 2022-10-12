class IncorrectLink(Exception):

    def __init__(self, message: str):
        self._message = message

    def __str__(self):
        return f"{self._message}"

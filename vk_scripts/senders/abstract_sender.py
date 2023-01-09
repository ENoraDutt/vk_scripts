from abc import ABC


class AbstractSender(ABC):
    def __call__(self):
        raise NotImplementedError

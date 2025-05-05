from abc import ABC, abstractmethod


class Member(ABC):
    @abstractmethod
    def update(self, message):
        pass

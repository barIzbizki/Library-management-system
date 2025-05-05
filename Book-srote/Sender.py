from abc import ABC, abstractmethod


class Sender(ABC):
    def __init__(self):
        self.registered = []

    def register(self, user):
        self.registered.append(user)

    def unregister(self, user):
        self.registered.remove(user)

    def notify_members(self, message):
        for user in self.registered:
            user.update(message)



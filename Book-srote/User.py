
from Member import Member


class User (Member):
    def __init__(self, user_name, hash_password):

        self.user_name = user_name
        self.hash_password = hash_password
        self.gui = None

    def update(self, message):
        pass


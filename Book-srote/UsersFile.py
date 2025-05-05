import pandas as pd
from User import User


class UserFile:
    file_path = "users.csv"

    @staticmethod
    def load_users():
        users = []
        df = pd.read_csv(UserFile.file_path)

        for index, row in df.iterrows():
            username = row["user_name"]
            password_hash = row["password_hash"]
            user = User(username, password_hash)
            users.append(user)

        return users

    @staticmethod
    def save_new_user(username, password_hash):
        try:
            df = pd.read_csv(UserFile.file_path)

            new_row = {"user_name": username, "password_hash": password_hash}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            df.to_csv("users.csv", index=False)
            print(f"SUCCESS: User '{username}' added successfully.")

        except Exception as e:
            print(f"ERROR: {e}")


import pandas as pd


class Book:
    def __init__(self, title, author, is_loaned, copies, genre, year):
        self.title = title
        self.author = author
        self.copies = copies
        self.genre = genre
        self.year = year
        self.is_loaned = is_loaned
        self.waiting_list = []
        self.popular = 0

    def to_dict(self):

        if isinstance(self.waiting_list, str):
            self.waiting_list = self.waiting_list.split(",")

        cleaned_waiting_list = [phone.strip() for phone in self.waiting_list if phone.strip()]

        return {
            "title": self.title,
            "author": self.author,
            "is_loaned": self.is_loaned,
            "copies": self.copies,
            "genre": self.genre,
            "year": self.year,
            "popular": self.popular,
            "waiting_list": ",".join(cleaned_waiting_list)
        }

    def add_to_waitinglist(self, phone_number):
        phone_number_to_add = str(phone_number) + ','
        self.waiting_list.append(phone_number_to_add)

    def remove_from_waitinglist(self, phone_number):
        self.waiting_list.remove(phone_number)

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False

    def __hash__(self):
        return hash((self.title, self.author))

    def __str__(self):
        print(f"{self.title} and {self.author}")

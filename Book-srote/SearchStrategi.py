from abc import ABC, abstractmethod


class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books, query):
        pass


class TitleSearchStrategy(SearchStrategy):
    def search(self, books, query):
        results = [book for book in books if query.lower() in book.title.lower()]
        return results if results else "not found"


class AuthorSearchStrategy(SearchStrategy):
    def search(self, books, query):
        results = [book for book in books if query.lower() in book.author.lower()]
        return results if results else "not found."


class GenreSearchStrategy(SearchStrategy):
    def search(self, books, query):
        results = [book for book in books if query.lower() in book.genre.lower()]
        return results if results else "not found"

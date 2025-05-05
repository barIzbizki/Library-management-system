class LibraryIterator:
    def __init__(self, books):
        self.books = books
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.books):
            book = self.books[self.index]
            self.index += 1
            return book
        raise StopIteration

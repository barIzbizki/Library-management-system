import pandas as pd

from Book import Book


class BookFactory:
    @staticmethod
    def create_book(books, title, author, is_loaned, copies, genre, year, waiting_list=None, popular=0):
        # Check if the book already exists
        for b in books:
            if b.title == title:
                b.copies += copies
                BookFactory.update_book_copies(b)
                return  # Exit if the book already exists and has been updated
        # If the book doesn't exist, create a new one
        new_book = Book(title, author, is_loaned, copies, genre, year)
        # Add waiting list if provided
        if waiting_list is not None:
            # Assuming the waiting list is a comma-separated string
            if isinstance(waiting_list, str):
                new_book.waiting_list = waiting_list.split(",")
            else:
                new_book.waiting_list = waiting_list
        if popular != 0:
            new_book.popular = popular
        books.append(new_book)
        return new_book

    @staticmethod
    def update_book_copies(book):
        try:
            df = pd.read_csv("books.csv")
            book_index = df[(df["title"] == book.title)].index
            if not book_index.empty:
                df.loc[book_index, "copies"] = book.copies
                df.to_csv("books.csv", index=False)
                print(f"SUCCESS: Updated copies for book {book.title} to {book.copies}.")
            else:
                print(f"ERROR: Book {book.title} by {book.author} not found in {'books.csv'}.")
        except FileNotFoundError:
            print(f"ERROR: File '{'books.csv'}' not found.")
        except Exception as e:
            print(f"ERROR: Failed to update copies: {e}")




import hashlib
from functools import wraps
from BookFactory import BookFactory
from User import User
from BooksFile import BooksFile
from UsersFile import UserFile
from LoanedFile import LoanedFile
from AvailableFile import AvailableFile
from LibraryIterator import LibraryIterator
from Sender import Sender
from Logger import Logger
from SearchStrategi import GenreSearchStrategy
from Book import Book


class Library(Sender):

    def __init__(self):
        super().__init__()
        self.books = BooksFile.load_books_from_file()
        self.bookLoaned = LoanedFile.load_listL_from_file()
        self.bookAvailable = AvailableFile.load_listA_from_file()
        self.users = UserFile.load_users()
        self.logger = Logger()

    @staticmethod
    def log_action(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            action_messages = {
                "add_book": ("book added successfully", "book add failed"),
                "remove_book": ("book removed successfully", "book removed failed"),
                "loan_book": ("book borrowed successfully", "book borrow failed"),
                "return_book": ("book returned successfully", "book returned failed"),
                "log_in": ("logged in successfully", "log in failed"),
                "sign_in": ("registered successfully", "registration failed"),
                "log_out": ("log out successful", "log out failed"),
                "search_book": ("Search completed successfully", "Search failed"),
                "get_all_books": ("Displayed all books successfully", "Display all books failed"),
                "get_available_books": ("Displayed available books successfully", "Display available books failed"),
                "get_books_sorted_by_genre": ("Displayed by category successfully", "Display failed"),
                "get_loaned_books": ("Displayed borrowed books successfully", "Display borrowed books failed"),
                "get_top_10_popular_books": ("displayed successfully", "display failed"),
            }

            try:
                # Execute the function
                result = func(self, *args, **kwargs)
                action = func.__name__
                success_message, fail_message = action_messages.get(action, ("Action succeeded", "Action failed"))

                # Customize log message for search_book
                if action == "search_book" and args:
                    strategy = args[0]
                    to_check = args[1]

                    if not result:
                        log_message = f"Search book '{to_check}' by {type(strategy).__name__} failed"
                        self.logger.log_error(log_message)
                    else:
                        log_message = f"Search book '{to_check}' by {type(strategy).__name__} completed successfully"
                        self.logger.log_info(log_message)
                else:
                    # Generic handling for other actions
                    if isinstance(result, str) and ("failed" in result.lower() or "no" in result.lower()):
                        log_message = f"{fail_message}"
                        self.logger.log_error(log_message)
                    else:
                        log_message = success_message
                        self.logger.log_info(log_message)

                return result

            except Exception as e:
                # Log the error in case of an exception
                action = func.__name__
                _, fail_message = action_messages.get(action, ("Action succeeded", "Action failed"))
                error_message = f"{fail_message}: {e}"
                self.logger.log_error(error_message)
                raise

        return wrapper

    @log_action
    def add_book(self, title, author, is_loaned, copies, genre, year):
        book = BookFactory.create_book(self.books, title, author, is_loaned, copies, genre, year)
        if book is not None:
            BooksFile.update_books_file(book)
            if is_loaned == "No":
                self.bookAvailable[title] = 0
                AvailableFile.add_row_to_av(title, 0)
            else:
                self.bookLoaned.append(title)
                LoanedFile.add_book_to_loaned(title)
        else:
            target_book = Library.search_by_title(self.books, title)
            if target_book is not None:
                if is_loaned == "No":
                    if target_book.title in self.bookLoaned:
                        self.bookLoaned.remove(title)
                        LoanedFile.remove_row_by_title(title)
                        self.bookAvailable[title] = target_book.copies - copies
                        AvailableFile.add_row_to_av(title, target_book.copies - copies)
                        target_book.is_loaned = "No"
                        BooksFile.update_is_loaned(title, "No")
                        if target_book.waiting_list:
                            i = 0
                            while target_book.waiting_list is not [] and i < copies:
                                self.loan_book(title)
                                target_book.waiting_list.pop(0)
                                BooksFile.update_waiting_list(title, target_book.waiting_list)
                                i += 1
                elif is_loaned == "Yes":
                    if title in self.bookAvailable:
                        self.bookAvailable[title] += copies
                        if self.bookAvailable[title] == target_book.copies:
                            self.bookLoaned.append(title)
                            LoanedFile.add_book_to_loaned(title)
                            del self.bookAvailable[title]
                            AvailableFile.remove_row_by_title(title)
                        AvailableFile.update_count_available(title, self.bookAvailable[title])

        return "success"

    @log_action
    def remove_book(self, title):
        target_book = Library.search_by_title(self.books, title)
        if target_book is None:
            return " failed - not_in_library"
        if title in self.bookAvailable:
            if self.bookAvailable[title] == 0:
                del self.bookAvailable[title]
                AvailableFile.remove_row_by_title(title)
                BooksFile.remove_row_by_title(title)
                self.books.remove(target_book)
            else:
                target_book.copies = self.bookAvailable[title]
                BooksFile.update_number_copies(target_book.title, target_book.copies)
                if target_book.copies == self.bookAvailable[title]:
                    del self.bookAvailable[title]
                    AvailableFile.remove_row_by_title(title)
                    target_book.is_loaned = "Yes"
                    self.bookLoaned.append(title)
                    LoanedFile.add_book_to_loaned(title)
            return "success"
        if title in self.bookLoaned:
            return "failed - all the copies are loaned - cannot remove"
        return "success"

    @log_action
    def loan_book(self, title):
        target_book = Library.search_by_title(self.books, title)
        if target_book is None:
            return "failed - not_in_library"

        for t in self.bookLoaned:
            if title == t:
                return "failed - out_of_copies"
        if self.bookAvailable[title] < target_book.copies:
            self.bookAvailable[title] += 1
            AvailableFile.update_count_available(title, self.bookAvailable[title])

        if self.bookAvailable[title] == target_book.copies:
            AvailableFile.remove_row_by_title(title)
            del self.bookAvailable[title]
            LoanedFile.add_book_to_loaned(title)
            self.bookLoaned.append(title)
            target_book.is_loaned = "Yes"
            BooksFile.update_is_loaned(title, "Yes")
        target_book.popular += 1
        return "success"

    def add_to_waiting_list(self, title, phone_number):
        if phone_number.startswith("05") and len(phone_number) == 10 and phone_number.isdigit():
            b = Library.search_by_title(self.books, title)

            if b is None or not isinstance(b, Book):
                return "failed to add to the waiting list"

            if str(phone_number) not in b.waiting_list:
                b.add_to_waitinglist(str(phone_number))  #
                BooksFile.update_waiting_list(title, b.waiting_list)
                return "success"

            return "failed - you are already in the waiting list"
        else:
            return "failed - not a phone number"
    @log_action
    def return_book(self, title):
        target_book = Library.search_by_title(self.books, title)
        if target_book is None:
            return "failed - not_in_library"

        in_av = None
        for i in self.bookAvailable:
            if title == i:
                in_av = i
        if in_av is not None:
            if self.bookAvailable[title] > 0:
                self.bookAvailable[title] -= 1
                AvailableFile.update_count_available(title, self.bookAvailable[title])
            else:
                return "failed - not_in_library"

        else:
            if target_book.waiting_list:
                self.loan_book(title)
                number = target_book.waiting_list.pop(0)
                BooksFile.update_waiting_list(target_book.title, target_book.waiting_list)
                Library.notify_members(self, f"the book- {target_book.title} returned and {number} received the book")
                return "still not available"

            LoanedFile.remove_row_by_title(title)
            self.bookLoaned.remove(title)
            AvailableFile.add_row_to_av(title, target_book.copies - 1)
            self.bookAvailable[title] = target_book.copies - 1
            BooksFile.update_is_loaned(title, "No")
            Library.notify_members(self, f"the book- {target_book.title} is available")

        return "success"

    @log_action
    def sign_in(self, username, password):
        for user in self.users:
            if user.user_name == username:
                return "failed -User already exists."
        if username == "" or password == "":
            return "cannot be userename/password"
        h_password = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(username, h_password)
        self.users.append(new_user)
        UserFile.save_new_user(username, h_password)
        return "User signed up successfully!"

    @log_action
    def log_in(self, username, password, gui):
        for user in self.users:
            if user.user_name == username:
                password_h = hashlib.sha256(password.encode()).hexdigest()
                if user.hash_password == password_h:
                    Library.register(self, user)
                    user.gui = gui
                    return "Log in successful"
                else:
                    return "failed -Incorrect password"
        return "failed -User not found"

    @log_action
    def log_out(self, username, password):
        for user in self.users:
            if user.user_name == username:
                password_h = hashlib.sha256(password.encode()).hexdigest()
                if user.hash_password == password_h:
                    Library.unregister(self, user)
                    return "Log out successful"
        return "failed -User not found"

    @log_action
    def search_book(self, strategy, to_check):
        result = strategy.search(self.books, to_check)
        return result

    @log_action
    def get_available_books(self):
        return self.bookAvailable

    @log_action
    def get_loaned_books(self):
        return self.bookLoaned

    @log_action
    def get_all_books(self):
        return self.books

    @log_action
    def get_top_10_popular_books(self):
        books_with_popularity = [
            (book, book.popular + len(book.waiting_list)) for book in self.books
        ]
        top_10_books = sorted(books_with_popularity, key=lambda x: x[1], reverse=True)[:10]
        return top_10_books

    def register(self, user):
        self.registered.append(user)

    def unregister(self, user):
        self.registered.remove(user)

    def notify_members(self, message):
        for user in self.registered:
            try:
                if user.gui and user.gui.root.winfo_exists():
                    user.gui.root.after(0, lambda: user.gui.show_notification(message))
            except Exception as e:
                print(f"Error notifying {user.user_name}: {e}")

    @log_action
    def get_books_sorted_by_genre(self):
        strategy = GenreSearchStrategy()
        genre_dict = {}

        for book in self.books:
            genre = book.genre
            if genre not in genre_dict:
                genre_dict[genre] = strategy.search(self.books, genre)

        sorted_genres = sorted(genre_dict.keys())
        return {genre: genre_dict[genre] for genre in sorted_genres}

    @staticmethod
    def search_by_title(books, title_to_check):
        iterator = LibraryIterator(books)
        for book in iterator:
            if book.title.lower() == title_to_check.lower():
                return book
        return None




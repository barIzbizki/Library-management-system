# Library Management System

This is a Library Management System project built with Python. The system allows users to add, remove, search, loan, and return books. we have also  a waiting list for books that are currently loaned out.

## Design Patterns Used

1. **Factory**: 
   - Used in the `BookFactory` add a new book to the library, either by creating a new book because one like it did not exist before, or by adding it as a copy.
   
2. **Decorator**: 
   - Applied in the `log_action` decorator, which is used to wrap methods and log the actions of those methods before and after execution, providing additional functionality without modifying the original methods.
   
3. **Strategy**: 
   - Used in the `search_book` method and in `get_books_sorted_by_genre`, where different search strategies can be passed to dynamically change the way books are searched ( by title, author...).
   
4. **Iterator**: 
   - Used in the `LibraryIterator` class to iterate over the list of books. This pattern provides a way to access the elements of the books collection sequentially without exposing the underlying structure.
   
5. **Observer**: 
   - Implemented in the `notify_members` method, which notifies all registered users of events (such as book availability).The sender is the library and the subjects are the users.

## Options

- **Add book**: 
    - A new book can be added to the library – the action is done through a method to determine whether it is a copy or a new book.
- **Remove book**:
    - A book can be deleted by its title, and it will be removed entirely from the library's database (we can remove a book only if ak his copies are not loaned , if sum of then are loaned we will remove only the copies that not loaned).
- **Search book**:
    - You can search for a book in the library by categories.
- **Loaned book**:
    - By entering a title and phone number, you can loan a book. If all copies are loaned out, you will be added to the waiting list.
- **Return book**:
    - A book can be returned to the library by its title. If the book has a waiting list, it will go directly to the first person on the list (a notification will be sent to everyone).
- **View books**:
    - 3 options are available: viewing loaned books , viewing books available for loan and view bools by category.
- **View popular books**:
    - You can view the 10 most popular books in the library (i.e., the ones with the highest number of requests so far).
- **Log in**:
    - On the first screen, there will be an option to log in using a username and password (we used password encryption here).
- **Log out**:
    - You can log out and return to the login screen.
- **Sing in**:
    - You can register by providing a username and password, and your user will be saved in the system.
- **Back**:
    - After logging in, you always have the option to go back to the main screen.


## Assumptions
   - There are no different books in the library with the same title.
   - Communication with a person who is added to the waiting list is done through their phone number – each person has a unique and personal phone number.
   - Every user who registers in the system is "approved" as a librarian – there are no users who are not librarians.

## How to run the Library?

- To run the library you need to run the main class




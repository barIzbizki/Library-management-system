import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Label, Button
from Library import Library
from SearchStrategi import TitleSearchStrategy, AuthorSearchStrategy, GenreSearchStrategy


class LibraryGUI:
    def __init__(self, root, library):
        self.library = library
        self.root = root
        self.root.title("Library System")
        self.root.geometry("400x600")
        self.root.configure(bg="#f5f5f5")
        self.current_user = None
        self.current_user_password = None
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=5)
        self.style.configure("TLabel", background="#f5f5f5", font=("Helvetica", 12))
        self.style.configure("TFrame", background="#f5f5f5")
        self.login_screen()

    def login_screen(self):
        """Create the login or sign-in screen."""

        for widget in self.root.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="Library System", font=("Helvetica", 16, "bold")).pack(pady=10)
        ttk.Label(frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack()
        ttk.Label(frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.pack()
        ttk.Button(frame, text="Log In", command=self.log_in).pack(pady=10)
        ttk.Button(frame, text="Sign In", command=self.sign_in).pack()

    def log_in(self):
        """Handle user login."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        result = self.library.log_in(username, password, self)
        if result == "Log in successful":
            self.current_user = username
            self.current_user_password = password  # Save the password
            messagebox.showinfo("Login", "Login successful!")
            self.main_menu()
        else:
            messagebox.showerror("Login", result)

    def sign_in(self):
        """User registration."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        result = self.library.sign_in(username, password)
        if "successfully" in result:
            messagebox.showinfo("Sign In", result)
        else:
            messagebox.showerror("Sign In", result)

    def logout(self):
        """Log out the current user."""
        if self.current_user and self.current_user_password:
            result = self.library.log_out(self.current_user, self.current_user_password)
            if result == "Log out successful":
                messagebox.showinfo("Logout", result)
                self.current_user = None
                self.current_user_password = None
                self.login_screen()
            else:
                messagebox.showerror("Logout", result)

    def main_menu(self):
        """Create the main menu after successful login."""

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text=f"Welcome, {self.current_user}!", font=("Helvetica", 16, "bold")).pack(pady=10)
        ttk.Button(frame, text="Add Book", command=self.add_book_screen).pack(pady=5)
        ttk.Button(frame, text="Loan Book", command=self.loan_book_screen).pack(pady=5)
        ttk.Button(frame, text="Return Book", command=self.return_book_screen).pack(pady=5)
        ttk.Button(frame, text="Search Book", command=self.search_book_screen).pack(pady=5)
        ttk.Button(frame, text="View Books", command=self.view_books_screen).pack(pady=5)
        ttk.Button(frame, text="View Popular Books", command=self.popular_books_screen).pack(pady=5)
        ttk.Button(frame, text="Remove Book", command=self.remove_book_screen).pack(pady=5)
        ttk.Button(frame, text="Logout", command=self.logout).pack(pady=20)

    def view_books_screen(self):
        """Create the screen to choose between available and loaned books."""

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="View Books", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Button(frame, text="Available Books", command=self.available_books_screen).pack(pady=10)
        ttk.Button(frame, text="Loaned Books", command=self.loaned_books_screen).pack(pady=10)
        ttk.Button(frame, text="View All Books", command=self.view_all_books_screen).pack(pady=10)
        ttk.Button(frame, text="View Books By Category", command=self.by_categori_screen).pack(pady=10)
        ttk.Button(frame, text="Back", command=self.main_menu).pack(pady=20)

    def add_book_screen(self):
        """screen to add a book."""

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Add Book", font=("Helvetica", 16, "bold")).pack(pady=10)

        fields = ["Title", "Author", "Is Loaned (Yes/No)", "Copies", "Genre", "Year"]
        self.book_entries = {}
        for field in fields:
            ttk.Label(frame, text=f"{field}:").pack(pady=5)
            entry = ttk.Entry(frame, width=30)
            entry.pack()
            self.book_entries[field] = entry

        ttk.Button(frame, text="Add Book", command=self.add_book).pack(pady=10)
        ttk.Button(frame, text="Back", command=self.main_menu).pack(pady=10)

    def add_book(self):
        """adding a book."""
        data = {field: entry.get() for field, entry in self.book_entries.items()}
        try:
            self.library.add_book(
                data["Title"], data["Author"], data["Is Loaned (Yes/No)"],
                int(data["Copies"]), data["Genre"], int(data["Year"])
            )
            messagebox.showinfo("Add Book", "Book added successfully!")
        except Exception as e:
            messagebox.showerror("Add Book", f"Error adding book: {str(e)}")
        self.main_menu()

    def remove_book_screen(self):
        """screen to remove a book."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Remove Book", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Label(frame, text="Book Title:").pack(pady=5)
        self.remove_book_entry = ttk.Entry(frame, width=30)
        self.remove_book_entry.pack()

        ttk.Button(frame, text="Remove Book", command=self.remove_book).pack(pady=10)
        ttk.Button(frame, text="Back", command=self.main_menu).pack(pady=10)

    def remove_book(self):
        """removing a book."""
        title = self.remove_book_entry.get()
        result = self.library.remove_book(title)
        if result == "success":
            messagebox.showinfo("Remove Book", "Book removed successfully!")
        elif result == "failed - not_in_library":
            messagebox.showerror("Remove Book", "Book not found in the library.")
        elif result == "failed - all the copies are loaned - cannot remove":
            messagebox.showerror("Remove Book", "all the copies are loaned - cannot remove")
        else:
            messagebox.showerror("Remove Book", "An unexpected error occurred.")
        self.main_menu()

    def loan_book_screen(self):
        """Screen to loan a book."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Loan Book", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Label(frame, text="Book Title:").pack(pady=5)
        self.loan_book_entry = ttk.Entry(frame, width=30)
        self.loan_book_entry.pack()

        ttk.Button(frame, text="Loan Book", command=self.loan_book).pack(pady=10)
        ttk.Button(frame, text="Back", command=self.main_menu).pack(pady=10)

    def loan_book(self):
        """Handle loaning a book."""
        title = self.loan_book_entry.get().strip()  # Get the book title from the input field
        if not title:
            messagebox.showerror("Error", "Please enter a book title.")
            return

        # Call the library's loan_book function
        result = self.library.loan_book(title)

        if result == "success":
            messagebox.showinfo("Loan Book", "Book loaned successfully!")
        elif result == "failed - out_of_copies":
            self.show_waitlist_popup(title)
        elif result == "failed - not_in_library":
            messagebox.showerror("Loan Book", "Book not found in the library.")
        else:
            messagebox.showerror("Loan Book", "An unexpected error occurred.")

    def show_waitlist_popup(self, title):
        """Show a popup to add the user to the waiting list."""
        popup = tk.Toplevel(self.root)
        popup.title("Join Waiting List")

        ttk.Label(popup, text=f"No copies of '{title}' are available.", font=("Helvetica", 12)).pack(pady=10)
        ttk.Label(popup, text="Enter your phone number to join the waiting list:").pack(pady=5)

        phone_entry = ttk.Entry(popup, width=30)
        phone_entry.pack(pady=5)

        def submit_waitlist():
            phone_number = phone_entry.get().strip()
            if not phone_number:
                messagebox.showerror("Error", "Phone number cannot be empty.")
                return

            # Call the add_to_waiting_list function
            result = self.add_to_waiting_list(title, phone_number)
            if result == "success":
                messagebox.showinfo("Waiting List", f"You've been added to the waiting list for '{title}'.")
                popup.destroy()
            elif result == "failed - you already in the waiting list":
                messagebox.showinfo("Waiting List", f"You are already in the waiting list for '{title}'.")
            elif result == "failed - not a phone number":
                messagebox.showerror("Waiting List", "Invalid phone number format.")
            else:
                messagebox.showerror("Waiting List", "An unexpected error occurred.")
                popup.destroy()

        ttk.Button(popup, text="Submit", command=submit_waitlist).pack(pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=5)

    def add_to_waiting_list(self, title, phone_number):
        """Add the user to the waiting list for the specified book."""
        return self.library.add_to_waiting_list(title, phone_number)

    def return_book_screen(self):
        """screen to return a book."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Return Book", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Label(frame, text="Book Title:").pack(pady=5)
        self.return_book_entry = ttk.Entry(frame, width=30)
        self.return_book_entry.pack()

        ttk.Button(frame, text="Return Book", command=self.return_book).pack(pady=10)
        ttk.Button(frame, text="Back", command=self.main_menu).pack(pady=10)

    def return_book(self):
        """returning a book."""
        title = self.return_book_entry.get()
        result = self.library.return_book(title)

        if result == "success":
            messagebox.showinfo("Return Book", "Book returned successfully!")
        elif result == "still not available":
            messagebox.showinfo("Return Book", "Book returned successfully!")
        else:
            messagebox.showerror("Return Book", result)
        self.main_menu()

    def search_book_screen(self):
        """Screen to search for a book with a strategy."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Search Book", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Label(frame, text="Search Query:").pack(pady=5)
        self.search_book_entry = ttk.Entry(frame, width=30)
        self.search_book_entry.pack()

        ttk.Label(frame, text="Search By:").pack(pady=5)
        self.search_strategy = tk.StringVar(value="Title")  # Set default value to 'Title'
        strategies = ["Title", "Author", "Genre"]
        strategy_menu = ttk.OptionMenu(frame, self.search_strategy, self.search_strategy.get(), *strategies)
        strategy_menu.pack(pady=5)

        ttk.Button(frame, text="Search", command=self.search_book).pack(pady=10)
        ttk.Button(frame, text="Back", command=self.main_menu).pack(pady=10)

    def search_book(self):
        """Handle searching for a book with strategy."""
        query = self.search_book_entry.get()
        strategy_name = self.search_strategy.get()

        strategy_map = {
            "Title": TitleSearchStrategy(),
            "Author": AuthorSearchStrategy(),
            "Genre": GenreSearchStrategy(),
        }

        strategy = strategy_map.get(strategy_name)
        if not strategy:
            messagebox.showerror("Search Error", f"Invalid strategy: {strategy_name}")
            return

        try:
            result = self.library.search_book(strategy, query)
            if result:
                books = "\n".join([f"{book.title} by {book.author}" for book in result])
                messagebox.showinfo("Search Results", books)
            else:
                messagebox.showinfo("Search Results", "No books found.")
        except Exception as e:
            messagebox.showerror("Search Error", str(e))

        self.main_menu()

    def by_categori_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="By Category", font=("Helvetica", 16, "bold")).pack(pady=10)
        listbox = tk.Listbox(frame, width=50, height=15)
        listbox.pack(pady=10)

        books_by_category = self.library.get_books_sorted_by_genre()
        if books_by_category:
            for category, books in books_by_category.items():
                listbox.insert(tk.END, category)
                listbox.itemconfig(tk.END, {'fg': 'red'})
                for book in books:
                    listbox.insert(tk.END, f"  - {book.title}")
        else:
            ttk.Label(frame, text="No books found").pack(pady=10)
        ttk.Button(frame, text="Back", command=self.view_books_screen).pack(pady=10)

    def view_all_books_screen(self):
        """Display all books in the library."""

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="All Books", font=("Helvetica", 16, "bold")).pack(pady=10)

        all_books = self.library.get_all_books()
        if all_books:
            listbox = tk.Listbox(frame, width=50, height=15)
            listbox.pack(pady=10)
            for book in all_books:
                listbox.insert(tk.END, f"{book.title} by {book.author}")
        else:
            ttk.Label(frame, text="No books found").pack(pady=10)

        ttk.Button(frame, text="Back", command=self.view_books_screen).pack(pady=10)

    def available_books_screen(self):
        """Display available books."""
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="Available Books", font=("Helvetica", 16, "bold")).pack(pady=10)
        available_books = self.library.get_available_books()

        if available_books:
            listbox = tk.Listbox(frame, width=50, height=15)
            listbox.pack(pady=10)
            for title, count in available_books.items():
                listbox.insert(tk.END, f"{title} ")
        else:
            ttk.Label(frame, text="No available books").pack(pady=10)
        ttk.Button(frame, text="Back", command=self.view_books_screen).pack(pady=10)

    def loaned_books_screen(self):
        """Display loaned books."""
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="Loaned Books", font=("Helvetica", 16, "bold")).pack(pady=10)
        loaned_books = self.library.get_loaned_books()

        if loaned_books:
            listbox = tk.Listbox(frame, width=50, height=15)
            listbox.pack(pady=10)
            for title in loaned_books:
                listbox.insert(tk.END, title)
        else:
            ttk.Label(frame, text="No loaned books").pack(pady=10)
        ttk.Button(frame, text="Back", command=self.view_books_screen).pack(pady=10)

    def popular_books_screen(self):
        """Display the top 10 popular books."""
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text="Top 10 Popular Books", font=("Helvetica", 16, "bold")).pack(pady=10)
        popular_books = self.library.get_top_10_popular_books()
        if popular_books:
            listbox = tk.Listbox(frame, width=50, height=15)
            listbox.pack(pady=10)
            for book, _ in popular_books:
                listbox.insert(tk.END, book.title)
        else:
            ttk.Label(frame, text="No popular books found").pack(pady=10)
        ttk.Button(frame, text="Back", command=self.main_menu).pack(pady=10)

    def show_notification(self, message):
        notification_window = tk.Toplevel(self.root)
        notification_window.title("New Message")

        label = Label(notification_window, text=message)
        label.pack()

        button = Button(notification_window, text="Close", command=notification_window.destroy)
        button.pack()
        notification_window.wait_window(notification_window)


if __name__ == "__main__":
    root = tk.Tk()
    library = Library()
    app = LibraryGUI(root, library)
    root.mainloop()

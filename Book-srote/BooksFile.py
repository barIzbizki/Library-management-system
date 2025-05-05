import pandas as pd
from BookFactory import BookFactory


class BooksFile:
    file_path = "books.csv"

    @staticmethod
    def load_books_from_file():
        books = []
        try:
            df = pd.read_csv(BooksFile.file_path, encoding="utf-8")

            df["waiting_list"] = df["waiting_list"].fillna(" ").apply(
                lambda x: [phone.strip() for phone in x.split(",")] if isinstance(x, str) and x.strip() != "" else []
            )
            for _, row in df.iterrows():
                BookFactory.create_book(
                    books,
                    row["title"],
                    row["author"],
                    row["is_loaned"],
                    int(row["copies"]),
                    row["genre"],
                    int(row["year"]),
                    row["waiting_list"],
                    int(row["popular"])
                )
            print(f"SUCCESS: Loaded books from {BooksFile.file_path}")
        except FileNotFoundError:
            print(f"ERROR: File {BooksFile.file_path} not found.")
        except Exception as e:
            print(f"ERROR: Error loading books: {e}")
        return books

    @staticmethod
    def update_books_file(book):
        try:
            # Convert the book object to a dictionary
            row = book.to_dict()
            # Convert the waiting list to a comma-separated string
            row["waiting_list"] = ",".join(book.waiting_list) if book.waiting_list else ""
            # Create a DataFrame from the dictionary
            df = pd.DataFrame([row])
            # Append the DataFrame to the CSV file
            df.to_csv(BooksFile.file_path, mode="a", index=False, header=False, encoding="utf-8")
            print(f"SUCCESS: Book added to {BooksFile.file_path}")
        except Exception as e:
            print(f"ERROR: Failed to update books file: {e}")

    @staticmethod
    def remove_row_by_title(title_to_remove):
        try:
            df = pd.read_csv(BooksFile.file_path)
            df = df[df['title'] != title_to_remove]

            df.to_csv(BooksFile.file_path, index=False)
            print(f"SUCCESS: Removed row with title '{title_to_remove}'")
        except FileNotFoundError:
            print(f"ERROR: File {BooksFile.file_path} not found.")
        except Exception as e:
            print(f"ERROR: {e}")

    @staticmethod
    def update_is_loaned(title, change_to):
        try:
            df = pd.read_csv(BooksFile.file_path)
            if title in df['title'].values:
                df.loc[df['title'] == title, 'is_loaned'] = change_to

                df.to_csv(BooksFile.file_path, index=False)
                print(f"SUCCESS: Updated 'is_loaned' for title '{title}' to {change_to}.")
            else:
                print(f"ERROR: Title '{title}' not found in file.")
        except FileNotFoundError:
            print(f"ERROR: File '{BooksFile.file_path}' not found.")
        except Exception as e:
            print(f"ERROR: {e}")

    @staticmethod
    def update_waiting_list(title, waiting_list):
        df = pd.read_csv(BooksFile.file_path)
        book_index = df[df['title'] == title].index

        if not book_index.empty:
            waiting_list_str = ','.join(str(phone) for phone in waiting_list)
            df['waiting_list'] = df['waiting_list'].astype(str)
            df.at[book_index[0], 'waiting_list'] = waiting_list_str
            df.to_csv(BooksFile.file_path, index=False)
            return "Successfully updated the waiting list."
        else:
            return f"Book {title} not found in the library."

    @staticmethod
    def update_number_copies(title, number):
        df = pd.read_csv(BooksFile.file_path)
        book_index = df[df['title'] == title].index

        if not book_index.empty:
            df.at[book_index[0], 'copies'] = int(number)
            df.to_csv(BooksFile.file_path, index=False)
            return "Successfully updated the copies."
        else:
            return f"Book {title} not found in the library."

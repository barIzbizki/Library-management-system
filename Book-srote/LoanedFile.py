import pandas as pd


class LoanedFile:
    file_path = "loaned_books.csv"

    @staticmethod
    def load_listL_from_file():
        bookLoaned = []
        try:
            df = pd.read_csv(LoanedFile.file_path)
            bookLoaned = df["title"].tolist()
            print(f"SUCCESS: Loaded loaned books from {LoanedFile.file_path}")
        except FileNotFoundError:
            print(f"ERROR: File {LoanedFile.file_path} not found.")
        except Exception as e:
            print(f"ERROR: Error loading loaned books: {e}")
        return bookLoaned

    @staticmethod
    def remove_row_by_title(title_to_remove):
        try:
            df = pd.read_csv(LoanedFile.file_path)
            df = df[df['title'] != title_to_remove]

            df.to_csv(LoanedFile.file_path, index=False)
            print(f"SUCCESS: Removed row with title '{title_to_remove}'")
        except FileNotFoundError:
            print(f"ERROR: File {LoanedFile.file_path} not found.")
        except Exception as e:
            print(f"ERROR: {e}")

    @staticmethod
    def add_book_to_loaned(new_title):
        try:
            df = pd.read_csv(LoanedFile.file_path)
            if df.empty:
                df = pd.DataFrame(columns=["title"])
            new_row = {"title": new_title}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(LoanedFile.file_path, index=False)
            print(f"SUCCESS: Added '{new_title}' to {LoanedFile.file_path}")

        except FileNotFoundError:
            print(f"ERROR: File {LoanedFile.file_path} not found.")
        except Exception as e:
            print(f"ERROR: {e}")






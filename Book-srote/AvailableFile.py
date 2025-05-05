import pandas as pd


class AvailableFile:
    file_path = "available_books.csv"

    @staticmethod
    def load_listA_from_file():
        """
        Loads a dictionary of available books from the CSV file.
        The dictionary's keys are book titles and the values are the count of loan copies.

        Returns:
            A dictionary where keys are book titles (str) and values are counts (int).
        """
        bookAvailable = {}
        try:
            # Read the CSV file and convert it to a dictionary
            df = pd.read_csv(AvailableFile.file_path)
            bookAvailable = df.set_index("title")["count"].to_dict()
            print(f"SUCCESS: Loaded available books from {AvailableFile.file_path}")
        except FileNotFoundError:
            print(f"ERROR: File {AvailableFile.file_path} not found.")
        except Exception as e:
            print(f"ERROR: Error loading available books: {e}")
        return bookAvailable

    @staticmethod
    def remove_row_by_title(title_to_remove):
        """
        Removes a row from the CSV file based on the provided book title.
        """
        try:
            # Read the CSV file
            df = pd.read_csv(AvailableFile.file_path)
            # Filter out the row with the specified title
            df = df[df['title'] != title_to_remove]

            # Write the updated DataFrame back to the CSV file
            df.to_csv(AvailableFile.file_path, index=False)
            print(f"SUCCESS: Removed row with title '{title_to_remove}'")
        except FileNotFoundError:
            print(f"ERROR: File {AvailableFile.file_path} not found.")
        except Exception as e:
            print(f"ERROR: {e}")

    @staticmethod
    def add_row_to_av(title, count):
        """
        Adds a new book row with the specified title and count to the CSV file.

        Args:
            title (str): The title of the book to be added.
            count (int): The  count of the copies that loan.
        """
        try:
            # Try to load the existing CSV file or create an empty DataFrame
            try:
                df = pd.read_csv(AvailableFile.file_path)
            except FileNotFoundError:
                df = pd.DataFrame(columns=["title", "count"])

            # Create a new row with the given title and count
            new_row = pd.DataFrame({"title": [title], "count": [count]})
            # Append the new row to the existing DataFrame
            df = pd.concat([df, new_row], ignore_index=True)
            # Write the updated DataFrame back to the CSV file
            df.to_csv(AvailableFile.file_path, index=False)

            print(f"SUCCESS: Row with title '{title}' and count {count} added.")
        except Exception as e:
            print(f"ERROR: Failed to add row to {AvailableFile.file_path}: {e}")

    @staticmethod
    def update_count_available(title, count):
        """
        Updates the  count of a book in the CSV file by its title.
        """
        try:
            # Read the CSV file
            df = pd.read_csv(AvailableFile.file_path)
            # Update the count for the book with the given title
            df.loc[df["title"] == title, "count"] = count
            # Write the updated DataFrame back to the CSV file
            df.to_csv("available_books.csv", index=False)
        except Exception as e:
            print(f"ERROR: {e}")

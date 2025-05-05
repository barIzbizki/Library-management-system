import unittest
from Library import Library


class TestLibrary(unittest.TestCase):

    def test_add_book(self):
        library = Library()
        # adding new book
        result = library.add_book('addtest', 'bar', 'No', 2, 'Classic', 2025)
        self.assertEqual(result, "success")
        # adding the same book - needs to add as copy
        library.add_book('addtest', 'bar', 'No', 2, 'Classic', 2025)
        check_copy = None
        for i in library.books:
            if i.title == "addtest":
                check_copy = i
        self.assertEqual(4, check_copy.copies)
        library.remove_book("addtest")  # remove him after we finished

    def test_loaned_book(self):
        library = Library()
        # loaned a book that in the library and has copies
        library.add_book('loanedtest', 'bar', 'No', 1, 'Classic', 2025)
        result1 = library.loan_book("loanedtest")
        self.assertEqual(result1, "success")
        # loaned a book that in the library but out of copies
        result2 = library.loan_book("loanedtest")
        self.assertEqual(result2, "failed - out_of_copies")
        # try to loan a book that not int the library
        result3 = library.loan_book("newbook")
        self.assertEqual(result3, "failed - not_in_library")
        library.remove_book("loanedtest")  # remove him after we finished

    def test_log_in(self):
        # we know that we have - "bar", "12345" in the file
        library = Library()
        # try to log in with new user that not singed in
        result1 = library.log_in("newuser", "12345", None)
        self.assertEqual(result1, "failed -User not found")
        # try to log in with incorrect password
        result2 = library.log_in("bar", "12346",None)
        self.assertEqual(result2, "failed -Incorrect password")
        # try with correct password
        result3 = library.log_in("bar", "12345",None)
        self.assertEqual(result3, "Log in successful")

    def test_sing_in(self):
        #  library.sign_in("bar", "12345")
        library = Library()
        # try to sing in with user that already singed in
        result = library.sign_in("bar", "12345")
        self.assertEqual(result, "failed -User already exists.")

    def test_return_book(self):
        library = Library()
        library.add_book('returntest', 'bar', 'Yes', 1, 'Classic', 2025)
        # try to return a book that was loaned
        result1 = library.return_book("returntest")
        self.assertEqual(result1, "success")
        # try to return a book that al his copies are in the library
        result2 = library.return_book("returntest")
        self.assertEqual(result2, "failed - not_in_library")
        library.remove_book("returntest")  # remove him after we finished
        # try to return a book that not in the library
        result3 = library.return_book("trytry")
        self.assertEqual(result3, "failed - not_in_library")

    def test_waiting_list(self):
        library = Library()
        library.add_book('waitingtest', 'bar', 'Yes', 1, 'Classic', 2025)
        library.add_to_waiting_list("waitingtest", "0505329448")
        testb = None
        for i in library.books:
            if i.title == "waitingtest":
                testb = i
        self.assertEqual(testb.waiting_list[0], "0505329448,")
        library.return_book("waitingtest")
        # want to see that the first number he is the one that get the book
        self.assertEqual(testb.waiting_list, [])
        library.remove_book("waitingtest")

    def test_file_update(self):
        library1 = Library()
        library1.add_book('updatetest', 'bar', 'Yes', 1, 'Classic', 2025)
        library2 = Library()
        result = library2.search_by_title(library2.books, "updatetest")
        self.assertNotEqual(result, None)
        library1.remove_book("updatetest")


if __name__ == "__main__":
    unittest.main()

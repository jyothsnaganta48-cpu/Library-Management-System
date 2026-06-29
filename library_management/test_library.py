#!/usr/bin/env python3
"""
Unit tests for the Library Management System.

Run with: python -m pytest test_library.py -v
Or run directly: python test_library.py
"""

import unittest
import os
import json
from datetime import datetime, timedelta
from book import Book
from member import Member
from borrow_record import BorrowRecord
from library_manager import LibraryManager


class TestBook(unittest.TestCase):
    """Test cases for the Book class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.book = Book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008, 3)
    
    def test_book_creation(self):
        """Test book creation."""
        self.assertEqual(self.book.isbn, "978-0-134-68599-1")
        self.assertEqual(self.book.title, "Clean Code")
        self.assertEqual(self.book.author, "Robert Martin")
        self.assertEqual(self.book.total_quantity, 3)
        self.assertEqual(self.book.available_quantity, 3)
    
    def test_borrow_book(self):
        """Test borrowing a book."""
        self.assertTrue(self.book.borrow())
        self.assertEqual(self.book.available_quantity, 2)
        self.assertEqual(self.book.issued_quantity, 1)
    
    def test_return_book(self):
        """Test returning a book."""
        self.book.borrow()
        self.assertTrue(self.book.return_book())
        self.assertEqual(self.book.available_quantity, 3)
        self.assertEqual(self.book.issued_quantity, 0)
    
    def test_borrow_unavailable_book(self):
        """Test borrowing when no copies available."""
        self.book.available_quantity = 0
        self.assertFalse(self.book.borrow())
    
    def test_is_available(self):
        """Test availability check."""
        self.assertTrue(self.book.is_available())
        self.book.borrow()
        self.book.borrow()
        self.book.borrow()
        self.assertFalse(self.book.is_available())
    
    def test_book_serialization(self):
        """Test book to_dict and from_dict."""
        self.book.borrow()
        book_dict = self.book.to_dict()
        
        new_book = Book.from_dict(book_dict)
        self.assertEqual(new_book.isbn, self.book.isbn)
        self.assertEqual(new_book.title, self.book.title)
        self.assertEqual(new_book.available_quantity, self.book.available_quantity)


class TestMember(unittest.TestCase):
    """Test cases for the Member class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset counter for consistent IDs
        Member._member_id_counter = 1000
        self.member = Member("John Doe", "john@example.com", "9876543210")
    
    def test_member_creation(self):
        """Test member creation."""
        self.assertEqual(self.member.name, "John Doe")
        self.assertEqual(self.member.email, "john@example.com")
        self.assertEqual(self.member.phone, "9876543210")
        self.assertEqual(self.member.member_id, 1000)
        self.assertTrue(self.member.is_active)
    
    def test_member_id_increment(self):
        """Test member ID auto-increment."""
        member1 = Member("Alice", "alice@example.com")
        member2 = Member("Bob", "bob@example.com")
        self.assertEqual(member2.member_id, member1.member_id + 1)
    
    def test_add_borrowed_book(self):
        """Test adding borrowed book."""
        self.member.add_borrowed_book("978-0-134-68599-1")
        self.assertIn("978-0-134-68599-1", self.member.borrowed_books)
        self.assertEqual(self.member.get_borrowed_count(), 1)
    
    def test_remove_borrowed_book(self):
        """Test removing borrowed book."""
        self.member.add_borrowed_book("978-0-134-68599-1")
        self.assertTrue(self.member.remove_borrowed_book("978-0-134-68599-1"))
        self.assertEqual(self.member.get_borrowed_count(), 0)
    
    def test_member_serialization(self):
        """Test member to_dict and from_dict."""
        self.member.add_borrowed_book("978-0-134-68599-1")
        member_dict = self.member.to_dict()
        
        new_member = Member.from_dict(member_dict)
        self.assertEqual(new_member.member_id, self.member.member_id)
        self.assertEqual(new_member.name, self.member.name)
        self.assertEqual(len(new_member.borrowed_books), 1)


class TestBorrowRecord(unittest.TestCase):
    """Test cases for the BorrowRecord class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.record = BorrowRecord(1000, "978-0-134-68599-1", "Clean Code")
    
    def test_record_creation(self):
        """Test borrow record creation."""
        self.assertEqual(self.record.member_id, 1000)
        self.assertEqual(self.record.isbn, "978-0-134-68599-1")
        self.assertEqual(self.record.title, "Clean Code")
        self.assertFalse(self.record.is_returned)
    
    def test_due_date_calculation(self):
        """Test due date is set correctly."""
        expected_days = BorrowRecord.BORROWING_DAYS
        due_date = self.record.borrow_date + timedelta(days=expected_days)
        
        delta = (self.record.due_date - due_date).total_seconds()
        self.assertLess(abs(delta), 1)  # Within 1 second
    
    def test_return_book_no_fine(self):
        """Test returning book on time (no fine)."""
        fine = self.record.return_book()
        self.assertEqual(fine, 0.0)
        self.assertTrue(self.record.is_returned)
    
    def test_return_book_with_fine(self):
        """Test returning book late (with fine)."""
        # Simulate returning 5 days late
        return_date = self.record.due_date + timedelta(days=5)
        fine = self.record.return_book(return_date)
        
        expected_fine = 5 * BorrowRecord.FINE_PER_DAY
        self.assertEqual(fine, expected_fine)
    
    def test_is_overdue(self):
        """Test overdue checking."""
        self.assertFalse(self.record.is_overdue())
        
        # Move return date to past
        self.record.borrow_date = datetime.now() - timedelta(days=30)
        self.record.due_date = self.record.borrow_date + timedelta(days=14)
        
        self.assertTrue(self.record.is_overdue())
    
    def test_record_serialization(self):
        """Test record to_dict and from_dict."""
        self.record.return_book()
        record_dict = self.record.to_dict()
        
        new_record = BorrowRecord.from_dict(record_dict)
        self.assertEqual(new_record.member_id, self.record.member_id)
        self.assertEqual(new_record.isbn, self.record.isbn)
        self.assertEqual(new_record.is_returned, True)


class TestLibraryManager(unittest.TestCase):
    """Test cases for the LibraryManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_file = "test_library_data.json"
        self.library = LibraryManager(self.test_file)
        Member._member_id_counter = 1000
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_book(self):
        """Test adding a book."""
        result = self.library.add_book(
            "978-0-134-68599-1", "Clean Code", "Robert Martin", 2008, 2
        )
        self.assertTrue(result)
        self.assertEqual(len(self.library.books), 1)
    
    def test_add_duplicate_book(self):
        """Test adding duplicate book."""
        self.library.add_book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008)
        result = self.library.add_book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008)
        self.assertFalse(result)
    
    def test_search_books_by_title(self):
        """Test searching books by title."""
        self.library.add_book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008)
        self.library.add_book("978-0-201-63361-0", "Code Complete", "Steve McConnell", 2004)
        
        results = self.library.search_books("Clean", search_type="title")
        self.assertEqual(len(results), 2)
    
    def test_search_books_by_author(self):
        """Test searching books by author."""
        self.library.add_book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008)
        self.library.add_book("978-0-134-05652-8", "The Clean Coder", "Robert Martin", 2011)
        
        results = self.library.search_books("Robert Martin", search_type="author")
        self.assertEqual(len(results), 2)
    
    def test_register_member(self):
        """Test registering a member."""
        mid = self.library.register_member("John Doe", "john@example.com")
        self.assertEqual(mid, 1000)
        self.assertEqual(len(self.library.members), 1)
    
    def test_borrow_book(self):
        """Test borrowing a book."""
        self.library.add_book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008, 2)
        mid = self.library.register_member("John Doe", "john@example.com")
        
        result = self.library.borrow_book(mid, "978-0-134-68599-1")
        self.assertTrue(result)
        self.assertEqual(self.library.books["978-0-134-68599-1"].available_quantity, 1)
    
    def test_return_book(self):
        """Test returning a book."""
        self.library.add_book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008)
        mid = self.library.register_member("John Doe", "john@example.com")
        
        self.library.borrow_book(mid, "978-0-134-68599-1")
        fine = self.library.return_book(mid, "978-0-134-68599-1")
        
        self.assertIsNotNone(fine)
        self.assertEqual(self.library.books["978-0-134-68599-1"].available_quantity, 1)
    
    def test_get_library_status(self):
        """Test getting library status."""
        self.library.add_book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008, 3)
        self.library.add_book("978-0-201-63361-0", "Design Patterns", "Gang of Four", 1994, 2)
        
        self.library.register_member("John Doe", "john@example.com")
        
        status = self.library.get_library_status()
        self.assertEqual(status['total_books'], 5)
        self.assertEqual(status['total_members'], 1)
    
    def test_data_persistence(self):
        """Test saving and loading data."""
        self.library.add_book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008)
        mid = self.library.register_member("John Doe", "john@example.com")
        self.library.borrow_book(mid, "978-0-134-68599-1")
        
        # Create new library instance and load data
        library2 = LibraryManager(self.test_file)
        
        self.assertEqual(len(library2.books), 1)
        self.assertEqual(len(library2.members), 1)
        self.assertEqual(len(library2.borrow_records), 1)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_file = "test_integration_data.json"
        self.library = LibraryManager(self.test_file)
        Member._member_id_counter = 1000
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_complete_workflow(self):
        """Test complete library workflow."""
        # Add books
        books = [
            ("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008, 3),
            ("978-0-201-63361-0", "Design Patterns", "Gang of Four", 1994, 2),
        ]
        
        for isbn, title, author, year, qty in books:
            self.library.add_book(isbn, title, author, year, qty)
        
        # Register members
        members = [
            ("Alice", "alice@example.com", "1111111111"),
            ("Bob", "bob@example.com", "2222222222"),
        ]
        
        member_ids = []
        for name, email, phone in members:
            mid = self.library.register_member(name, email, phone)
            member_ids.append(mid)
        
        # Borrow books
        self.assertTrue(self.library.borrow_book(member_ids[0], "978-0-134-68599-1"))
        self.assertTrue(self.library.borrow_book(member_ids[1], "978-0-201-63361-0"))
        
        # Check status
        status = self.library.get_library_status()
        self.assertEqual(status['issued_books'], 2)
        self.assertEqual(status['available_books'], 3)
        
        # Return books
        fine1 = self.library.return_book(member_ids[0], "978-0-134-68599-1")
        fine2 = self.library.return_book(member_ids[1], "978-0-201-63361-0")
        
        self.assertIsNotNone(fine1)
        self.assertIsNotNone(fine2)
        
        # Verify return
        status = self.library.get_library_status()
        self.assertEqual(status['issued_books'], 0)
        self.assertEqual(status['available_books'], 5)
    
    def test_search_and_borrow(self):
        """Test searching and borrowing workflow."""
        self.library.add_book("978-0-134-68599-1", "Clean Code", "Robert Martin", 2008, 2)
        self.library.add_book("978-0-201-63361-0", "Code Design", "Steve McConnell", 2004, 1)
        
        # Search for books
        results = self.library.search_books("Code", search_type="title")
        self.assertEqual(len(results), 2)
        
        # Register and borrow
        mid = self.library.register_member("John", "john@example.com")
        self.assertTrue(self.library.borrow_book(mid, "978-0-134-68599-1"))


def run_tests():
    """Run all tests with verbose output."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestBook))
    suite.addTests(loader.loadTestsFromTestCase(TestMember))
    suite.addTests(loader.loadTestsFromTestCase(TestBorrowRecord))
    suite.addTests(loader.loadTestsFromTestCase(TestLibraryManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

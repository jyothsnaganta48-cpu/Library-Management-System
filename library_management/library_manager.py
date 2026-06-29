"""Main LibraryManager class for managing all library operations."""

import json
import os
from typing import List, Optional, Dict
from datetime import datetime

from book import Book
from member import Member
from borrow_record import BorrowRecord


class LibraryManager:
    """Main manager class for library operations."""
    
    def __init__(self, data_file: str = "library_data.json"):
        """
        Initialize the library manager.
        
        Args:
            data_file: Path to JSON file for storing library data
        """
        self.data_file = data_file
        self.books: Dict[str, Book] = {}  # ISBN -> Book
        self.members: Dict[int, Member] = {}  # Member ID -> Member
        self.borrow_records: List[BorrowRecord] = []  # All borrow records
        self.load_data()
    
    # ============ BOOK MANAGEMENT ============
    
    def add_book(self, isbn: str, title: str, author: str, 
                 publication_year: int, quantity: int = 1) -> bool:
        """
        Add a new book to the library.
        
        Args:
            isbn: ISBN of the book
            title: Title of the book
            author: Author of the book
            publication_year: Publication year
            quantity: Number of copies
            
        Returns:
            True if added successfully, False if book already exists
        """
        if isbn in self.books:
            print(f"❌ Book with ISBN {isbn} already exists.")
            return False
        
        self.books[isbn] = Book(isbn, title, author, publication_year, quantity)
        self.save_data()
        print(f"✅ Book '{title}' added successfully.")
        return True
    
    def update_book(self, isbn: str, **kwargs) -> bool:
        """
        Update book details.
        
        Args:
            isbn: ISBN of the book to update
            **kwargs: Fields to update (title, author, publication_year)
            
        Returns:
            True if updated, False if book not found
        """
        if isbn not in self.books:
            print(f"❌ Book with ISBN {isbn} not found.")
            return False
        
        book = self.books[isbn]
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        
        self.save_data()
        print(f"✅ Book updated successfully.")
        return True
    
    def remove_book(self, isbn: str) -> bool:
        """
        Remove a book from the library.
        
        Args:
            isbn: ISBN of the book to remove
            
        Returns:
            True if removed, False if book not found
        """
        if isbn not in self.books:
            print(f"❌ Book with ISBN {isbn} not found.")
            return False
        
        if self.books[isbn].issued_quantity > 0:
            print(f"❌ Cannot remove book. {self.books[isbn].issued_quantity} copies are currently borrowed.")
            return False
        
        title = self.books[isbn].title
        del self.books[isbn]
        self.save_data()
        print(f"✅ Book '{title}' removed successfully.")
        return True
    
    def search_books(self, query: str, search_type: str = "title") -> List[Book]:
        """
        Search for books.
        
        Args:
            query: Search query
            search_type: "title", "author", or "isbn"
            
        Returns:
            List of matching books
        """
        results = []
        query_lower = query.lower()
        
        for book in self.books.values():
            if search_type == "title" and query_lower in book.title.lower():
                results.append(book)
            elif search_type == "author" and query_lower in book.author.lower():
                results.append(book)
            elif search_type == "isbn" and query == book.isbn:
                results.append(book)
        
        return results
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Get a book by ISBN."""
        return self.books.get(isbn)
    
    def get_all_books(self) -> List[Book]:
        """Get all books in the library."""
        return list(self.books.values())
    
    # ============ MEMBER MANAGEMENT ============
    
    def register_member(self, name: str, email: str, phone: str = "") -> int:
        """
        Register a new library member.
        
        Args:
            name: Member's full name
            email: Member's email
            phone: Member's phone number
            
        Returns:
            Member ID if successful
        """
        member = Member(name, email, phone)
        self.members[member.member_id] = member
        self.save_data()
        print(f"✅ Member '{name}' registered successfully. Member ID: {member.member_id}")
        return member.member_id
    
    def get_member(self, member_id: int) -> Optional[Member]:
        """Get a member by ID."""
        return self.members.get(member_id)
    
    def get_all_members(self) -> List[Member]:
        """Get all members."""
        return list(self.members.values())
    
    def update_member(self, member_id: int, **kwargs) -> bool:
        """
        Update member details.
        
        Args:
            member_id: ID of the member to update
            **kwargs: Fields to update (name, email, phone)
            
        Returns:
            True if updated, False if member not found
        """
        if member_id not in self.members:
            print(f"❌ Member with ID {member_id} not found.")
            return False
        
        member = self.members[member_id]
        for key, value in kwargs.items():
            if hasattr(member, key):
                setattr(member, key, value)
        
        self.save_data()
        print(f"✅ Member updated successfully.")
        return True
    
    def deactivate_member(self, member_id: int) -> bool:
        """
        Deactivate a member account.
        
        Args:
            member_id: ID of the member to deactivate
            
        Returns:
            True if deactivated, False if member not found
        """
        if member_id not in self.members:
            print(f"❌ Member with ID {member_id} not found.")
            return False
        
        member = self.members[member_id]
        if member.get_borrowed_count() > 0:
            print(f"❌ Cannot deactivate member. {member.get_borrowed_count()} books are still borrowed.")
            return False
        
        member.is_active = False
        self.save_data()
        print(f"✅ Member deactivated successfully.")
        return True
    
    # ============ BORROWING OPERATIONS ============
    
    def borrow_book(self, member_id: int, isbn: str) -> bool:
        """
        Borrow a book.
        
        Args:
            member_id: ID of the member borrowing
            isbn: ISBN of the book to borrow
            
        Returns:
            True if successful, False otherwise
        """
        member = self.get_member(member_id)
        if not member:
            print(f"❌ Member with ID {member_id} not found.")
            return False
        
        if not member.is_active:
            print(f"❌ Member account is inactive.")
            return False
        
        book = self.get_book_by_isbn(isbn)
        if not book:
            print(f"❌ Book with ISBN {isbn} not found.")
            return False
        
        if not book.borrow():
            print(f"❌ No copies of '{book.title}' available.")
            return False
        
        # Create borrow record
        record = BorrowRecord(member_id, isbn, book.title)
        self.borrow_records.append(record)
        member.add_borrowed_book(isbn)
        
        self.save_data()
        print(f"✅ Book '{book.title}' borrowed successfully.")
        print(f"   Due Date: {record.due_date.strftime('%Y-%m-%d')}")
        return True
    
    def return_book(self, member_id: int, isbn: str) -> Optional[float]:
        """
        Return a book.
        
        Args:
            member_id: ID of the member returning
            isbn: ISBN of the book to return
            
        Returns:
            Fine amount if applicable, None if return failed
        """
        member = self.get_member(member_id)
        if not member:
            print(f"❌ Member with ID {member_id} not found.")
            return None
        
        book = self.get_book_by_isbn(isbn)
        if not book:
            print(f"❌ Book with ISBN {isbn} not found.")
            return None
        
        # Find the active borrow record
        active_record = None
        for record in self.borrow_records:
            if (record.member_id == member_id and record.isbn == isbn 
                and not record.is_returned):
                active_record = record
                break
        
        if not active_record:
            print(f"❌ No active borrow record found for this member and book.")
            return None
        
        # Return the book
        if not book.return_book():
            print(f"❌ Error returning book.")
            return None
        
        fine = active_record.return_book()
        member.remove_borrowed_book(isbn)
        
        self.save_data()
        print(f"✅ Book '{book.title}' returned successfully.")
        
        if fine > 0:
            print(f"⚠️  Late fine: ₹{fine:.2f}")
        else:
            print(f"✅ No fine charges.")
        
        return fine
    
    def get_member_borrowed_books(self, member_id: int) -> List[Book]:
        """Get all books currently borrowed by a member."""
        member = self.get_member(member_id)
        if not member:
            return []
        
        borrowed = []
        for isbn in member.borrowed_books:
            book = self.get_book_by_isbn(isbn)
            if book:
                borrowed.append(book)
        return borrowed
    
    def get_overdue_books(self) -> List[BorrowRecord]:
        """Get all overdue books."""
        return [record for record in self.borrow_records if record.is_overdue()]
    
    # ============ REPORT GENERATION ============
    
    def get_library_status(self) -> Dict:
        """Get overall library statistics."""
        total_books = sum(book.total_quantity for book in self.books.values())
        available_books = sum(book.available_quantity for book in self.books.values())
        issued_books = sum(book.issued_quantity for book in self.books.values())
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'issued_books': issued_books,
            'total_members': len(self.members),
            'active_members': sum(1 for m in self.members.values() if m.is_active),
            'total_titles': len(self.books),
            'overdue_count': len(self.get_overdue_books())
        }
    
    def get_borrow_history(self, member_id: Optional[int] = None) -> List[BorrowRecord]:
        """
        Get borrow history.
        
        Args:
            member_id: If provided, get history for specific member
            
        Returns:
            List of borrow records
        """
        if member_id:
            return [r for r in self.borrow_records if r.member_id == member_id]
        return self.borrow_records
    
    # ============ DATA PERSISTENCE ============
    
    def save_data(self) -> None:
        """Save all data to JSON file."""
        data = {
            'books': {isbn: book.to_dict() for isbn, book in self.books.items()},
            'members': {mid: member.to_dict() for mid, member in self.members.items()},
            'borrow_records': [record.to_dict() for record in self.borrow_records]
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self) -> None:
        """Load all data from JSON file."""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Load books
            for isbn, book_data in data.get('books', {}).items():
                self.books[isbn] = Book.from_dict(book_data)
            
            # Load members
            for mid_str, member_data in data.get('members', {}).items():
                mid = int(mid_str)
                self.members[mid] = Member.from_dict(member_data)
            
            # Load borrow records
            for record_data in data.get('borrow_records', []):
                self.borrow_records.append(BorrowRecord.from_dict(record_data))
            
            print(f"✅ Data loaded from {self.data_file}")
        except Exception as e:
            print(f"❌ Error loading data: {e}")

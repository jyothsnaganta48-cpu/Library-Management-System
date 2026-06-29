"""Member class for the library management system."""

from datetime import datetime
from typing import List


class Member:
    """Represents a library member."""
    
    _member_id_counter = 1000  # Starting ID for members
    
    def __init__(self, name: str, email: str, phone: str = ""):
        """
        Initialize a member.
        
        Args:
            name: Full name of the member
            email: Email address of the member
            phone: Phone number of the member (optional)
        """
        self.member_id = Member._member_id_counter
        Member._member_id_counter += 1
        
        self.name = name
        self.email = email
        self.phone = phone
        self.registration_date = datetime.now().isoformat()
        self.borrowed_books: List[str] = []  # List of ISBNs
        self.is_active = True
    
    def add_borrowed_book(self, isbn: str) -> None:
        """Add a book ISBN to member's borrowed list."""
        if isbn not in self.borrowed_books:
            self.borrowed_books.append(isbn)
    
    def remove_borrowed_book(self, isbn: str) -> bool:
        """
        Remove a book ISBN from member's borrowed list.
        
        Returns:
            True if successful, False if book not in list
        """
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)
            return True
        return False
    
    def get_borrowed_count(self) -> int:
        """Get the number of books currently borrowed."""
        return len(self.borrowed_books)
    
    def is_member_valid(self) -> bool:
        """Check if member is active and can borrow books."""
        return self.is_active
    
    def to_dict(self) -> dict:
        """Convert member to dictionary for JSON serialization."""
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'registration_date': self.registration_date,
            'borrowed_books': self.borrowed_books,
            'is_active': self.is_active
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Member':
        """Create a Member object from a dictionary."""
        member = Member(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', '')
        )
        member.member_id = data['member_id']
        # Update the counter to avoid ID duplication
        if data['member_id'] >= Member._member_id_counter:
            Member._member_id_counter = data['member_id'] + 1
        
        member.registration_date = data['registration_date']
        member.borrowed_books = data.get('borrowed_books', [])
        member.is_active = data.get('is_active', True)
        return member
    
    def __str__(self) -> str:
        """String representation of the member."""
        status = "Active" if self.is_active else "Inactive"
        return (f"ID: {self.member_id} | {self.name} | Email: {self.email} | "
                f"Books Borrowed: {self.get_borrowed_count()} | Status: {status}")
    
    def __repr__(self) -> str:
        """Detailed representation of the member."""
        return f"Member(member_id={self.member_id}, name='{self.name}')"

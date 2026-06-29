"""Book class for the library management system."""

from datetime import datetime
from typing import Optional


class Book:
    """Represents a book in the library."""
    
    def __init__(self, isbn: str, title: str, author: str, publication_year: int, quantity: int = 1):
        """
        Initialize a book.
        
        Args:
            isbn: International Standard Book Number (unique identifier)
            title: Title of the book
            author: Author of the book
            publication_year: Year the book was published
            quantity: Number of copies available
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.total_quantity = quantity
        self.available_quantity = quantity
        self.issued_quantity = 0
        self.creation_date = datetime.now().isoformat()
    
    def borrow(self) -> bool:
        """
        Decrease available quantity when a book is borrowed.
        
        Returns:
            True if successful, False if no copies available
        """
        if self.available_quantity > 0:
            self.available_quantity -= 1
            self.issued_quantity += 1
            return True
        return False
    
    def return_book(self) -> bool:
        """
        Increase available quantity when a book is returned.
        
        Returns:
            True if successful, False if all copies already returned
        """
        if self.issued_quantity > 0:
            self.available_quantity += 1
            self.issued_quantity -= 1
            return True
        return False
    
    def is_available(self) -> bool:
        """Check if the book has available copies."""
        return self.available_quantity > 0
    
    def to_dict(self) -> dict:
        """Convert book to dictionary for JSON serialization."""
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'publication_year': self.publication_year,
            'total_quantity': self.total_quantity,
            'available_quantity': self.available_quantity,
            'issued_quantity': self.issued_quantity,
            'creation_date': self.creation_date
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Book':
        """Create a Book object from a dictionary."""
        book = Book(
            isbn=data['isbn'],
            title=data['title'],
            author=data['author'],
            publication_year=data['publication_year'],
            quantity=data['total_quantity']
        )
        book.available_quantity = data['available_quantity']
        book.issued_quantity = data['issued_quantity']
        book.creation_date = data['creation_date']
        return book
    
    def __str__(self) -> str:
        """String representation of the book."""
        return (f"ISBN: {self.isbn} | {self.title} by {self.author} "
                f"({self.publication_year}) | Available: {self.available_quantity}/{self.total_quantity}")
    
    def __repr__(self) -> str:
        """Detailed representation of the book."""
        return f"Book(isbn='{self.isbn}', title='{self.title}')"

"""Library Management System Package."""

from book import Book
from member import Member
from borrow_record import BorrowRecord
from library_manager import LibraryManager
from cli import LibraryCLI

__all__ = [
    'Book',
    'Member',
    'BorrowRecord',
    'LibraryManager',
    'LibraryCLI'
]

__version__ = '1.0.0'
__author__ = 'Library Management Team'

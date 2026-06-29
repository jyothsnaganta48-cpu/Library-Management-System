"""BorrowRecord class for tracking borrowing activities."""

from datetime import datetime, timedelta
from typing import Optional


class BorrowRecord:
    """Represents a borrowing transaction in the library."""
    
    FINE_PER_DAY = 10  # Fine amount per day in currency units
    BORROWING_DAYS = 14  # Standard borrowing period
    
    def __init__(self, member_id: int, isbn: str, title: str):
        """
        Initialize a borrow record.
        
        Args:
            member_id: ID of the member borrowing the book
            isbn: ISBN of the borrowed book
            title: Title of the borrowed book
        """
        self.record_id = self._generate_record_id()
        self.member_id = member_id
        self.isbn = isbn
        self.title = title
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=self.BORROWING_DAYS)
        self.return_date: Optional[datetime] = None
        self.fine_amount = 0.0
        self.is_returned = False
    
    @staticmethod
    def _generate_record_id() -> str:
        """Generate a unique record ID based on timestamp."""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def return_book(self, return_date: Optional[datetime] = None) -> float:
        """
        Mark the book as returned and calculate any fines.
        
        Args:
            return_date: Date of return (defaults to today)
            
        Returns:
            Amount of fine for late return
        """
        self.return_date = return_date or datetime.now()
        self.is_returned = True
        self.fine_amount = self._calculate_fine()
        return self.fine_amount
    
    def _calculate_fine(self) -> float:
        """
        Calculate fine for late return.
        
        Returns:
            Fine amount in currency units
        """
        if not self.is_returned or not self.return_date:
            return 0.0
        
        days_late = (self.return_date.date() - self.due_date.date()).days
        if days_late > 0:
            return days_late * self.FINE_PER_DAY
        return 0.0
    
    def get_days_borrowed(self) -> int:
        """Calculate days borrowed."""
        end_date = self.return_date or datetime.now()
        return (end_date.date() - self.borrow_date.date()).days
    
    def is_overdue(self) -> bool:
        """Check if the book is overdue (not returned and past due date)."""
        if self.is_returned:
            return False
        return datetime.now() > self.due_date
    
    def get_days_overdue(self) -> int:
        """Get the number of days overdue."""
        if not self.is_overdue():
            return 0
        return (datetime.now().date() - self.due_date.date()).days
    
    def to_dict(self) -> dict:
        """Convert record to dictionary for JSON serialization."""
        return {
            'record_id': self.record_id,
            'member_id': self.member_id,
            'isbn': self.isbn,
            'title': self.title,
            'borrow_date': self.borrow_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'fine_amount': self.fine_amount,
            'is_returned': self.is_returned
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'BorrowRecord':
        """Create a BorrowRecord object from a dictionary."""
        record = BorrowRecord(
            member_id=data['member_id'],
            isbn=data['isbn'],
            title=data['title']
        )
        record.record_id = data['record_id']
        record.borrow_date = datetime.fromisoformat(data['borrow_date'])
        record.due_date = datetime.fromisoformat(data['due_date'])
        
        if data['return_date']:
            record.return_date = datetime.fromisoformat(data['return_date'])
        
        record.fine_amount = data['fine_amount']
        record.is_returned = data['is_returned']
        return record
    
    def __str__(self) -> str:
        """String representation of the borrow record."""
        status = "Returned" if self.is_returned else "Active"
        return (f"Record ID: {self.record_id} | Member: {self.member_id} | "
                f"Book: {self.title} | Status: {status}")
    
    def __repr__(self) -> str:
        """Detailed representation of the borrow record."""
        return f"BorrowRecord(record_id='{self.record_id}', member_id={self.member_id})"

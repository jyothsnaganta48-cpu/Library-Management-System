"""Command-line interface for the library management system."""

from library_manager import LibraryManager
from datetime import datetime


class LibraryCLI:
    """CLI interface for library operations."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.library = LibraryManager()
    
    def display_menu(self) -> None:
        """Display main menu."""
        print("\n" + "="*60)
        print("      📚 LIBRARY MANAGEMENT SYSTEM 📚".center(60))
        print("="*60)
        print("\n[1] Book Management")
        print("[2] Member Management")
        print("[3] Borrowing Operations")
        print("[4] Reports & Statistics")
        print("[5] Exit")
        print("-"*60)
    
    def display_book_menu(self) -> None:
        """Display book management menu."""
        print("\n[BOOK MANAGEMENT]")
        print("[1] Add Book")
        print("[2] Update Book")
        print("[3] Remove Book")
        print("[4] Search Books")
        print("[5] View All Books")
        print("[6] Back to Main Menu")
    
    def display_member_menu(self) -> None:
        """Display member management menu."""
        print("\n[MEMBER MANAGEMENT]")
        print("[1] Register Member")
        print("[2] View All Members")
        print("[3] Update Member")
        print("[4] Deactivate Member")
        print("[5] View Member Borrowed Books")
        print("[6] Back to Main Menu")
    
    def display_borrowing_menu(self) -> None:
        """Display borrowing operations menu."""
        print("\n[BORROWING OPERATIONS]")
        print("[1] Borrow Book")
        print("[2] Return Book")
        print("[3] View Overdue Books")
        print("[4] Member Borrow History")
        print("[5] Back to Main Menu")
    
    def display_reports_menu(self) -> None:
        """Display reports menu."""
        print("\n[REPORTS & STATISTICS]")
        print("[1] Library Status")
        print("[2] All Borrow History")
        print("[3] Overdue Report")
        print("[4] Back to Main Menu")
    
    # ============ BOOK OPERATIONS ============
    
    def add_book(self) -> None:
        """Add a new book."""
        print("\n[ADD BOOK]")
        isbn = input("Enter ISBN: ").strip()
        title = input("Enter Title: ").strip()
        author = input("Enter Author: ").strip()
        
        try:
            year = int(input("Enter Publication Year: ").strip())
            quantity = int(input("Enter Quantity (default 1): ").strip() or "1")
        except ValueError:
            print("❌ Invalid input for year or quantity.")
            return
        
        self.library.add_book(isbn, title, author, year, quantity)
    
    def update_book(self) -> None:
        """Update book details."""
        print("\n[UPDATE BOOK]")
        isbn = input("Enter ISBN of book to update: ").strip()
        
        if not self.library.get_book_by_isbn(isbn):
            print("❌ Book not found.")
            return
        
        print("Leave field empty to skip updating it.")
        title = input("New Title (leave empty to skip): ").strip()
        author = input("New Author (leave empty to skip): ").strip()
        year_str = input("New Publication Year (leave empty to skip): ").strip()
        
        update_data = {}
        if title:
            update_data['title'] = title
        if author:
            update_data['author'] = author
        if year_str:
            try:
                update_data['publication_year'] = int(year_str)
            except ValueError:
                print("❌ Invalid year input.")
                return
        
        if update_data:
            self.library.update_book(isbn, **update_data)
        else:
            print("No updates provided.")
    
    def remove_book(self) -> None:
        """Remove a book."""
        print("\n[REMOVE BOOK]")
        isbn = input("Enter ISBN of book to remove: ").strip()
        self.library.remove_book(isbn)
    
    def search_books(self) -> None:
        """Search for books."""
        print("\n[SEARCH BOOKS]")
        print("[1] Search by Title")
        print("[2] Search by Author")
        print("[3] Search by ISBN")
        choice = input("Select search type: ").strip()
        
        search_types = {'1': 'title', '2': 'author', '3': 'isbn'}
        if choice not in search_types:
            print("❌ Invalid choice.")
            return
        
        query = input(f"Enter search query: ").strip()
        results = self.library.search_books(query, search_types[choice])
        
        if results:
            print(f"\n📚 Found {len(results)} book(s):")
            for book in results:
                print(f"  • {book}")
        else:
            print("❌ No books found.")
    
    def view_all_books(self) -> None:
        """View all books."""
        books = self.library.get_all_books()
        
        if not books:
            print("❌ No books in the library.")
            return
        
        print(f"\n📚 Total Books: {len(books)}")
        print("-"*100)
        for book in books:
            print(f"  {book}")
        print("-"*100)
    
    # ============ MEMBER OPERATIONS ============
    
    def register_member(self) -> None:
        """Register a new member."""
        print("\n[REGISTER MEMBER]")
        name = input("Enter Full Name: ").strip()
        email = input("Enter Email: ").strip()
        phone = input("Enter Phone (optional): ").strip()
        
        self.library.register_member(name, email, phone)
    
    def view_all_members(self) -> None:
        """View all members."""
        members = self.library.get_all_members()
        
        if not members:
            print("❌ No members registered.")
            return
        
        print(f"\n👥 Total Members: {len(members)}")
        print("-"*100)
        for member in members:
            print(f"  {member}")
        print("-"*100)
    
    def update_member(self) -> None:
        """Update member details."""
        print("\n[UPDATE MEMBER]")
        try:
            member_id = int(input("Enter Member ID: ").strip())
        except ValueError:
            print("❌ Invalid member ID.")
            return
        
        if not self.library.get_member(member_id):
            print("❌ Member not found.")
            return
        
        print("Leave field empty to skip updating it.")
        name = input("New Name (leave empty to skip): ").strip()
        email = input("New Email (leave empty to skip): ").strip()
        phone = input("New Phone (leave empty to skip): ").strip()
        
        update_data = {}
        if name:
            update_data['name'] = name
        if email:
            update_data['email'] = email
        if phone:
            update_data['phone'] = phone
        
        if update_data:
            self.library.update_member(member_id, **update_data)
        else:
            print("No updates provided.")
    
    def deactivate_member(self) -> None:
        """Deactivate a member."""
        print("\n[DEACTIVATE MEMBER]")
        try:
            member_id = int(input("Enter Member ID to deactivate: ").strip())
        except ValueError:
            print("❌ Invalid member ID.")
            return
        
        self.library.deactivate_member(member_id)
    
    def view_member_books(self) -> None:
        """View books borrowed by a member."""
        print("\n[VIEW MEMBER'S BORROWED BOOKS]")
        try:
            member_id = int(input("Enter Member ID: ").strip())
        except ValueError:
            print("❌ Invalid member ID.")
            return
        
        member = self.library.get_member(member_id)
        if not member:
            print("❌ Member not found.")
            return
        
        books = self.library.get_member_borrowed_books(member_id)
        
        if not books:
            print(f"✅ Member has no borrowed books.")
            return
        
        print(f"\n📚 Books borrowed by {member.name}:")
        for book in books:
            print(f"  • {book}")
    
    # ============ BORROWING OPERATIONS ============
    
    def borrow_book(self) -> None:
        """Borrow a book."""
        print("\n[BORROW BOOK]")
        try:
            member_id = int(input("Enter Member ID: ").strip())
        except ValueError:
            print("❌ Invalid member ID.")
            return
        
        isbn = input("Enter Book ISBN: ").strip()
        self.library.borrow_book(member_id, isbn)
    
    def return_book(self) -> None:
        """Return a book."""
        print("\n[RETURN BOOK]")
        try:
            member_id = int(input("Enter Member ID: ").strip())
        except ValueError:
            print("❌ Invalid member ID.")
            return
        
        isbn = input("Enter Book ISBN: ").strip()
        self.library.return_book(member_id, isbn)
    
    def view_overdue_books(self) -> None:
        """View overdue books."""
        overdue = self.library.get_overdue_books()
        
        if not overdue:
            print("✅ No overdue books!")
            return
        
        print(f"\n⚠️  Overdue Books: {len(overdue)}")
        print("-"*80)
        total_fine = 0
        for record in overdue:
            member = self.library.get_member(record.member_id)
            days_overdue = record.get_days_overdue()
            fine = record.get_days_overdue() * record.FINE_PER_DAY
            total_fine += fine
            
            print(f"  Member: {member.name} (ID: {member.member_id})")
            print(f"  Book: {record.title}")
            print(f"  Due Date: {record.due_date.strftime('%Y-%m-%d')}")
            print(f"  Days Overdue: {days_overdue}")
            print(f"  Fine Amount: ₹{fine:.2f}")
            print("-"*80)
        
        print(f"\nTotal Fine Amount: ₹{total_fine:.2f}")
    
    def member_borrow_history(self) -> None:
        """View borrow history for a member."""
        print("\n[MEMBER BORROW HISTORY]")
        try:
            member_id = int(input("Enter Member ID: ").strip())
        except ValueError:
            print("❌ Invalid member ID.")
            return
        
        member = self.library.get_member(member_id)
        if not member:
            print("❌ Member not found.")
            return
        
        history = self.library.get_borrow_history(member_id)
        
        if not history:
            print(f"✅ No borrow history for {member.name}.")
            return
        
        print(f"\n📖 Borrow History for {member.name}:")
        print("-"*100)
        for record in history:
            status = "Returned" if record.is_returned else "Active"
            print(f"  Book: {record.title}")
            print(f"  Borrowed: {record.borrow_date.strftime('%Y-%m-%d')}")
            print(f"  Due: {record.due_date.strftime('%Y-%m-%d')}")
            if record.return_date:
                print(f"  Returned: {record.return_date.strftime('%Y-%m-%d')}")
            print(f"  Fine: ₹{record.fine_amount:.2f}")
            print(f"  Status: {status}")
            print("-"*100)
    
    # ============ REPORTS ============
    
    def library_status(self) -> None:
        """Display library status."""
        status = self.library.get_library_status()
        
        print("\n[LIBRARY STATUS]")
        print("="*50)
        print(f"Total Titles: {status['total_books']}")
        print(f"Available Books: {status['available_books']}")
        print(f"Issued Books: {status['issued_books']}")
        print(f"Total Members: {status['total_members']}")
        print(f"Active Members: {status['active_members']}")
        print(f"Total Borrow Records: {len(self.library.borrow_records)}")
        print(f"Overdue Books: {status['overdue_count']}")
        print("="*50)
    
    def all_borrow_history(self) -> None:
        """View all borrow history."""
        history = self.library.get_borrow_history()
        
        if not history:
            print("✅ No borrow history.")
            return
        
        print(f"\n[ALL BORROW HISTORY] - Total Records: {len(history)}")
        print("-"*100)
        for record in history:
            status = "Returned" if record.is_returned else "Active"
            member = self.library.get_member(record.member_id)
            
            print(f"  Record ID: {record.record_id}")
            print(f"  Member: {member.name} (ID: {member.member_id})")
            print(f"  Book: {record.title}")
            print(f"  Borrowed: {record.borrow_date.strftime('%Y-%m-%d')}")
            print(f"  Due: {record.due_date.strftime('%Y-%m-%d')}")
            if record.return_date:
                print(f"  Returned: {record.return_date.strftime('%Y-%m-%d')}")
            print(f"  Fine: ₹{record.fine_amount:.2f}")
            print(f"  Status: {status}")
            print("-"*100)
    
    def overdue_report(self) -> None:
        """Display overdue report."""
        self.view_overdue_books()
    
    # ============ MAIN MENU LOOP ============
    
    def run(self) -> None:
        """Run the CLI application."""
        print("\n✅ Welcome to Library Management System!")
        
        while True:
            self.display_menu()
            choice = input("Select option: ").strip()
            
            if choice == '1':
                self.book_menu()
            elif choice == '2':
                self.member_menu()
            elif choice == '3':
                self.borrowing_menu()
            elif choice == '4':
                self.reports_menu()
            elif choice == '5':
                print("\n👋 Thank you for using Library Management System!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def book_menu(self) -> None:
        """Handle book management menu."""
        while True:
            self.display_book_menu()
            choice = input("Select option: ").strip()
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.update_book()
            elif choice == '3':
                self.remove_book()
            elif choice == '4':
                self.search_books()
            elif choice == '5':
                self.view_all_books()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def member_menu(self) -> None:
        """Handle member management menu."""
        while True:
            self.display_member_menu()
            choice = input("Select option: ").strip()
            
            if choice == '1':
                self.register_member()
            elif choice == '2':
                self.view_all_members()
            elif choice == '3':
                self.update_member()
            elif choice == '4':
                self.deactivate_member()
            elif choice == '5':
                self.view_member_books()
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def borrowing_menu(self) -> None:
        """Handle borrowing operations menu."""
        while True:
            self.display_borrowing_menu()
            choice = input("Select option: ").strip()
            
            if choice == '1':
                self.borrow_book()
            elif choice == '2':
                self.return_book()
            elif choice == '3':
                self.view_overdue_books()
            elif choice == '4':
                self.member_borrow_history()
            elif choice == '5':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def reports_menu(self) -> None:
        """Handle reports menu."""
        while True:
            self.display_reports_menu()
            choice = input("Select option: ").strip()
            
            if choice == '1':
                self.library_status()
            elif choice == '2':
                self.all_borrow_history()
            elif choice == '3':
                self.overdue_report()
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    cli = LibraryCLI()
    cli.run()

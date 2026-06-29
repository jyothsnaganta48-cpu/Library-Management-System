#!/usr/bin/env python3


import sys
import argparse
from cli import LibraryCLI
from library_manager import LibraryManager
from datetime import datetime, timedelta


def demo_mode():
    """Run demo mode with sample data."""
    print("\n" + "="*60)
    print("      🎬 DEMO MODE - LIBRARY MANAGEMENT SYSTEM 🎬".center(60))
    print("="*60)
    
    library = LibraryManager("demo_library_data.json")
    
    # Add sample books
    print("\n📚 Adding sample books...")
    books_data = [
        ("978-0-134-68599-1", "Clean Code", "Robert C. Martin", 2008, 3),
        ("978-0-201-63361-0", "Design Patterns", "Gang of Four", 1994, 2),
        ("978-0-596-00712-6", "Programming Perl", "Larry Wall", 2000, 1),
        ("978-0-262-03384-8", "Introduction to Algorithms", "Cormen, Leiserson", 2009, 2),
        ("978-1-491-95107-8", "Python Data Science", "Jake VanderPlas", 2016, 3),
    ]
    
    for isbn, title, author, year, qty in books_data:
        library.add_book(isbn, title, author, year, qty)
    
    # Add sample members
    print("\n👥 Registering sample members...")
    members_data = [
        ("Alice Johnson", "alice@example.com", "9876543210"),
        ("Bob Smith", "bob@example.com", "9876543211"),
        ("Carol White", "carol@example.com", "9876543212"),
    ]
    
    member_ids = []
    for name, email, phone in members_data:
        mid = library.register_member(name, email, phone)
        member_ids.append(mid)
    
    # Perform borrowing operations
    print("\n📖 Performing borrowing operations...")
    library.borrow_book(member_ids[0], "978-0-134-68599-1")
    library.borrow_book(member_ids[0], "978-0-201-63361-0")
    library.borrow_book(member_ids[1], "978-0-596-00712-6")
    library.borrow_book(member_ids[2], "978-0-262-03384-8")
    
    # Return a book
    print("\n✅ Returning a book...")
    library.return_book(member_ids[0], "978-0-134-68599-1")
    
    # Display reports
    print("\n" + "="*60)
    print("LIBRARY STATUS REPORT")
    print("="*60)
    status = library.get_library_status()
    print(f"Total Titles: {status['total_books']}")
    print(f"Available Books: {status['available_books']}")
    print(f"Issued Books: {status['issued_books']}")
    print(f"Total Members: {status['total_members']}")
    print(f"Active Members: {status['active_members']}")
    print(f"Total Borrow Records: {len(library.borrow_records)}")
    
    print("\n" + "="*60)
    print("ALL MEMBERS")
    print("="*60)
    for member in library.get_all_members():
        print(f"  {member}")
    
    print("\n" + "="*60)
    print("ALL BOOKS")
    print("="*60)
    for book in library.get_all_books():
        print(f"  {book}")
    
    print("\n✅ Demo completed! Data saved to 'demo_library_data.json'")
    print("Run 'python main.py' to start the interactive CLI.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Library Management System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Run interactive CLI
  python main.py --demo       # Run demo with sample data
  python main.py --help       # Show this help message
        """
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demo mode with sample data'
    )
    
    args = parser.parse_args()
    
    if args.demo:
        demo_mode()
    else:
        cli = LibraryCLI()
        cli.run()


if __name__ == "__main__":
    main()

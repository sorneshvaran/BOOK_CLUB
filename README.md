# Book Club Membership and Lending Database

## Overview
This is a full-stack web application for managing a book club's membership and lending system. The application consists of:
- **Backend**: Python Flask API with SQLite database
- **Frontend**: HTML/CSS/JavaScript client interface
- **Architecture**: RESTful API with CRUD operations for members, books, and lending

## Features
- **Member Management**: Add, view, and remove members from the book club
- **Book Management**: Catalog books with titles, authors, and availability status
- **Lending System**: Track book loans between members with loan and return functionality
- **Responsive UI**: Clean, user-friendly interface for managing the book club
- **RESTful API**: Well-defined endpoints for all operations

## Technology Stack
- **Backend**: Python, Flask, Flask-CORS, SQLite
- **Database**: SQLite with custom schema
- **Frontend**: Plain HTML, CSS, and JavaScript (no framework)
- **API**: RESTful endpoints with JSON data exchange

## Database Schema

The application uses SQLite with three main tables:

### Members Table
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `name` (TEXT, NOT NULL)
- `email` (TEXT, NOT NULL, UNIQUE)
- `joined_date` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### Books Table
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `title` (TEXT, NOT NULL)
- `author` (TEXT, NOT NULL)
- `published_date` (DATE)
- `available` (INTEGER, DEFAULT 1)

### Loans Table
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `member_id` (INTEGER, NOT NULL, FOREIGN KEY to members.id)
- `book_id` (INTEGER, NOT NULL, FOREIGN KEY to books.id)
- `loan_date` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `return_date` (TIMESTAMP)

## Project Structure
```
book-club-app
├── frontend
│   ├── index.html        # Main HTML document
│   ├── css
│   │   └── styles.css    # Styles for the frontend
│   └── css/js
│       └── app.js        # JavaScript for user interactions
├── backend
│   ├── app.py            # Entry point for the backend application
│   ├── api.py            # API endpoints for the application
│   ├── models
│   │   ├── __init__.py   # Initializes the models package
│   │   ├── member.py     # Member model
│   │   └── book.py       # Book model
│   ├── db
│   │   └── schema.sql    # SQL schema for the SQLite database
│   ├── scripts
│   │   └── init_db.py    # Script to initialize the database
│   └── requirements.txt   # Dependencies for the backend
├── tests
│   └── test_api.py       # Unit tests for the API
├── .env.example           # Example of environment variables
└── README.md              # Project documentation
```

## API Endpoints

### Members
- `GET /api/members` - Retrieve all members
- `POST /api/members` - Add a new member (requires: name, email)
- `DELETE /api/members/<id>` - Delete a member by ID

### Books
- `GET /api/books` - Retrieve all books
- `POST /api/books` - Add a new book (requires: title, author)
- `DELETE /api/books/<id>` - Delete a book by ID

### Lending
- `POST /api/lend` - Lend a book to a member (requires: member_id, book_id)
- `GET /api/loans` - Retrieve all current (non-returned) loans
- `POST /api/loans/<id>/return` - Mark a loan as returned

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd book-club-app/backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Initialize the database:
   ```bash
   python -m backend.scripts.init_db
   # If the script doesn't exist, the database will be created automatically on first run
   ```

6. Start the backend server:
   ```bash
   python app.py
   ```
   The backend server will start on `http://localhost:5000`

### Frontend Access
The frontend is served statically by the Flask app when the backend is running.

1. Start the backend server (as described above)
2. Open your browser to `http://localhost:5000` to access the application

## Running Tests
Execute the tests with:
```bash
python -m pytest tests/
```
or
```bash
python tests/test_api.py
```

## Development
- All API endpoints return JSON responses
- Error handling returns appropriate HTTP status codes
- Client-side JavaScript uses DOMContentLoaded to ensure page is fully loaded
- Form submissions use JSON payloads
- Database operations include proper foreign key constraint handling

## Security Considerations
- CORS is enabled to allow frontend-backend communication
- Input validation is performed on both frontend and backend
- SQL injection is mitigated through parameterized queries

## Troubleshooting
- If you encounter import errors, ensure you've installed all dependencies with `pip install -r requirements.txt`
- If the application fails to start, check that the database path is correct and writable
- Make sure no other processes are using port 5000

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a pull request

## License
This project is licensed under the GLP License - see the LICENSE file for details.

# Movie Catalog Application

A Python GUI application for cataloging movies on your hard disk. This application recursively scans directories, extracts genres from directory names, and identifies movie files based on their extensions.

## Features

- **File Management**:
  - Create new database in Documents folder
  - Open existing database
  - Close current database
  - Exit application

- **Movie Cataloging**:
  - Recursive directory scanning
  - Genre extraction from directory names
  - Movie name extraction from filenames
  - Progress tracking during scanning
  - File tree view display

- **Data Persistence**:
  - SQLite database storage
  - CSV export functionality
  - Load from database capability
  - Database state management

- **User Interface**:
  - Modern GUI using tkinter
  - Intuitive menu system
  - Status bar with real-time feedback
  - Enhanced treeview with improved styling
  - Success/error messages
  - Help documentation
  - About dialog with version info
  - Sponsor options

## Installation

No external dependencies required - the application uses Python's built-in modules:
- tkinter (GUI framework)
- sqlite3 (Database management)

## Usage

1. Run the application:
```bash
python main.py
```

2. Database Management:
   - Create a new database from File menu
   - Open an existing database
   - Close current database
   - Exit application

3. Movie Cataloging:
   - Click "Browse" to select your movie directory
   - Click "Scan Movies" to start the scanning process
   - The application will display the progress and show the catalogued movies in a tree view
   - Use "Export to CSV" to save movies to a CSV file
   - Use "Load from Database" to view previously scanned movies

## GUI Features

- Improved layout with labeled frames
- Status bar showing application state and version
- Enhanced treeview with better scrolling
- Proper widget organization
- Improved visual hierarchy
- Better spacing and padding
- Responsive design

## Database Management

- The application uses SQLite for data persistence
- Database operations are thread-safe
- Database state is properly managed
- Multiple database support through file management
- Automatic database creation on first use

## File Management

- Create new database (clears existing data)
- Open existing database files (*.db)
- Close current database connection
- Exit application safely

## Supported Movie File Extensions

- .mp4
- .mkv
- .avi
- .mov

## Database Schema

The application creates a SQLite database (`movies.db`) with the following schema:
```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre TEXT,
    movie_name TEXT,
    path TEXT UNIQUE,
    last_scanned DATETIME
)
```

## UI Components

- File Menu:
  - New Database
  - Open Database
  - Close Database
  - Exit

- Help Menu:
  - Help Documentation
  - About Dialog
  - Sponsor Options

- Main Interface:
  - Directory selection
  - Scan controls
  - Progress bar
  - Movie tree view
  - Database operations buttons
  - Status bar

## Development Setup

For development, you can install optional dependencies:
```bash
pip install -r requirements.txt
```

## Note

The application assumes that your movie files are organized in directories named after their genres. For example:
```
movies/
├── Action/
│   ├── ActionMovie1.mkv
│   └── ActionMovie2.mp4
├── Comedy/
│   ├── ComedyMovie1.mkv
└── Drama/
    └── DramaMovie1.mp4
```

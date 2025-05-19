# Movie Catalog Application

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%26%20Linux-blue.svg)](https://www.python.org/downloads/)

A modern Python GUI application for managing and cataloging your movie collection. This tool helps you organize your movies by automatically scanning directories, extracting genres from folder names, and maintaining a comprehensive database of your collection.

## Key Features

- **Smart Movie Organization**
  - Automatic genre detection from folder names
  - Recursive directory scanning
  - Intelligent movie file recognition
  - Progress tracking during scanning

- **Powerful Database Management**
  - SQLite-based persistent storage
  - Multiple database support
  - Thread-safe operations
  - CSV export functionality
  - Automatic database creation and management

- **Modern User Interface**
  - Clean, intuitive tkinter-based GUI
  - Responsive design
  - Status bar with real-time feedback
  - Enhanced treeview display
  - Platform-specific theming
  - Professional error handling

- **Advanced Features**
  - Database state management
  - File tree view display
  - Progress tracking
  - Success/error notifications
  - Help documentation
  - Version information
  - Sponsor options

## System Requirements

- Python 3.8 or higher
- Windows or Linux operating system
- SQLite3 (included with Python)

## Installation

The application uses Python's built-in modules and requires no external dependencies:

```bash
# Clone the repository
git clone https://github.com/Nsfr750/movie_catalog.git

# Navigate to the project directory
cd movie_catalog

# Run the application
python main.py
```

## Usage Guide

### Database Management
1. Create a new database:
   - Go to File menu > New Database
   - A new database will be created in your Documents folder

2. Open existing database:
   - File menu > Open Database
   - Select your existing *.db file

3. Close current database:
   - File menu > Close Database
   - All unsaved changes will be lost

4. Exit application:
   - File menu > Exit
   - Or click the close button

### Movie Cataloging
1. Select movie directory:
   - Click "Browse" button
   - Navigate to your movie collection folder

2. Start scanning:
   - Click "Scan Movies" button
   - Monitor progress in the status bar
   - View results in the tree view

3. Export data:
   - Click "Export to CSV" button
   - Save your movie collection as a CSV file

4. View existing database:
   - Click "Load from Database" button
   - View previously scanned movies

## Technical Details

### Supported File Formats
The application supports the following movie file extensions:
- `.mp4`
- `.mkv`
- `.avi`
- `.mov`

### Database Structure
The application creates a SQLite database with the following schema:
```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre TEXT,
    movie_name TEXT,
    path TEXT UNIQUE,
    last_scanned DATETIME
)
```

### UI Components

- **File Menu**
  - Database operations
  - Exit application

- **Help Menu**
  - Documentation
  - About dialog
  - Sponsor options

- **Main Interface**
  - Directory selection
  - Scan controls
  - Progress tracking
  - Movie tree view
  - Status bar

## Development

For development purposes, you can install optional dependencies:

```bash
pip install -r requirements.txt
```

## Project Organization

The application assumes your movie files are organized in a structured folder hierarchy:
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

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the [GitHub Issues](https://github.com/Nsfr750/movie_catalog/issues) page.

## Acknowledgments

- Thanks to all contributors and users who have helped improve this project
- Special thanks to the Python community for their excellent documentation and support

## Version History

For detailed version history, please refer to the [CHANGELOG.md](CHANGELOG.md) file.

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
- MySQL (install using pip)

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/movie_catalog.git
   cd movie_catalog
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

3. Configure MySQL database:
   - Open the application
   - Click on "Database" in the menu
   - Configure your MySQL connection settings
   - Click "Save" to apply the configuration

4. Run the application:
   ```bash
   movie-catalog
   ```

### From PyPI

1. Install from PyPI:
   ```bash
   pip install movie-catalog
   ```

2. Run the application:
   ```bash
   movie-catalog
   ```

## Configuration

The application uses MySQL as its database backend. You can configure the database settings through the GUI:

1. Click "Database" in the menu
2. Click "Configure Database"
3. Enter your MySQL connection details:
   - Host (default: localhost)
   - Username (default: root)
   - Password
   - Database name (default: movie_catalog)
4. Click "Save" to apply the configuration

## Usage

1. Create or open a database:
   - Click "Database" in the menu
   - Choose "New Database" or "Open Database"
   - Follow the configuration wizard

2. Select a directory containing your movies:
   - Click "Browse" to select your movie directory
   - Movies should be organized in genre folders
   - Supported formats: .mp4, .mkv, .avi, .mov, .webm, .mpg, .mpeg, .wmv, .flv, .m4v, .vob, .divx

3. Click "Scan Movies" to scan for movies:
   - Progress will be shown in the progress bar
   - Status updates will appear in the status bar
   - Movies will be automatically organized by genre

4. Use the tree view to browse your collection:
   - Movies are displayed with genre, name, and path
   - Export your collection to CSV using the "File" menu
   - Use "Help" menu for more information

## Database Configuration

The application uses MySQL as its database backend. You can configure the database settings through the GUI:

1. Click "Database" in the menu
2. Click "Configure Database"
3. Enter your MySQL connection details:
   - Host (default: localhost)
   - Username (default: root)
   - Password
   - Database name (default: movie_catalog)
4. Click "Save" to apply the configuration

## Supported Video Formats

The application supports the following video file formats:
- .mp4 (MPEG-4)
- .mkv (Matroska)
- .avi (Audio Video Interleave)
- .mov (QuickTime)
- .webm (WebM)
- .mpg (MPEG-1)
- .mpeg (MPEG)
- .wmv (Windows Media Video)
- .flv (Flash Video)
- .m4v (MPEG-4 Video)
- .vob (Video Object)
- .divx (DivX)

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
- `.webm`
- `.mpg`
- `.mpeg`
- `.wmv`
- `.flv`
- `.m4v`
- `.vob`
- `.divx`

### Database Structure
The application creates a MySQL database with the following schema:
```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre TEXT,
    movie_name TEXT,
    path TEXT UNIQUE,
    last_scanned DATETIME
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors
- Special thanks to the Python community
- Special thanks to sponsors who support this project

## Version

Current version: 1.6.0

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

## Development

For development, install the package with development dependencies:

```bash
pip install -e ".[dev]"
```

This will install all required dependencies for development, including:
- Code formatting tools (black, isort)
- Linters (flake8, pylint)
- Type checking (mypy)
- Testing tools (pytest, pytest-cov)
- Documentation tools (sphinx)

### Running Tests

To run the test suite:

```bash
pytest tests/
```

### Building Documentation

The documentation is located in the `docs/` directory and can be built using Sphinx:

```bash
sphinx-build -b html docs/ docs/_build/html
```

## Version History

For detailed version history, please refer to the [CHANGELOG.md](CHANGELOG.md) file.

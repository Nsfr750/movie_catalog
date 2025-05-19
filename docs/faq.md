# Frequently Asked Questions

## General Questions

### What is Movie Catalog?
Movie Catalog is a Python application that helps you organize and manage your movie collection. It scans your movie files, categorizes them by genre, and provides tools to view and export your collection.

### What platforms does it support?
Movie Catalog works on:
- Windows
- Linux
- Any platform that supports Python 3.8+

### What video formats are supported?
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

## Installation

### How do I install Movie Catalog?
You can install Movie Catalog in two ways:

1. From PyPI:
   ```bash
   pip install movie-catalog
   ```

2. From source:
   ```bash
   git clone https://github.com/Nsfr750/movie_catalog.git
   cd movie_catalog
   pip install -e .
   ```

### What dependencies are required?
Required dependencies:
- Python 3.8 or higher
- MySQL 8.0 or higher
- tkinter (included with Python)
- mysql-connector-python
- pillow

### How do I configure the database?
1. Open Movie Catalog
2. Click "Database" in the menu
3. Click "Configure Database"
4. Enter your MySQL connection details
5. Click "Save" to apply the configuration

## Usage

### How do I organize my movies?
The application expects movies to be organized in a folder structure like:
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

### How do I scan my movies?
1. Click "Browse" to select your movie directory
2. Click "Scan Movies" to start scanning
3. Progress will be shown in the progress bar
4. Movies will be automatically organized by genre

### Can I export my collection?
Yes! You can export your movie collection to CSV format:
1. Click "File" in the menu
2. Select "Export to CSV"
3. Choose a location to save the file
4. The file will contain genre, movie name, path, and scan date

## Troubleshooting

### The application won't start
1. Check if Python is installed correctly
2. Verify all dependencies are installed
3. Check if MySQL is running
4. Review the error messages in the status bar

### Database connection fails
1. Verify MySQL is running
2. Check your connection settings
3. Ensure the user has proper permissions
4. Check the error message for more details

### Movies aren't being found
1. Check if files are in supported formats
2. Verify folder structure
3. Check if files have proper permissions
4. Review the scan progress in the status bar

### The application is slow
1. Close other applications
2. Ensure MySQL has enough resources
3. Use proper indexing in the database
4. Consider upgrading your hardware

## Development

### How can I contribute?
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### What are the development requirements?
Development requirements include:
- Python 3.8+
- Development dependencies (black, isort, pytest, etc.)
- MySQL for testing
- Git for version control

### How do I run the tests?
```bash
pytest tests/
```

## Support

### How do I get help?
1. Check the documentation
2. Search existing issues
3. Create a new issue on GitHub
4. Join the community discussion

### Where can I find more information?
- [GitHub Repository](https://github.com/Nsfr750/movie_catalog)
- [Documentation](https://nsfr750.github.io/movie_catalog)
- [Issue Tracker](https://github.com/Nsfr750/movie_catalog/issues)

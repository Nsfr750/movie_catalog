# Getting Started with Movie Catalog

## System Requirements

- Python 3.8 or higher
- MySQL 8.0 or higher
- Windows or Linux operating system

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

3. Configure MySQL:
   - Ensure MySQL is installed and running
   - Create a user with appropriate permissions
   - Note down the connection details (host, username, password)

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

## Development Setup

For development, install the package with development dependencies:

```bash
pip install -e ".[dev]"
```

This will install all required development tools including:
- Code formatters (black, isort)
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

To build the documentation:

```bash
sphinx-build -b html docs/ docs/_build/html
```

The built documentation will be available in `docs/_build/html/`

## Initial Setup

1. Database Configuration:
   - Launch the application
   - Click "Database" in the menu
   - Configure your MySQL connection:
     - Host (default: localhost)
     - Username (default: root)
     - Password
     - Database name (default: movie_catalog)
   - Click "Save" to apply the configuration

2. Movie Directory Organization:
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

## Basic Usage

1. Create or Open Database:
   - Click "Database" in the menu
   - Choose "New Database" or "Open Database"
   - Follow the configuration wizard

2. Scan Movies:
   - Click "Browse" to select your movie directory
   - Click "Scan Movies" to start scanning
   - Progress will be shown in the progress bar
   - Status updates will appear in the status bar

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

# API Reference

This document provides a reference for the core classes and functions in the Movie Catalog application.

## `main.MovieCatalogApp`

The main application class that orchestrates the GUI and all backend components.

- `__init__(self, root)`: Initializes the main application window, database, and UI components.
- `set_language(self, lang_code)`: Sets the application language and triggers a UI text update.
- `update_ui_texts(self)`: Updates all text in the UI to the currently selected language.
- `create_widgets(self)`: Creates all the main GUI components.
- `browse_directory(self)`: Opens a dialog to select the movie directory.
- `scan_movies(self)`: Starts the movie scanning process in a separate thread.
- `load_movies_from_db(self)`: Loads and displays all movies from the database.
- `export_to_csv(self)`: Exports the movie list to a CSV file.

## `struttura.menu.AppMenu`

Handles the creation and management of the application's menu bar.

- `__init__(self, app)`: Initializes the menu and links it to the main app.
- `create_menu(self)`: Creates the File, Language, and Help menus.
- `update_menu_text(self)`: Updates the text of all menu items when the language changes.
- `show_about_dialog(self)`: Displays the 'About' dialog.
- `show_help_dialog(self)`: Displays the 'Help' dialog.
- `show_sponsor_dialog(self)`: Displays the 'Sponsor' dialog.

## `struttura.db.MySQLDatabase`

Manages all interactions with the MySQL database.

- `__init__(self, root)`: Initializes the database configuration.
- `create_connection(self)`: Establishes a connection to the database.
- `create_tables(self)`: Creates the `movies` table if it doesn't exist.
- `add_movie(self, genre, movie_name, path)`: Adds a single movie to the database.
- `get_all_movies(self)`: Retrieves all movies from the database.
- `store_scanned_files(self, files)`: Stores a batch of scanned movie files in the database.

## `struttura.db.MySQLConfig`

Manages the database connection settings.

- `__init__(self, root)`: Loads the configuration from `mysql_config.json` or uses defaults.
- `load_config(self)`: Loads the database configuration from the JSON file.
- `save_config(self, config)`: Saves the current configuration to the JSON file.
- `show_config_form(self)`: Displays a dialog for the user to edit the database configuration.

## `lang.lang`

Provides functions for localization.

- `set_language(lang_code)`: Sets the active language ('en' or 'it').
- `get_string(key)`: Retrieves a string for the given key in the active language.

## API Usage Example

```python
# Initialize application
app = MovieCatalogApp(root)

# Configure database
db_config = MySQLConfig(root)
config = db_config.show_config_form()
if config:
    db_config.save_config(config)

# Start movie scanning
scanner = MovieScanner(root_path="/path/to/movies", queue=app.result_queue)
scanner.scan()

# Export to CSV
app.export_to_csv("movies.csv")
```

## Supported File Formats

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

## Error Handling

### Common Exceptions

```python
# Database errors
class DatabaseError(Exception):
    """Base class for database-related errors."""
    
class ConnectionError(DatabaseError):
    """Database connection error."""
    
class ConfigurationError(DatabaseError):
    """Database configuration error."""

# File handling errors
class FileError(Exception):
    """Base class for file-related errors."""
    
class UnsupportedFormat(FileError):
    """Unsupported file format."""
    
class PermissionError(FileError):
    """File permission error."""

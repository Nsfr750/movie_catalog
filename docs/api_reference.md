# API Reference

## Database API

### Database Class

```python
class Database:
    def __init__(self, root):
        """Initialize the database with a root window reference.
        
        Args:
            root (tk.Tk): The root Tkinter window
        """
        
    def initialize(self) -> bool:
        """Initialize the database connection.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        
    def add_movie(self, genre: str, movie_name: str, path: str) -> bool:
        """Add a movie to the database.
        
        Args:
            genre (str): Movie genre
            movie_name (str): Movie name
            path (str): Full path to the movie file
            
        Returns:
            bool: True if movie was added successfully, False otherwise
        """
        
    def get_all_movies(self) -> List[Tuple[str, str, str]]:
        """Get all movies from the database.
        
        Returns:
            List[Tuple[str, str, str]]: List of tuples containing (genre, movie_name, path)
        """
        
    def export_to_csv(self, filename: str) -> bool:
        """Export movies to CSV file.
        
        Args:
            filename (str): Path to the CSV file
            
        Returns:
            bool: True if export was successful, False otherwise
        """

### MovieScanner Class

```python
class MovieScanner:
    def __init__(self, root_path: str, queue: Queue):
        """Initialize the movie scanner.
        
        Args:
            root_path (str): Root directory to scan
            queue (Queue): Queue for communication with GUI
        """
        
    def scan(self) -> None:
        """Scan the directory for movies.
        
        Scans the root directory and all subdirectories for supported video files.
        Progress is reported through the queue.
        """

## GUI Components

### MovieCatalogApp Class

```python
class MovieCatalogApp:
    def __init__(self, root):
        """Initialize the main application window.
        
        Args:
            root (tk.Tk): The root Tkinter window
        """
        
    def create_menu(self) -> None:
        """Create the application menu."""
        
    def load_movies_from_database(self) -> None:
        """Load movies from database into treeview."""
        
    def start_scan(self) -> None:
        """Start scanning for movies."""
        
    def process_results(self) -> None:
        """Process scan results and update GUI."""
        
    def export_to_csv(self) -> None:
        """Export movies to CSV file."""

## Configuration

### MySQLConfig Class

```python
class MySQLConfig:
    def __init__(self, root=None):
        """Initialize MySQL configuration.
        
        Args:
            root (tk.Tk, optional): The root Tkinter window
        """
        
    def show_config_form(self) -> dict:
        """Show configuration dialog and return settings.
        
        Returns:
            dict: Database configuration settings
        """
        
    def save_config(self, config: dict) -> bool:
        """Save configuration to file.
        
        Args:
            config (dict): Configuration settings
            
        Returns:
            bool: True if save was successful, False otherwise
        """

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

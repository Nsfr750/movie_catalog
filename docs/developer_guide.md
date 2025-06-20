# Developer Guide

This guide provides technical details about the project's architecture, code structure, and development practices.

## Project Architecture

The application follows a modular architecture, with a clear separation of concerns between the UI, core logic, and data layers.

### Core Components

- **`main.py`**: The main entry point of the application. It contains the `MovieCatalogApp` class which initializes the GUI and orchestrates the different components.

- **`struttura` Package**: This is a central package containing the core backend logic and shared components.
  - **`db.py`**: Manages all database interactions. The `MySQLDatabase` class handles connections, table creation, and CRUD operations.
  - **`menu.py`**: The `AppMenu` class encapsulates all logic for creating and managing the application's menu bar.
  - **`version.py`**: Provides version information for the application.
  - **`about.py` / `help.py` / `sponsor.py`**: These modules contain the classes for their respective UI dialogs.

- **`lang` Package**:
  - **`lang.py`**: Handles localization. It contains dictionaries for English and Italian strings and functions to switch the language at runtime.

### UI Layer

- The user interface is built using Python's standard `tkinter` library, with the themed `ttk` widgets for a modern look and feel.
- The main application window and its components are created in `main.py`.
- Dialogs for 'About', 'Help', and 'Sponsor' are encapsulated in their own classes within the `struttura` package.

### Data Layer

- The application uses a MySQL database for persistent storage.
- The `MySQLConfig` class in `struttura/db.py` handles loading and saving the database connection configuration from a `mysql_config.json` file.
- All SQL queries are managed within the `MySQLDatabase` class.

## Development Workflow

1.  **Code Style**: The project uses `black` for code formatting to ensure consistency.
2.  **Dependencies**: Project dependencies are managed in `requirements.txt`.
3.  **Branching**: Follow standard Git branching practices (e.g., feature branches for new development).
4.  **Documentation**: Keep the documentation in the `/docs` folder updated with any significant changes.

## How to Contribute

- See `CONTRIBUTING.md` for detailed guidelines on how to contribute to the project.

## Project Structure

```
movie_catalog/
├── docs/              # Documentation
├── src/              # Source code
│   ├── main.py       # Main application
│   ├── struttura/    # Core backend logic and shared components
│   │   ├── db.py     # Database operations
│   │   ├── menu.py   # Application menu
│   │   ├── version.py # Version information
│   │   ├── about.py  # About dialog
│   │   ├── help.py   # Help dialog
│   │   └── sponsor.py # Sponsor dialog
│   └── lang/         # Localization
│       └── lang.py   # Localization logic
├── tests/            # Test files
├── requirements.txt  # Project dependencies
└── setup.py          # Package configuration
```

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/movie_catalog.git
   cd movie_catalog
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install development tools:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints
- Implement docstrings
- Use meaningful variable names

### Documentation
- Use markdown for documentation
- Follow consistent formatting
- Keep examples up to date
- Document all public APIs

## Testing

### Unit Tests
- Located in `tests/` directory
- Use pytest framework
- Cover core functionality
- Include integration tests

### Running Tests
```bash
pytest tests/
```

## Contributing

### Pull Requests
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Update documentation
6. Submit pull request

### Code Review
- Follow code style guidelines
- Ensure tests pass
- Check documentation
- Verify error handling

## API Reference

### Database API
```python
class Database:
    def initialize(self) -> bool:
        """Initialize database connection."""
        pass
    
    def add_movie(self, genre: str, movie_name: str, path: str) -> bool:
        """Add a movie to the database."""
        pass
    
    def get_all_movies(self) -> List[Tuple[str, str, str]]:
        """Get all movies from database."""
        pass
```

### GUI Components
```python
class MovieCatalogApp:
    def create_menu(self) -> None:
        """Create application menu."""
        pass
    
    def load_movies_from_database(self) -> None:
        """Load movies from database."""
        pass
    
    def process_results(self) -> None:
        """Process scan results."""
        pass
```

## Best Practices

### Error Handling
- Use try-except blocks
- Provide meaningful error messages
- Implement graceful degradation
- Log errors appropriately

### Performance
- Use efficient database queries
- Implement caching where appropriate
- Optimize file operations
- Handle large datasets efficiently

### Security
- Validate user input
- Use secure database connections
- Implement proper error handling
- Follow secure coding practices

## Version Control

### Branching Strategy
- `main`: Stable releases
- `develop`: Development
- `feature/*`: New features
- `hotfix/*`: Critical fixes
- `release/*`: Release preparation

### Commit Messages
- Use imperative mood
- Keep messages concise
- Include issue numbers
- Follow conventional commits

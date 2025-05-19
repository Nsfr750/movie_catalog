# Developer Guide

## Project Structure

```
movie_catalog/
├── docs/              # Documentation
├── src/              # Source code
│   ├── main.py       # Main application
│   ├── db.py         # Database operations
│   └── help.py       # Help system
├── tests/            # Test files
├── requirements.txt  # Project dependencies
└── setup.py          # Package configuration
```

## Core Components

### Database System
- Uses MySQL as backend
- Provides configuration dialog
- Supports database migrations
- Implements error handling

### GUI Components
- Built with tkinter
- Uses ttk for modern look
- Implements status updates
- Supports multiple dialogs

### File Handling
- Supports multiple video formats
- Implements progress tracking
- Handles large file collections
- Provides error recovery

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

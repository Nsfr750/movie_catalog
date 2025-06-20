"""
Configuration management for the Movie Catalog application.
"""
import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

# Default configuration
DEFAULT_CONFIG = {
    'app': {
        'language': 'en',
        'theme': 'system',
        'window_width': 1000,
        'window_height': 700,
        'window_x': None,
        'window_y': None,
        'window_maximized': False,
    },
    'logging': {
        'level': 'INFO',
        'file': 'logs/movie_catalog.log',
        'max_size': 5,  # MB
        'backup_count': 5,
    },
    'database': {
        'last_used': None,
        'recent_files': [],
    },
    'updates': {
        'check_on_startup': True,
        'last_checked': None,
        'last_version': None,
    },
}

class Config:
    """Configuration manager for the application."""
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialize the configuration manager.
        
        Args:
            config_file: Path to the configuration file.
        """
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
        self._load()
    
    def _load(self) -> None:
        """Load configuration from file or create a new one with defaults."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self._migrate_config()
            else:
                self.config = DEFAULT_CONFIG.copy()
                self._save()
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            self.config = DEFAULT_CONFIG.copy()
    
    def _migrate_config(self) -> None:
        """Migrate old config versions to current format."""
        # Add any missing default values
        for section, values in DEFAULT_CONFIG.items():
            if section not in self.config:
                self.config[section] = values.copy()
            else:
                if isinstance(values, dict):
                    for key, default_value in values.items():
                        if key not in self.config[section]:
                            self.config[section][key] = default_value
    
    def _save(self) -> None:
        """Save the current configuration to file."""
        try:
            os.makedirs(self.config_file.parent, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.
        
        Example: get('app.language')
        """
        try:
            keys = key.split('.')
            value = self.config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any, save: bool = True) -> None:
        """Set a configuration value using dot notation.
        
        Args:
            key: The configuration key in dot notation (e.g., 'app.language')
            value: The value to set
            save: Whether to save the configuration to disk immediately
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        if save:
            self._save()
    
    def get_recent_files(self) -> list[str]:
        """Get the list of recently used database files."""
        return self.get('database.recent_files', [])
    
    def add_recent_file(self, file_path: str) -> None:
        """Add a file to the recent files list."""
        recent = self.get_recent_files()
        if file_path in recent:
            recent.remove(file_path)
        recent.insert(0, file_path)
        # Keep only the 10 most recent files
        self.set('database.recent_files', recent[:10])
    
    def get_language(self) -> str:
        """Get the current language setting."""
        return self.get('app.language', 'en')
    
    def set_language(self, lang_code: str) -> None:
        """Set the application language."""
        self.set('app.language', lang_code)
    
    def get_theme(self) -> str:
        """Get the current theme setting."""
        return self.get('app.theme', 'system')
    
    def set_theme(self, theme: str) -> None:
        """Set the application theme."""
        self.set('app.theme', theme)
    
    def get_window_geometry(self) -> tuple[Optional[int], Optional[int], int, int, bool]:
        """Get the window geometry settings.
        
        Returns:
            Tuple of (x, y, width, height, maximized)
        """
        return (
            self.get('app.window_x'),
            self.get('app.window_y'),
            self.get('app.window_width', 1000),
            self.get('app.window_height', 700),
            self.get('app.window_maximized', False)
        )
    
    def set_window_geometry(self, x: int, y: int, width: int, height: int, maximized: bool = False) -> None:
        """Set the window geometry settings."""
        self.set('app.window_x', x, save=False)
        self.set('app.window_y', y, save=False)
        self.set('app.window_width', width, save=False)
        self.set('app.window_height', height, save=False)
        self.set('app.window_maximized', maximized)
    
    def get_logging_config(self) -> dict[str, Any]:
        """Get the logging configuration."""
        return {
            'level': self.get('logging.level', 'INFO'),
            'file': self.get('logging.file', 'logs/movie_catalog.log'),
            'max_size': self.get('logging.max_size', 5) * 1024 * 1024,  # Convert to bytes
            'backup_count': self.get('logging.backup_count', 5),
        }

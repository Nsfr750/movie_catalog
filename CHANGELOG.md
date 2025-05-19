# Changelog

All notable changes to this project will be documented in this file.

## [1.5.0] - 2025-05-19
### Added
- Database creation in user's Documents folder
- Improved error handling for database operations
- Tree view initialization checks

### Changed
- Removed custom theme system for simpler GUI
- Improved database path handling
- Better error messages for database operations

### Fixed
- Tree view initialization errors
- Database creation permission issues
- GUI component initialization order

## [1.4.0] - 2025-05-19
### Added
- Modern GUI theme system
- Improved window layout with labeled frames
- Status bar with version information
- Enhanced treeview styling
- Platform-specific theming
- Better widget organization

### Changed
- Increased window size for better visibility
- Improved responsive design
- Better visual hierarchy
- Enhanced user feedback through status messages
- Improved progress bar layout
- Added proper padding and spacing

### Fixed
- Various UI layout issues
- Widget alignment problems
- Status bar visibility
- Treeview scrolling behavior

## [1.3.0] - 2025-05-19
### Added
- File menu with database management options
- New Database creation
- Open existing database
- Close database functionality
- Exit application option
- Improved database state handling

### Changed
- Enhanced error handling for database operations
- Added database state checks before operations
- Improved UI feedback with success/error messages
- Better organization of menu items

## [1.2.0] - 2025-05-19
### Added
- Database functionality using SQLite
- CSV export feature
- Load from database functionality
- Thread-safe database operations
- Help menu with documentation
- About dialog with version info
- Sponsor options

### Changed
- Replaced PyQt6 with tkinter for better Windows compatibility
- Improved error handling for database operations
- Enhanced UI layout with better button organization

## [1.1.0] - 2025-05-19
### Added
- Initial implementation with basic movie scanning
- Directory browsing
- Progress tracking
- Tree view display of results
- Genre and movie name extraction

### Changed
- Switched from PyQt6 to tkinter GUI framework

## [1.0.0] - 2025-05-19
### Added
- Initial version with basic movie cataloging functionality
- Recursive directory scanning
- File extension filtering (.mp4, .mkv, .avi, .mov)
- Basic UI with progress tracking

# 📋 Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.8.2] - 2025-06-22 

### Added
- Italian language support with complete UI translation
- Search functionality improvements including handling of tuple and dictionary formats
- Enhanced error handling for database operations
- Added comprehensive logging throughout the application
- New CHANGELOG.md to track all changes
- Added TO_DO.md to track future improvements and features
- Added requirements.txt for better dependency management

### Changed
- Refactored database handling code for better maintainability
- Improved error messages and user feedback
- Updated README.md with latest features and setup instructions
- Optimized search performance with better data handling

### Fixed
- Fixed 'tuple' object has no attribute 'get' error in search functionality
- Fixed language file loading issues
- Resolved database connection handling problems
- Fixed sorting issues in the movie list view
- Addressed various UI layout and responsiveness issues

### Removed
- Removed unused dependencies and code
- Cleaned up old configuration files

### Security
- Updated dependencies to address known vulnerabilities
- Improved error handling to prevent information leakage


## [1.8.1] - 2024-02-06

### Fixed
- Fixed critical issue with database connection handling
- Resolved problem with movie metadata not being saved correctly
- Addressed issue with duplicate movie entries
- Fixed sorting functionality in the movie list
- Resolved problem with movie poster display
- Fixed issues with the search functionality
- Addressed problem with special characters in movie titles
- Resolved issue with date formatting in different locales
- Fixed problem with application freezing during database operations
- Addressed issue with incorrect movie count display


## [1.8.0] - 2024-02-05

### Added
- Initial release of Movie Catalog
- Basic movie management functionality
- Support for adding, editing, and deleting movies
- Basic search and filter capabilities
- Simple user interface built with Tkinter
- SQLite database for storing movie information
- Basic error handling and user feedback
- Simple configuration management
- Basic logging functionality
- Initial documentation

### Changed
- Improved database schema for better performance
- Enhanced user interface with better organization
- Updated error messages for better clarity
- Improved input validation
- Better handling of application state
- Enhanced logging with more detailed information
- Updated documentation with more examples
- Improved error recovery mechanisms
- Better handling of application settings
- Enhanced data validation

### Fixed
- Fixed issue with movie deletion not working
- Resolved problem with search not returning results
- Addressed issue with application crashing on invalid input
- Fixed problem with database locking
- Resolved issue with date formatting
- Fixed problem with special characters in search
- Addressed issue with window resizing
- Fixed problem with application not starting on some systems
- Resolved issue with configuration file handling
- Fixed problem with logging configuration


## [1.7.2] - 2025-06-22 

### Added
- Full Italian language support with complete UI translation
- Dynamic language switching between English and Italian
- New language module for managing translations
- Added Italian language JSON file (it.json)
- Language selection in settings dialog
- Automatic language detection based on system settings
- Support for right-to-left (RTL) languages in the UI
- Added language-specific date and number formatting
- Documentation for adding new languages
- Unit tests for language switching functionality

### Changed
- Refactored UI text to use language strings from JSON files
- Updated settings dialog to include language selection
- Improved error messages with support for multiple languages
- Modified database schema to support multilingual content
- Updated documentation to reflect new language features
- Enhanced logging for language-related operations
- Improved string formatting to support different languages
- Updated build process to include language files
- Modified search functionality to work with translated content
- Enhanced settings persistence for language preferences

### Fixed
- Fixed issue with special characters in translated strings
- Resolved layout issues with different text lengths in translations
- Fixed database queries to handle multilingual content
- Addressed performance issues with language switching
- Fixed issues with date and number formatting in different locales
- Resolved problems with right-to-left text rendering
- Fixed issues with text alignment in translated content
- Addressed problems with string encoding in different languages
- Fixed issues with text truncation in translated UI elements
- Resolved problems with keyboard shortcuts in different keyboard layouts


## [1.7.1] - 2025-07-01

### Added
- Movie Metadata: Added TMDB integration for fetching movie details
  - Movie posters and backdrops
  - Plot summaries and ratings
  - Cast and crew information
  - Genres and release years
- Image Handling: Added support for downloading and displaying movie posters
- Search Functionality: Integrated TMDB search API

### Changed
- Database Schema: Updated to support comprehensive movie metadata
  - Added fields for TMDB integration
  - Improved data types and constraints
  - Added proper indexing for better performance
- UI Enhancements: 
  - Added movie details dialog
  - Improved movie list display with metadata
  - Better error handling and user feedback

### Fixed
- Fixed MySQL connection and schema initialization
- Resolved issues with database migrations
- Improved error handling for API requests
- Fixed image loading and caching


## [1.7.0] - 2025-06-20

### Added
- Multilingual Support: Added dynamic language switching between English and Italian
- Language Menu: New menu for selecting the application language at runtime
- `struttura` Package: Created a new package to house core application logic
- `requirements.txt`: Added a file to manage project dependencies
- Sponsor Dialog: Added support for project sponsorship through various platforms
- Improved Error Handling: Better error messages and recovery mechanisms

### Changed
- Project Structure: Refactored modules into the `struttura` package
- Menu Logic: Moved all menu creation into `AppMenu` class
- Dialogs as Classes: Refactored dialogs from static methods to classes
- UI Updates: All UI text now updates dynamically on language change
- Code Organization: Improved code structure and documentation

### Fixed
- Fixed `AttributeError` on startup
- Fixed `TypeError` in dialogs
- Fixed language switching issues
- Improved window management
- Fixed memory leaks in dialog handling


## [1.6.0] - 2025-05-19

### Added
- Tree view for displaying movies with genre, name, and path
- Progress tracking during scanning
- Status bar showing current application state
- Export to CSV functionality
- Help and About dialogs
- Sponsorship feature
- Improved error handling and user feedback
- MySQL database support with configuration dialog
- Support for additional video file formats
- Package configuration with setup.py
- Command line interface support
- Development environment setup

### Changed
- Improved database initialization and configuration
- Enhanced movie scanning algorithm
- Better GUI organization and component management
- Updated help documentation with new features
- Updated installation instructions

### Fixed
- Resolved CSV export issues
- Fixed database connection handling
- Improved error messages for file operations
- Fixed window resizing issues
- Addressed memory management in long-running operations

- 📤 Resolved CSV export issues
- 🗃️ Fixed database connection handling
- 💬 Improved error messages for file operations
- 🖥️ Fixed window resizing issues
- ⚡ Addressed memory management in long-running operations


## [1.5.0] - 2025-05-19


### 🆕 Added

- 🎬 Initial version with basic movie catalog functionality
- 🗃️ SQLite database support
- 🖥️ Basic GUI implementation
- 🔍 File scanning capability
- 🛡️ Basic error handling


### 🔄 Changed

- 🏗️ Initial project structure
- ⚙️ Basic configuration system
- 📝 Initial documentation


### 🐛 Fixed

- 🐞 Initial bug fixes


[Unreleased]: https://github.com/Nsfr750/movie_catalog/compare/v1.7.2...HEAD
[1.7.2]: https://github.com/Nsfr750/movie_catalog/compare/v1.7.1...v1.7.2
[1.7.1]: https://github.com/Nsfr750/movie_catalog/compare/v1.7.0...v1.7.1
[1.7.0]: https://github.com/Nsfr750/movie_catalog/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/Nsfr750/movie_catalog/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/Nsfr750/movie_catalog/compare/v1.4.0...v1.5.0

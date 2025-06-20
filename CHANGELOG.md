# 📋 Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased] 🚧


### 🆕 Added

- 🎬 **Movie Metadata**: Added TMDB integration for fetching movie details
  - 🖼️ Movie posters and backdrops
  - 📝 Plot summaries and ratings
  - 🎭 Cast and crew information
  - 🏷️ Genres and release years
- 🖼️ **Image Handling**: Added support for downloading and displaying movie posters
- 🔍 **Search Functionality**: Integrated TMDB search API
- ✨ **Update System**: Added automatic update checking with GitHub integration
- ⚙️ **Settings Dialog**: New tabbed settings dialog for application configuration
- 📝 **Logging System**: Comprehensive logging with log viewer interface
- 🔧 **Configuration Management**: Persistent application settings storage


### 🔄 Changed

- 🗃️ **Database Schema**: Updated to support comprehensive movie metadata
  - Added fields for TMDB integration
  - Improved data types and constraints
  - Added proper indexing for better performance
- 🎨 **UI Enhancements**: 
  - Added movie details dialog
  - Improved movie list display with metadata
  - Better error handling and user feedback


### 🐛 Fixed

- 🛠️ Fixed MySQL connection and schema initialization
- 🔄 Resolved issues with database migrations
- 🌐 Improved error handling for API requests
- 🖼️ Fixed image loading and caching
- 🛠️ Fixed sponsor dialog close button functionality
- 🔄 Resolved duplicate tree view creation issue
- 🌐 Fixed language switching for all UI elements
- 🐞 Improved error handling in database operations
- 🔄 Fixed circular import issues in package structure


## [1.7.2] - 2025-07-01 🚀


### 🆕 Added

- 🎬 **Movie Metadata**: Added TMDB integration for fetching movie details
  - 🖼️ Movie posters and backdrops
  - 📝 Plot summaries and ratings
  - 🎭 Cast and crew information
  - 🏷️ Genres and release years
- 🖼️ **Image Handling**: Added support for downloading and displaying movie posters
- 🔍 **Search Functionality**: Integrated TMDB search API


### 🔄 Changed

- 🗃️ **Database Schema**: Updated to support comprehensive movie metadata
  - Added fields for TMDB integration
  - Improved data types and constraints
  - Added proper indexing for better performance
- 🎨 **UI Enhancements**: 
  - Added movie details dialog
  - Improved movie list display with metadata
  - Better error handling and user feedback


### 🐛 Fixed

- 🛠️ Fixed MySQL connection and schema initialization
- 🔄 Resolved issues with database migrations
- 🌐 Improved error handling for API requests
- 🖼️ Fixed image loading and caching


## [1.7.1] - 2025-06-20 🚀


### 🆕 Added

- 🔄 **Update System**: Automatic version checking and update notifications
- ⚙️ **Settings Dialog**: User-configurable application settings
  - 🎨 Theme selection (Light/Dark/System)
  - 🌐 Language selection (English/Italian)
  - 📝 Logging configuration
  - 🔄 Update preferences
- 📝 **Logging System**:
  - 📊 Configurable log levels
  - 🔄 Log file rotation
  - 🔍 Built-in log viewer
- ⚙️ **Configuration Management**:
  - 📋 JSON-based configuration
  - 💾 Persistent settings between sessions
  - ⚡ Default value handling


### 🔄 Changed

- 🏗️ **Project Structure**:
  - 📦 Moved version information to `__init__.py`
  - 🧩 Better module organization
  - 🔄 Improved import structure
- 💬 **User Interface**:
  - 🎨 Updated theme support
  - 🌐 Enhanced language switching
  - 📱 Improved responsive design


### 🐛 Fixed

- 🛠️ Fixed sponsor dialog close functionality
- 🔄 Resolved duplicate tree view creation
- 🌐 Fixed language switching for all UI elements
- 🐞 Improved error handling in database operations
- 🔄 Fixed circular import issues in package structure


## [1.7.0] - 2025-06-20


### 🆕 Added

- 🌐 **Multilingual Support**: Added dynamic language switching between English and Italian
- 🗣️ **Language Menu**: New menu for selecting the application language at runtime
- 📦 **`struttura` Package**: Created a new package to house core application logic
- 📋 **`requirements.txt`**: Added a file to manage project dependencies
- 💖 **Sponsor Dialog**: Added support for project sponsorship through various platforms
- 🛡️ **Improved Error Handling**: Better error messages and recovery mechanisms


### 🔄 Changed

- 🏗️ **Project Structure**: Refactored modules into the `struttura` package
- 🍔 **Menu Logic**: Moved all menu creation into `AppMenu` class
- 💬 **Dialogs as Classes**: Refactored dialogs from static methods to classes
- 🌍 **UI Updates**: All UI text now updates dynamically on language change
- 📝 **Code Organization**: Improved code structure and documentation


### 🐛 Fixed

- 🚀 Fixed `AttributeError` on startup
- 💬 Fixed `TypeError` in dialogs
- 🌐 Fixed language switching issues
- 🖼️ Improved window management
- 🧹 Fixed memory leaks in dialog handling


## [1.6.0] - 2025-05-19


### 🆕 Added

- 🌳 Tree view for displaying movies with genre, name, and path
- 📊 Progress tracking during scanning
- ℹ️ Status bar showing current application state
- 📤 Export to CSV functionality
- ❓ Help and About dialogs
- 💝 Sponsorship feature
- 🐞 Improved error handling and user feedback
- 🗃️ MySQL database support with configuration dialog
- 🎬 Support for additional video file formats
- 📦 Package configuration with setup.py
- ⌨️ Command line interface support
- 🛠️ Development environment setup


### 🔄 Changed

- 🗃️ Improved database initialization and configuration
- 🔍 Enhanced movie scanning algorithm
- 🖥️ Better GUI organization and component management
- 📝 Updated help documentation with new features
- 📋 Updated installation instructions


### 🐛 Fixed

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

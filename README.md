# 🎬 Movie Catalog

[![GitHub release](https://img.shields.io/badge/release-v1.9.0-green)](https://github.com/Nsfr750/movie_catalog/releases/tag/v1.9.0)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/Nsfr750/movie_catalog/graphs/commit-activity)
[![Last Commit](https://img.shields.io/github/last-commit/Nsfr750/movie_catalog?style=for-the-badge)](https://github.com/Nsfr750/movie_catalog/commits/main)

A modern Python GUI application for managing and cataloging your movie collection, built with Tkinter and MySQL.

## ✨ Features

- 🎥 **Movie Scanning**: Scan directories to find movie files and extract genre and movie names.
- 🎬 **Movie Metadata**: Automatically fetch movie details from TMDB including:
  - 🖼️ High-quality posters and backdrops
  - ⭐ Ratings and reviews
  - 📝 Plot summaries
  - 🎭 Cast and crew information
  - 🏷️ Genres and release years
- 💾 **Database Integration**: Store your movie collection in a MySQL database with comprehensive metadata support.
- 🎨 **Dynamic UI**: A clean and responsive user interface built with `tkinter.ttk`.
- 🌐 **Multilingual Support**: Switch between English and Italian at runtime with complete UI translation.
- 🔍 **Advanced Search**: Powerful search functionality that works across all movie attributes.
- 🔄 **Automatic Updates**: Check for and install application updates.
- ⚙️ **Configurable Settings**: Customize application behavior through a settings dialog.
- 📝 **Logging**: Comprehensive logging system with configurable log levels.
- 📤 **Data Export**: Export your movie catalog to a CSV file.
- 🏗️ **Modular Structure**: Code is organized into a `struttura` package for better maintainability.
- 💖 **Sponsor Support**: Support the project through various platforms directly from the application.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- TMDB API key (for movie metadata) - https://www.themoviedb.org/settings/api

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/movie_catalog.git
   cd movie_catalog
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your MySQL database in `mysql_config.json`:
   ```json
   {
       "host": "localhost",
       "user": "your_username",
       "password": "your_password",
       "database": "movie_catalog"
   }
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## 🏗️ Project Structure

```markdown
movie_catalog/
├── 📁 lang/                 # Language files
│   ├── 🌐 lang.py         # Handles language translations
│   ├── en.json            # English language file
│   ├── it.json            # Italian language file
├── 📁 logs/                # Application logs
│   └── 📄 movie_catalog.log
├── 📁 struttura/           # Core application package
│   ├── 📁 images/           # application images
│   │    └── icon.ico        # Application icon
│   ├── ℹ️ about.py        # 'About' dialog class
│   ├── ⚙️ config.py      # Configuration management
│   ├── 💾 db.py           # Database connection and operations
│   ├── ❓ help.py         # 'Help' dialog class
│   ├── 📊 log_viewer.py   # Log viewing interface
│   ├── 📊 logger.py         # Logging configuration
│   ├── 🍔 menu.py         # Application menu class
│   ├── 🎬 movie_details_dialog.py  # Movie metadata dialog
│   ├── 📽️ movie_metadata.py      # TMDB API integration
│   ├── ⚙️ options.py     # Settings dialog
│   ├── 💝 sponsor.py      # 'Sponsor' dialog class
│   ├── 📊 traceback.py      # Traceback
│   ├── 🔄 updates.py      # Update checking functionality
│   ├── 📊 version.py      # Version information
│   └── __init__.py     # Package initialization
├── 🚀 main.py            # Main application entry point
├── 📋 requirements.txt    # Project dependencies
├── 📖 README.md          # This file
├── 📜 CHANGELOG.md       # Project version history
├── ✅ TO_DO.md           # Development to-do list
├── ⚙️ settings.json      # Application settings
├── ⚙️ updates.json       # Update information
└── ⚙️ mysql_config.json  # MySQL configuration file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.

## 📫 Contact

Nsfr750 - [@Nsfr750](https://github.com/Nsfr750)

Project Link: [https://github.com/Nsfr750/movie_catalog](https://github.com/Nsfr750/movie_catalog)

## 🙏 Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Pillow](https://python-pillow.org/)
- [Requests](https://docs.python-requests.org/)

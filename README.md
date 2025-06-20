# 🎬 Movie Catalog

[![GitHub release](https://img.shields.io/github/v/release/Nsfr750/movie_catalog?style=for-the-badge)](https://github.com/Nsfr750/movie_catalog/releases)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/Nsfr750/movie_catalog/graphs/commit-activity)

A modern Python GUI application for managing and cataloging your movie collection, built with Tkinter and MySQL.

## ✨ Features

- 🎥 **Movie Scanning**: Scan directories to find movie files and extract genre and movie names.
- 💾 **Database Integration**: Store your movie collection in a MySQL database.
- 🎨 **Dynamic UI**: A clean and responsive user interface built with `tkinter.ttk`.
- 🌐 **Multilingual Support**: Switch between English and Italian at runtime.
- 🔄 **Automatic Updates**: Check for and install application updates.
- ⚙️ **Configurable Settings**: Customize application behavior through a settings dialog.
- 📝 **Logging**: Comprehensive logging system with configurable log levels.
- 📤 **Data Export**: Export your movie catalog to a CSV file.
- 🏗️ **Modular Structure**: Code is organized into a `struttura` package for better maintainability.
- 💖 **Sponsor Support**: Support the project through various platforms directly from the application.

## 🏗️ Project Structure

```
movie_catalog/
├── 📁 lang/                 # Language files
│   ├── 🌐 lang.py         # Handles language translations
│   └── __init__.py
├── 📁 logs/                # Application logs
│   └── 📄 app.log
├── 📁 struttura/           # Core application package
│   ├── ℹ️ about.py        # 'About' dialog class
│   ├── ⚙️ config.py      # Configuration management
│   ├── 💾 db.py           # Database connection and operations
│   ├── ❓ help.py         # 'Help' dialog class
│   ├── 📊 log_viewer.py   # Log viewing interface
│   ├── 🍔 menu.py         # Application menu class
│   ├� options.py      # Settings dialog
│   ├── 💝 sponsor.py      # 'Sponsor' dialog class
│   ├── 🔄 updates.py      # Update checking functionality
│   └── __init__.py     # Package initialization
├── 🚀 main.py             # Main application entry point
├── 📋 requirements.txt    # Project dependencies
├── 📖 README.md          # This file
├── 📜 CHANGELOG.md       # Project version history
├── ✅ TO_DO.md           # Development to-do list
└── ⚙️ mysql_config.json  # MySQL configuration file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- Git (for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nsfr750/movie_catalog.git
   cd movie_catalog
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL**
   - Create a new MySQL database
   - Copy `mysql_config.example.json` to `mysql_config.json`
   - Update the database credentials in `mysql_config.json`

4. **Run the application**
   ```bash
   python main.py
   ```

## 📝 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Support

If you find this project useful, consider supporting its development:

[![GitHub Sponsors](https://img.shields.io/badge/Support%20on-GitHub%20Sponsors-ea4aaa?style=for-the-badge&logo=github-sponsors&logoColor=white)](https://github.com/sponsors/Nsfr750)
[![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?style=for-the-badge&logo=paypal)](https://www.paypal.com/donate?hosted_button_id=YOUR_PAYPAL_BUTTON_ID)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📬 Contact

For questions or feedback, please open an issue or contact [Nsfr750](https://github.com/Nsfr750).

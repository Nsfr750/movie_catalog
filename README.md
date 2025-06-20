# Movie Catalog

**Version: 1.7.1**

A modern Python GUI application for managing and cataloging your movie collection, built with Tkinter and MySQL.

## Features

- **Movie Scanning**: Scan directories to find movie files and extract genre and movie names.
- **Database Integration**: Store your movie collection in a MySQL database.
- **Dynamic UI**: A clean and responsive user interface built with `tkinter.ttk`.
- **Multilingual Support**: Switch between English and Italian at runtime.
- **Automatic Updates**: Check for and install application updates.
- **Configurable Settings**: Customize application behavior through a settings dialog.
- **Logging**: Comprehensive logging system with configurable log levels.
- **Data Export**: Export your movie catalog to a CSV file.
- **Modular Structure**: Code is organized into a `struttura` package for better maintainability.
- **Sponsor Support**: Support the project through various platforms directly from the application.

## Project Structure

The project has been refactored for clarity and scalability:

```
movie_catalog/
├── lang/
│   ├── lang.py         # Handles language translations
│   └── __init__.py
├── logs/               # Application logs
│   └── app.log
├── struttura/
│   ├── about.py        # 'About' dialog class
│   ├── config.py       # Configuration management
│   ├── db.py           # Database connection and operations
│   ├── help.py         # 'Help' dialog class
│   ├── log_viewer.py   # Log viewing interface
│   ├── menu.py         # Application menu class
│   ├── options.py      # Settings dialog
│   ├── sponsor.py      # 'Sponsor' dialog class
│   ├── updates.py      # Update checking functionality
│   └── __init__.py     # Makes 'struttura' a package
├── main.py             # Main application entry point
├── requirements.txt    # Project dependencies
├── README.md           # This file
├── CHANGELOG.md        # Project version history
├── TO_DO.md            # Development to-do list
└── mysql_config.json   # MySQL configuration file

## Setup and Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/Nsfr750/movie_catalog.git
    cd movie_catalog
    ```

2.  **Install dependencies:**
    Make sure you have Python 3 installed. Then, install the required packages using pip:
    ```sh
    pip install -r requirements.txt
    ```

3.  **Configure Database:**
    - Make sure MySQL Server is installed and running
    - Run the application and use the Database menu to configure your MySQL connection

4.  **Run the application:**
    ```sh
    python main.py
    ```

## Usage

1. **Add Movies:**
   - Click 'Browse' to select a directory containing your movies
   - Click 'Scan for Movies' to add them to your catalog

2. **View Movies:**
   - Your movies will be displayed in the main window
   - Use the 'Load Database' button to refresh the view

3. **Export Data:**
   - Click 'Export to CSV' to save your movie catalog to a file

4. **Change Language:**
   - Use the Language menu to switch between English and Italian

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Support

If you find this project useful, please consider supporting it through:
- [GitHub Sponsors](https://github.com/sponsors/Nsfr750)
- [Buy Me a Coffee](https://paypal.me/3dmega)
- [Patreon](https://www.patreon.com/Nsfr750)
- [Discord](https://discord.gg/BvvkUEP9)

## Version History

See [CHANGELOG.md](CHANGELOG.md) for a complete version history.

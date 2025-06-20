# Movie Catalog

**Version: 1.7.0**

A modern Python GUI application for managing and cataloging your movie collection, built with Tkinter and MySQL.

## Features

- **Movie Scanning**: Scan directories to find movie files and extract genre and movie names.
- **Database Integration**: Store your movie collection in a MySQL database.
- **Dynamic UI**: A clean and responsive user interface built with `tkinter.ttk`.
- **Multilingual Support**: Switch between English and Italian at runtime.
- **Data Export**: Export your movie catalog to a CSV file.
- **Modular Structure**: Code is organized into a `struttura` package for better maintainability.

## Project Structure

The project has been refactored for clarity and scalability:

```
movie_catalog/
├── lang/
│   ├── lang.py         # Handles language translations
│   └── __init__.py
├── struttura/
│   ├── about.py        # 'About' dialog class
│   ├── db.py           # Database connection and operations
│   ├── help.py         # 'Help' dialog class
│   ├── menu.py         # Application menu class
│   ├── sponsor.py      # 'Sponsor' dialog class
│   ├── version.py      # Version management
│   └── __init__.py     # Makes 'struttura' a package
├── main.py             # Main application entry point
├── requirements.txt    # Project dependencies
├── README.md           # This file
├── CHANGELOG.md        # Project version history
└── TO_DO.md            # Development to-do list
```

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

3.  **Configure the Database:**
    On the first run, the application will prompt you to configure the MySQL database connection details (host, user, password, database name).

## Usage

Run the main application file from the project's root directory:

```sh
python main.py
```

- Use the **Browse** button to select the root directory of your movie collection.
- Click **Scan Movies** to populate the catalog.
- Use the **File** menu for database operations and to exit the application.
- Use the **Language** menu to switch between English and Italian.
- Use the **Help** menu for more information.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the GPL-3.0 License.

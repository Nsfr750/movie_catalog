# Getting Started

This guide will walk you through setting up the Movie Catalog application on your local machine.

## Prerequisites

- Python 3.8 or higher
- `pip` for installing packages
- A running MySQL server instance

## Installation

1.  **Clone the Repository**

    Open your terminal or command prompt and clone the project from GitHub:

    ```sh
    git clone https://github.com/Nsfr750/movie_catalog.git
    cd movie_catalog
    ```

2.  **Install Dependencies**

    Install the required Python packages using the `requirements.txt` file. This will install `mysql-connector-python` and `Pillow`.

    ```sh
    pip install -r requirements.txt
    ```

## Initial Configuration

1.  **Database Setup**

    On the very first launch, the application will automatically prompt you to configure the connection to your MySQL database. You will need to provide:

    - **Host**: The address of your MySQL server (e.g., `localhost`).
    - **User**: Your MySQL username (e.g., `root`).
    - **Password**: Your MySQL password.
    - **Database**: The name for the movie catalog database (e.g., `movie_catalog`). The application will create the database if it does not exist.

2.  **Running the Application**

    Once the dependencies are installed, you can run the application from the project's root directory:

    ```sh
    python main.py
    ```

The main application window should now appear, ready for you to start cataloging your movies.

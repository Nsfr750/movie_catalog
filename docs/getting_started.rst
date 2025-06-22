.. _getting_started:

Getting Started
===============

This guide will help you get started with Movie Catalog, a powerful application for managing your movie collection with TMDB integration.

.. contents:: Table of Contents
   :depth: 3
   :local:
   :backlinks: top

System Requirements
------------------

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: 3.8 or higher
- **Database**: MySQL 8.0+ or MariaDB 10.5+
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Disk Space**: 500MB free space (plus space for your movie collection)

Prerequisites
-------------

1. **Python**
   - Download and install the latest Python 3.8+ from `python.org <https://www.python.org/downloads/>`_
   - During installation, make sure to check "Add Python to PATH"

2. **MySQL/MariaDB**
   - Install `MySQL Community Server <https://dev.mysql.com/downloads/mysql/>`_ or `MariaDB <https://mariadb.org/download/>`_
   - Note down your database credentials (username and password)

3. **TMDB API Key** (Optional but recommended)
   - Create an account at `The Movie Database <https://www.themoviedb.org/>`_
   - Request an API key from your account settings
   - This key will be used to fetch movie metadata automatically

Installation
------------

1. **Clone the repository**

   .. code-block:: bash

      git clone https://github.com/Nsfr750/movie_catalog.git
      cd movie_catalog

2. **Install dependencies**

   .. code-block:: bash

      pip install -r requirements.txt

3. **Database Setup**

   - Create a new MySQL database for Movie Catalog
   - Run the initialization script:

   .. code-block:: bash

      python -m struttura.create_database

4. **Configuration**

   - Copy `.env.example` to `.env`
   - Edit `.env` with your database credentials and TMDB API key

5. **Run the Application**

   .. code-block:: bash

      python main.py

First Run
---------

On first launch, Movie Catalog will:

1. Create the necessary database tables
2. Set up the default configuration
3. Create a log file in the `logs` directory

.. note::
   Make sure your MySQL server is running before starting the application.

.. tip::
   For troubleshooting, check the log file at ``logs/movie_catalog.log`` if you encounter any issues during startup.

      pip install -r requirements.txt

3. Configure your MySQL database:

   - Create a new MySQL database
   - Copy `mysql_config.example.json` to `mysql_config.json`
   - Update the database credentials in `mysql_config.json`

4. (Optional) Configure TMDB API:
   - Get an API key from `TMDB <https://www.themoviedb.org/settings/api>`_
   - Add your API key to the configuration

Running the Application
-----------------------

To start the application:

.. code-block:: bash

   python main.py

Alternatively, if you installed the package:

.. code-block:: bash

   movie-catalog

First Run
---------

On first run, the application will:

1. Initialize the database schema
2. Create necessary directories
3. Set up default configuration

You can then start adding movies to your collection through the intuitive GUI interface.

Basic Usage
-----------

1. **Adding Movies**:
   - Click on "Add Movie" and select a movie file or directory
   - The application will automatically fetch metadata from TMDB

2. **Browsing Collection**:
   - Use the tree view to navigate your collection by genre
   - Search for specific movies using the search bar

3. **Viewing Details**:
   - Double-click on a movie to view detailed information
   - See cast, ratings, and plot summary

4. **Updating Metadata**:
   - Right-click on a movie and select "Update Metadata" to refresh information

Next Steps
----------

- Learn more about :doc:`advanced features <user_guide/advanced_features>`
- Check out the :doc:`developer guide <developer_guide/index>`
- Explore the :doc:`API reference <api_reference/index>`

.. _getting_started:

Getting Started
===============

This guide will help you get started with Movie Catalog, a powerful application for managing your movie collection with TMDB integration.

Installation
------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.8 or higher
- MySQL Server
- TMDB API key (for movie metadata)

Installation Steps
~~~~~~~~~~~~~~~~~~

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/Nsfr750/movie_catalog.git
      cd movie_catalog

2. Install the required dependencies:

   .. code-block:: bash

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

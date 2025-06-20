.. _user_guide:

User Guide
==========

This guide provides detailed information about using Movie Catalog's features and functionality.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   interface_overview
   managing_movies
   searching
   preferences
   keyboard_shortcuts
   advanced_features

Interface Overview
-----------------

The Movie Catalog interface consists of the following main components:

1. **Menu Bar** - Access to all application functions
2. **Toolbar** - Quick access to common actions
3. **Navigation Panel** - Browse your collection by genre
4. **Movie List** - View and manage your movies
5. **Status Bar** - Displays current status and progress

Managing Your Collection
-----------------------

Adding Movies
~~~~~~~~~~~~

1. Click the "Add Movie" button or select "File > Add Movie"
2. Choose a movie file or directory
3. The application will automatically:
   - Scan for movie files
   - Fetch metadata from TMDB
   - Add the movie to your collection

Editing Movie Information
~~~~~~~~~~~~~~~~~~~~~~~~

1. Right-click on a movie
2. Select "Edit Details"
3. Modify the information as needed
4. Click "Save" to apply changes

Deleting Movies
~~~~~~~~~~~~~~

1. Right-click on the movie you want to remove
2. Select "Delete"
3. Confirm the deletion

Searching and Filtering
----------------------

Basic Search
~~~~~~~~~~~

1. Type your search term in the search box
2. Results will update as you type
3. Click the "X" to clear the search

Advanced Search
~~~~~~~~~~~~~~

1. Click the filter icon next to the search box
2. Set your search criteria:
   - Title
   - Year
   - Genre
   - Rating
   - Director
   - Cast
3. Click "Apply" to filter the results

Preferences
----------

Accessing Settings
~~~~~~~~~~~~~~~~~

1. Click "Edit" in the menu bar
2. Select "Preferences"

Available Settings
~~~~~~~~~~~~~~~~~

- **General**
  - Language
  - Theme
  - Default directories

- **Database**
  - Connection settings
  - Backup options

- **TMDB**
  - API key
  - Image settings
  - Preferred language

- **Updates**
  - Check for updates
  - Update channel

Keyboard Shortcuts
----------------

+-----------------+---------------------------------+
| Shortcut        | Action                          |
+=================+=================================+
| Ctrl+N         | Add new movie                  |
+-----------------+---------------------------------+
| Ctrl+O         | Open movie                     |
+-----------------+---------------------------------+
| Delete         | Delete selected movie          |
+-----------------+---------------------------------+
| F5             | Refresh view                   |
+-----------------+---------------------------------+
| Ctrl+F         | Focus search box               |
+-----------------+---------------------------------+
| F1             | Help                           |
+-----------------+---------------------------------+
| Alt+F4         | Exit application               |
+-----------------+---------------------------------+

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

- **Database Connection Issues**
  - Verify MySQL server is running
  - Check database credentials in configuration

- **TMDB API Errors**
  - Verify your API key is valid
  - Check your internet connection

- **Missing Metadata**
  - Try updating the metadata manually
  - Verify the movie title is correct

Getting Help
~~~~~~~~~~~

For additional help, please refer to:

- :doc:`FAQ <faq>`
- :doc:`Troubleshooting Guide <troubleshooting>`
- `GitHub Issues <https://github.com/Nsfr750/movie_catalog/issues>`_

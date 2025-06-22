.. _troubleshooting:

Troubleshooting Guide
===================

This guide helps you resolve common issues with Movie Catalog.

.. contents::
   :depth: 2
   :local:

Common Issues
------------

Application Won't Start
~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**

- Application crashes on launch
- Error messages in the status bar
- Blank window appears

**Solutions**

1. Check Python Installation:

   .. code-block:: bash

      python --version

   - Should show Python 3.8 or higher
   - If not, install from `python.org <https://www.python.org/downloads/>`_


2. Install Dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

3. Check Logs:
   - View ``logs/movie_catalog.log`` for error messages

Database Connection Issues
~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**

- "Cannot connect to database" errors
- Timeout when accessing database
- Missing data in the interface

**Solutions**

1. Verify MySQL Service:
   - Ensure MySQL server is running
   - Check service status:

     .. code-block:: bash

        # Linux
        sudo systemctl status mysql

        # Windows
        services.msc

2. Check Database Credentials:
   - Verify username and password in ``.env``
   - Ensure the database exists and is accessible

3. Test Connection:

   .. code-block:: bash

      mysql -u username -p -h localhost

Metadata Fetching Issues
~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**

- No movie information is retrieved
- Incorrect movie data
- Timeout errors

**Solutions**

1. Check TMDB API Key:
   - Verify API key in settings
   - Get a new key from `TMDB <https://www.themoviedb.org/settings/api>`_ if needed

2. Check Internet Connection:
   - Ensure you have an active internet connection
   - Try accessing `api.themoviedb.org` in a browser

3. Rate Limiting:
   - TMDB has rate limits
   - Wait a few minutes and try again

Performance Issues
----------------

Slow Application
~~~~~~~~~~~~~~~

**Solutions**

1. Increase Database Cache:
   - Edit ``config.ini``:

     .. code-block:: ini

        [database]
        cache_size = 2000

2. Optimize Database:

   .. code-block:: sql

      OPTIMIZE TABLE movies;

3. Reduce Logging:
   - Set log level to WARNING or ERROR in ``logging.ini``

High Memory Usage
~~~~~~~~~~~~~~~

**Solutions**

1. Close unused tabs/windows
2. Reduce number of movies loaded at once
3. Restart the application

Common Error Messages
--------------------

"Database is locked"
~~~~~~~~~~~~~~~~~~~

**Cause**: Another instance of the application is using the database.

**Solution**:
1. Close all instances of Movie Catalog
2. Restart the application

"TMDB API Error"
~~~~~~~~~~~~~~~

**Solutions**:
1. Check your internet connection
2. Verify TMDB API key is valid
3. Check TMDB service status

Getting Help
-----------

If you're still experiencing issues:

1. Check the :doc:`FAQ <faq>`
2. Search the `GitHub Issues <https://github.com/Nsfr750/movie_catalog/issues>`_
3. Create a new issue with:
   - Steps to reproduce
   - Error messages
   - Log file content
   - Screenshots if applicable

.. note::
   Always include your Movie Catalog version and operating system when requesting help.

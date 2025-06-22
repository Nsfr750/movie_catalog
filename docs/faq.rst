.. _faq:

Frequently Asked Questions
========================

This section answers common questions about Movie Catalog.

.. contents::
   :depth: 2
   :local:

General Questions
----------------

What is Movie Catalog?
~~~~~~~~~~~~~~~~~~~~~

Movie Catalog is a Python application that helps you organize and manage your movie collection. It scans your movie files, categorizes them by genre, and provides tools to view and export your collection.

What platforms does it support?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Movie Catalog works on:

- Windows
- Linux
- Any platform that supports Python 3.8+

What video formats are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application supports the following video file formats:

- .mp4 (MPEG-4)
- .mkv (Matroska)
- .avi (Audio Video Interleave)
- .mov (QuickTime)
- .webm (WebM)
- .mpg (MPEG-1)
- .mpeg (MPEG)
- .wmv (Windows Media Video)
- .flv (Flash Video)
- .m4v (MPEG-4 Video)

Installation Questions
---------------------

How do I install Movie Catalog?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/Nsfr750/movie_catalog.git
      cd movie_catalog

2. Install dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

3. Run the application:

   .. code-block:: bash

      python main.py

What are the system requirements?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python 3.8 or higher
- MySQL 8.0+ or MariaDB 10.5+
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

Usage Questions
--------------

How do I add movies to the catalog?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Click the "Add Movie" button
2. Select the movie file or folder
3. The application will automatically fetch metadata

Can I edit movie information?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, you can edit movie information by:

1. Right-clicking on a movie
2. Selecting "Edit Details"
3. Making your changes
4. Clicking "Save"

Troubleshooting
--------------

Where can I find the log files?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Logs are stored in the ``logs`` directory:

.. code-block:: text

   movie_catalog/
   └── logs/
       └── movie_catalog.log

How do I reset the application?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Close the application
2. Delete the configuration file (location varies by OS)
3. Restart the application

.. note::
   This will reset all your settings to defaults.

Support
-------

Where can I get help?
~~~~~~~~~~~~~~~~~~~~

For additional help, please:

1. Check the :doc:`troubleshooting` guide
2. Open an issue on `GitHub <https://github.com/Nsfr750/movie_catalog/issues>`_
3. Contact support at nsfr750@yandex.com

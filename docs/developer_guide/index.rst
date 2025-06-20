.. _developer_guide:

Developer Guide
===============

This guide is intended for developers who want to contribute to Movie Catalog or extend its functionality.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   architecture
   database_schema
   api_reference
   testing
   contributing
   code_style
   deployment

Project Structure
----------------

.. code-block:: text

   movie_catalog/
   ├── docs/               # Documentation files
   ├── lang/               # Language files
   │   └── lang.py        # Language handling
   ├── logs/              # Application logs
   ├── struttura/         # Main package
   │   ├── __init__.py    # Package initialization
   │   ├── config.py      # Configuration management
   │   ├── db.py          # Database operations
   │   ├── movie_metadata.py  # TMDB integration
   │   └── ...            # Other modules
   ├── main.py            # Application entry point
   └── tests/             # Test files

Development Setup
----------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.8+
- MySQL Server
- Git
- Poetry (for dependency management)


Setting Up the Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Fork and clone the repository:
   .. code-block:: bash

      git clone https://github.com/Nsfr750/movie_catalog.git
      cd movie_catalog

2. Install dependencies:
   .. code-block:: bash

      pip install -r requirements-dev.txt
      pip install -e .


3. Set up pre-commit hooks:
   .. code-block:: bash

      pre-commit install

Coding Standards
----------------

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Write unit tests for new features

Testing
-------

Run the test suite:

.. code-block:: bash

   pytest tests/


Run with coverage:

.. code-block:: bash

   pytest --cov=src tests/

Documentation
------------

Building the Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install documentation dependencies:
   .. code-block:: bash

      pip install -r docs/requirements.txt

2. Build the documentation:
   .. code-block:: bash

      cd docs
      make html

3. Open `_build/html/index.html` in your browser

Documentation Guidelines
~~~~~~~~~~~~~~~~~~~~~~~
- Keep documentation up-to-date with code changes
- Use reStructuredText format for all documentation
- Include examples for complex functionality
- Document all public APIs

API Reference
------------

.. automodule:: struttura.movie_metadata
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: struttura.db
   :members:
   :undoc-members:
   :show-inheritance:


Deployment
---------

Building Distributions
~~~~~~~~~~~~~~~~~~~~~

Build a source distribution and wheel:

.. code-block:: bash

   python setup.py sdist bdist_wheel

Publishing to PyPI
~~~~~~~~~~~~~~~~~

1. Install Twine:
   .. code-block:: bash

      pip install twine

2. Upload to TestPyPI:
   .. code-block:: bash

      twine upload --repository testpypi dist/*

3. Upload to PyPI:
   .. code-block:: bash

      twine upload dist/*


Versioning
---------

Movie Catalog follows `Semantic Versioning <https://semver.org/>`_.

- **MAJOR** version for incompatible API changes
- **MINOR** version for added functionality in a backward-compatible manner
- **PATCH** version for backward-compatible bug fixes

Changelog
--------

See the :doc:`CHANGELOG <../changelog>` for a history of changes to the project.

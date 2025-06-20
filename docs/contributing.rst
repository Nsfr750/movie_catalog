.. _contributing:

Contributing to Movie Catalog
=============================

Thank you for your interest in contributing to Movie Catalog! We welcome all contributions, including bug reports, feature requests, documentation improvements, and code contributions.

Ways to Contribute
------------------

- **Report Bugs**: File an issue on our `issue tracker <https://github.com/Nsfr750/movie_catalog/issues>`_
- **Suggest Enhancements**: Open a new issue with the "enhancement" label
- **Write Documentation**: Improve the docs or add examples
- **Submit Fixes**: Submit a pull request for any open issues
- **Add Tests**: Help improve test coverage
- **Spread the Word**: Star the repository and tell others about the project

Getting Started
--------------

1. **Fork the Repository**
   - Click the "Fork" button on the `GitHub repository <https://github.com/Nsfr750/movie_catalog>`_
   - Clone your forked repository:
     .. code-block:: bash

        git clone https://github.com/Nsfr750/movie_catalog.git
        cd movie_catalog

2. **Set Up Development Environment**
   .. code-block:: bash

      # Create and activate a virtual environment
      python -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`

      # Install development dependencies
      pip install -r requirements-dev.txt
      pip install -e .
      # Install pre-commit hooks
      pre-commit install

3. **Create a Branch**
   .. code-block:: bash

      git checkout -b feature/your-feature-name

4. **Make Your Changes**
   - Follow the coding standards
   - Write tests for new features
   - Update documentation as needed

5. **Run Tests**
   .. code-block:: bash

      pytest tests/


6. **Commit Your Changes**
   .. code-block:: bash

      git add .
      git commit -m "Add your commit message here"
      git push origin feature/your-feature-name

7. **Open a Pull Request**
   - Go to the `GitHub repository <https://github.com/Nsfr750/movie_catalog/pulls>`_
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template
   - Submit the PR

Coding Standards
---------------

- Follow `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ style guide
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Write meaningful commit messages
- Update documentation when adding new features

Pull Request Guidelines
----------------------

- Keep PRs focused on a single feature or bug fix
- Update documentation and tests as needed
- Make sure all tests pass
- Reference relevant issues in your PR description
- Keep your branch up to date with the main branch

Development Workflow
-------------------

1. Create an issue describing the bug or feature
2. Fork the repository and create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Code Review Process
------------------

1. A maintainer will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

Reporting Bugs
-------------

When reporting bugs, please include:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected vs. actual behavior
4. Version information (Python, OS, etc.)
5. Any relevant error messages or logs

Feature Requests
---------------

For feature requests, please:

1. Check if a similar feature already exists
2. Explain why this feature would be useful
3. Describe how it should work
4. Include any relevant examples or mockups

License
-------
By contributing to Movie Catalog, you agree that your contributions will be licensed under the GPL-3.0 License.

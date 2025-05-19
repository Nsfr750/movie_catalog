# Contributing to Movie Catalog

We welcome contributions from the community! Whether you're fixing bugs, adding new features, or improving documentation, your help is greatly appreciated.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## How to Contribute

### Reporting Bugs

1. Check the [issue tracker](https://github.com/Nsfr750/movie_catalog/issues) to see if your issue has already been reported
2. If not, create a new issue with:
   - A clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, MySQL version)
   - Any error messages

### Suggesting Enhancements

1. Create an issue describing:
   - The enhancement you'd like to see
   - Why it would be beneficial
   - Any relevant examples or references

### Submitting Code Changes

1. Fork the repository
2. Create a new branch for your feature/bugfix
3. Make your changes
4. Add tests for your changes
5. Update documentation
6. Create a pull request

### Pull Request Guidelines

- Follow the code style guidelines
- Include tests for new features
- Update relevant documentation
- Reference the related issue in your PR description
- Keep PRs focused on a single change

## Development Setup

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Run the test suite:
   ```bash
   pytest tests/
   ```

3. Format your code:
   ```bash
   black src/
   isort src/
   ```

4. Check code style:
   ```bash
   flake8 src/
   pylint src/
   mypy src/
   ```

## Code Style

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all public methods
- Keep lines under 80 characters
- Use meaningful variable names
- Include error handling

## Testing

- Write unit tests for new features
- Include integration tests for database operations
- Test on multiple Python versions
- Test with different MySQL configurations

## Documentation

- Update API documentation for new features
- Add examples to the documentation
- Keep README.md up to date
- Document configuration options

## Versioning

We use Semantic Versioning (SemVer) for versioning. For the versions available, see the tags on this repository.

## License

By contributing to Movie Catalog, you agree that your contributions will be licensed under the MIT License.

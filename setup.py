from setuptools import setup, find_packages
import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="movie-catalog",
    version=version.get_version(),
    author="Nsfr750",
    author_email="nsfr750@yandex.com",
    description="A Python application for managing your movie collection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nsfr750/movie_catalog",
    project_urls={
        "Bug Tracker": "https://github.com/Nsfr750/movie_catalog/issues",
        "Documentation": "https://nsfr750.github.io/movie_catalog"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL3 License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "Topic :: Database",
        "Topic :: Utilities"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "mysql-connector-python>=8.2.0",
        "pillow>=10.2.0",
        "tkinter>=8.6"
    ],
    extras_require={
        "dev": [
            "black>=24.1.0",
            "isort>=5.13.0",
            "flake8>=7.0.0",
            "pytest>=7.4.3",
            "pylint>=3.0.2",
            "mypy>=1.8.0",
            "coverage>=7.3.2",
            "sphinx>=7.2.6",
            "twine>=4.1.2",
            "wheel>=0.42.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "movie-catalog=main:main"
        ]
    },
    package_data={
        "": ["*.json", "*.md", "*.txt"]
    },
    include_package_data=True,
    keywords=["movie", "catalog", "database", "MySQL", "media management"],
    license="GPL3"
)

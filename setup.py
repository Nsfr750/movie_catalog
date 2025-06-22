from setuptools import setup, find_packages
from pathlib import Path

# Read the README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Get version from struttura/version.py
version = {}
with open("struttura/version.py", "r", encoding="utf-8") as f:
    exec(f.read(), version)

setup(
    name="movie-catalog",
    version=version["__version__"],
    author="Nsfr750",
    author_email="nsfr750@yandex.com",
    description="A modern Python GUI application for managing and cataloging your movie collection with TMDB integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nsfr750/movie_catalog",
    project_urls={
        "Bug Tracker": "https://github.com/Nsfr750/movie_catalog/issues",
        "Documentation": "https://github.com/Nsfr750/movie_catalog/wiki",
        "Source Code": "https://github.com/Nsfr750/movie_catalog",
        "Changelog": "https://github.com/Nsfr750/movie_catalog/blob/main/CHANGELOG.md"
    },
    packages=find_packages(include=['struttura*']),
    package_dir={"": "."},
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "movie-catalog=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Natural Language :: Italian",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
)

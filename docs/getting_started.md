# Getting Started with Movie Catalog

## System Requirements

- Python 3.8 or higher
- MySQL 8.0 or higher
- Windows or Linux operating system

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/movie_catalog.git
   cd movie_catalog
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure MySQL:
   - Ensure MySQL is installed and running
   - Create a user with appropriate permissions
   - Note down the connection details (host, username, password)

4. Run the application:
   ```bash
   python main.py
   ```

## Initial Setup

1. Database Configuration:
   - Launch the application
   - Click "Database" in the menu
   - Configure your MySQL connection:
     - Host (default: localhost)
     - Username (default: root)
     - Password
     - Database name (default: movie_catalog)
   - Click "Save" to apply the configuration

2. Movie Directory Organization:
   The application expects movies to be organized in a folder structure like:
   ```
   movies/
   ├── Action/
   │   ├── ActionMovie1.mkv
   │   └── ActionMovie2.mp4
   ├── Comedy/
   │   ├── ComedyMovie1.mkv
   └── Drama/
       └── DramaMovie1.mp4
   ```

## Basic Usage

1. Create or Open Database:
   - Click "Database" in the menu
   - Choose "New Database" or "Open Database"
   - Follow the configuration wizard

2. Scan Movies:
   - Click "Browse" to select your movie directory
   - Click "Scan Movies" to start scanning
   - Progress will be shown in the progress bar
   - Status updates will appear in the status bar

## Supported Video Formats

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
- .vob (Video Object)
- .divx (DivX)

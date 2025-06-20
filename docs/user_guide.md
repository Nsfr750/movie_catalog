# User Guide

## Main Interface

### File Menu
- **New Database**: Create a new MySQL database
- **Open Database**: Connect to an existing database
- **Close Database**: Disconnect from the current database
- **Export to CSV**: Export movie list to CSV file
- **Exit**: Close the application

### Help Menu
- **Documentation**: Open online documentation
- **About**: Show application information
- **Sponsor**: Support the project

### Language Menu
- **Switch Language**: This menu allows you to change the application's display language at any time.
    - Click **Language** in the menu bar.
    - Select **English** or **Italiano**.
    - The entire user interface will instantly update to the selected language.

### Main Window Components

#### Directory Selection
- **Browse**: Select the root directory containing your movies
- **Current Directory**: Shows the currently selected directory

#### Action Buttons
- **Scan Movies**: Start scanning for movies
- **Load from Database**: Load movies from the database
- **Export to CSV**: Export current movie list to CSV

#### Progress Tracking
- **Progress Bar**: Shows scanning progress
- **Processed Files**: Number of files processed
- **Total Files**: Total number of files found

#### Movie Tree View
- Displays movies organized by genre
- Shows movie name and path
- Supports sorting and filtering

#### Status Bar
- Shows current application state
- Displays error messages
- Shows database connection status

## Database Management

### Creating a New Database
1. Click "Database" in the menu
2. Select "New Database"
3. Enter MySQL connection details:
   - Host: MySQL server address
   - Username: Database username
   - Password: Database password
   - Database: Name for new database
4. Click "Create" to create and connect to the database

### Opening an Existing Database
1. Click "Database" in the menu
2. Select "Open Database"
3. Enter existing MySQL connection details
4. Click "Connect" to connect to the database

## Movie Scanning

### Scanning Process
1. Select your movie directory using "Browse"
2. Click "Scan Movies" to start scanning
3. Progress will be shown in the progress bar
4. Movies will be automatically organized by genre
5. Results will be displayed in the tree view

### Supported File Formats
The application supports multiple video file formats:
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

## Exporting Movies

### Export to CSV
1. Click "Export to CSV" in the File menu
2. Choose a location to save the CSV file
3. The file will contain:
   - Genre
   - Movie Name
   - File Path
   - Last Scanned Date

## Troubleshooting

### Common Issues
- **Database Connection Failed**: Check MySQL connection details and server status
- **Files Not Found**: Ensure movies are organized in genre folders
- **Export Failed**: Check file permissions and available disk space
- **Scanning Stuck**: Check if MySQL server is responsive

### Error Messages
- **Database Error**: Check MySQL connection settings
- **File Error**: Verify file permissions and path
- **Configuration Error**: Review database configuration

## Tips and Best Practices

### Organizing Movies
- Keep movies organized in genre folders
- Use consistent naming conventions
- Maintain a backup of your movie collection
- Regularly update the database

### Performance Tips
- Close other applications during scanning
- Ensure MySQL server has enough resources
- Use proper indexing in the database
- Regularly maintain the database

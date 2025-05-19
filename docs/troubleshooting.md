# Troubleshooting Guide

## Common Issues and Solutions

### Application Won't Start

#### Symptoms
- Application crashes on launch
- Error messages in the status bar
- Blank window appears

#### Solutions
1. Check Python Installation
   - Verify Python 3.8+ is installed
   - Run `python --version` to check
   - Install Python from official website if needed

2. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Verify MySQL Connection
   - Ensure MySQL is running
   - Check MySQL service status
   - Verify MySQL user permissions

### Database Connection Issues

#### Symptoms
- "Database connection failed" error
- "Unable to connect to MySQL" message
- "Authentication failed" error

#### Solutions
1. Check MySQL Service
   - Ensure MySQL is running
   - Restart MySQL service if needed
   - Check MySQL logs for errors

2. Verify Connection Settings
   - Check host address
   - Verify username and password
   - Confirm database name
   - Test connection using MySQL client

3. User Permissions
   - Ensure user has proper permissions
   - Grant necessary privileges:
     ```sql
     GRANT ALL PRIVILEGES ON movie_catalog.* TO 'username'@'localhost';
     FLUSH PRIVILEGES;
     ```

### Movie Scanning Issues

#### Symptoms
- Movies not being found
- Slow scanning process
- Incomplete scan results

#### Solutions
1. Check File Permissions
   - Verify read permissions on movie files
   - Check directory access rights
   - Run as administrator if needed

2. Verify File Formats
   - Check supported formats:
     - .mp4, .mkv, .avi, .mov
     - .webm, .mpg, .mpeg
     - .wmv, .flv, .m4v
     - .vob, .divx
   - Convert unsupported formats

3. Folder Structure
   - Ensure movies are organized by genre
   - Check folder names match genre
   - Verify no hidden files

### Export Issues

#### Symptoms
- CSV export fails
- Empty CSV file
- Incorrect data format

#### Solutions
1. Check File Permissions
   - Verify write permissions
   - Check disk space
   - Run as administrator if needed

2. Verify Data
   - Check if movies are loaded
   - Verify database connection
   - Check for special characters

3. File Path
   - Use absolute paths
   - Avoid special characters
   - Check file name length

### GUI Issues

#### Symptoms
- Blank windows
- Missing menu items
- Unresponsive buttons

#### Solutions
1. Check Python Environment
   - Verify tkinter installation
   - Check Python version
   - Update tkinter if needed

2. Reinstall Dependencies
   ```bash
   pip uninstall movie-catalog
   pip install movie-catalog
   ```

3. Clear Cache
   - Delete __pycache__ folders
   - Remove compiled files
   - Restart application

## Error Messages and Solutions

### Database Errors

#### "Connection refused"
- MySQL service not running
- Incorrect host address
- Firewall blocking connection

#### "Access denied"
- Incorrect username/password
- User lacks permissions
- Host restrictions

### File Errors

#### "Permission denied"
- File locked by another process
- Insufficient permissions
- File in use

#### "File not found"
- Incorrect path
- File moved or deleted
- Symbolic link issues

### System Errors

#### "Out of memory"
- Insufficient RAM
- Large movie collection
- Too many open files

#### "Timeout"
- Slow network connection
- Large database
- Heavy system load

## Advanced Troubleshooting

### Debugging Steps

1. Enable Debug Mode
   - Add `-d` flag when running
   - Check debug output
   - Review error logs

2. Check System Resources
   - Monitor CPU usage
   - Check memory usage
   - Verify disk space

3. Review Logs
   - Check MySQL logs
   - Review application logs
   - Look for error patterns

### Performance Optimization

1. Optimize Database
   - Add proper indexes
   - Optimize queries
   - Regular maintenance

2. System Configuration
   - Increase file limits
   - Optimize MySQL settings
   - Use SSD storage

### Recovery Procedures

1. Database Recovery
   - Backup database
   - Restore from backup
   - Repair corrupted tables

2. File Recovery
   - Check backup copies
   - Use file recovery tools
   - Verify file integrity

## Support Resources

### Getting Help

1. GitHub Issues
   - Report bugs
   - Request features
   - Get support

2. Documentation
   - Check troubleshooting guide
   - Review installation guide
   - Read API documentation

3. Community
   - Join discussions
   - Share solutions
   - Get peer support

### Additional Resources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Python Documentation](https://docs.python.org/3/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Movie Catalog GitHub](https://github.com/Nsfr750/movie_catalog)

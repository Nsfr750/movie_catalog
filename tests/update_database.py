#!/usr/bin/env python3
"""
Database Migration Script for Movie Catalog

This script updates the database schema to support movie metadata.
It adds the following columns to the movies table:
- poster_url
- backdrop_url
- overview
- rating
- runtime
- director
- cast_json
- genres_json
- imdb_id
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from typing import Optional

# Add the project root to the path
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

# Import the database configuration
from struttura.db import MySQLDatabase, MySQLConfig

class DatabaseUpdater:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.is_mysql = False
        
    def connect(self):
        """Connect to the database."""
        try:
            if self.db_path:
                # SQLite connection
                self.conn = sqlite3.connect(self.db_path)
                self.cursor = self.conn.cursor()
                self.is_mysql = False
            else:
                # MySQL connection (using your existing MySQLDatabase class)
                self.conn = MySQLDatabase(None)  # Pass None for root as it's not needed
                # The MySQLDatabase class will show config form and create connection
                self.conn.create_connection()  # This sets up self.conn.connection
                if not hasattr(self.conn, 'connection') or not self.conn.connection:
                    print("Failed to connect to MySQL database")
                    return False
                self.cursor = self.conn.connection.cursor()  # Get cursor from the connection
                self.is_mysql = True
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            if hasattr(self.conn, 'close'):
                self.conn.close()
            elif hasattr(self.conn, 'connection') and self.conn.connection:
                self.conn.connection.close()
    
    def needs_update(self) -> bool:
        """Check if the database needs to be updated."""
        try:
            # Try to select from the new columns to see if they exist
            if self.is_mysql:
                self.cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'movies' 
                    AND COLUMN_NAME IN (
                        'poster_url', 'backdrop_url', 'overview',
                        'rating', 'runtime', 'director',
                        'cast_json', 'genres_json', 'imdb_id'
                    )
                """)
                # If any of the columns are missing, we need to update
                return self.cursor.fetchone()[0] < 9
            else:
                # SQLite version
                self.cursor.execute("PRAGMA table_info(movies)")
                columns = [col[1] for col in self.cursor.fetchall()]
                required_columns = {
                    'poster_url', 'backdrop_url', 'overview',
                    'rating', 'runtime', 'director',
                    'cast_json', 'genres_json', 'imdb_id'
                }
                return not required_columns.issubset(columns)
                
        except Exception as e:
            print(f"Error checking if update is needed: {e}")
            # If there's an error, assume we need to update
            return True
    
    def backup_database(self, backup_path: str) -> bool:
        """Create a backup of the database."""
        try:
            if self.db_path:  # SQLite
                import shutil
                shutil.copy2(self.db_path, backup_path)
                print(f"Database backed up to {backup_path}")
                return True
            else:  # MySQL
                print("For MySQL, please create a backup manually before proceeding.")
                print("You can use the following command:")
                print(f"mysqldump -h {self.conn.host} -u {self.conn.user} -p {self.conn.database} > {backup_path}")
                return False
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def update_schema(self) -> bool:
        """Update the database schema to support movie metadata."""
        try:
            columns = [
                ("poster_url", "TEXT"),
                ("backdrop_url", "TEXT"),
                ("overview", "TEXT"),
                ("rating", "REAL"),
                ("runtime", "INTEGER"),
                ("director", "TEXT"),
                ("cast_json", "TEXT"),
                ("genres_json", "TEXT"),
                ("imdb_id", "VARCHAR(20)")
            ]
            
            for column, data_type in columns:
                if self.is_mysql:
                    self.cursor.execute(f"""
                        SELECT COUNT(*)
                        FROM information_schema.COLUMNS 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'movies' 
                        AND COLUMN_NAME = %s
                    """, (column,))
                    if not self.cursor.fetchone()[0]:
                        self.cursor.execute(f"""
                            ALTER TABLE movies 
                            ADD COLUMN {column} {data_type}
                        """)
                else:
                    # SQLite doesn't support IF NOT EXISTS in ALTER TABLE
                    try:
                        self.cursor.execute(f"""
                            ALTER TABLE movies 
                            ADD COLUMN {column} {data_type}
                        """)
                    except sqlite3.OperationalError as e:
                        if "duplicate column" not in str(e):
                            raise
            
            # Commit changes
            if self.is_mysql:
                if hasattr(self.conn, 'connection') and self.conn.connection:
                    self.conn.connection.commit()
                else:
                    self.conn.commit()
            else:
                self.conn.commit()
                
            print("Database schema updated successfully!")
            return True
            
        except Exception as e:
            print(f"Error updating database schema: {e}")
            if self.is_mysql:
                if hasattr(self.conn, 'connection') and self.conn.connection:
                    self.conn.connection.rollback()
                elif hasattr(self.conn, 'rollback'):
                    self.conn.rollback()
            elif hasattr(self.conn, 'rollback'):
                self.conn.rollback()
            return False
    
    def migrate_existing_data(self) -> bool:
        """Migrate existing data to match the new schema."""
        try:
            # Set default values for existing records
            if self.is_mysql:
                self.cursor.execute("""
                    UPDATE movies 
                    SET 
                        poster_url = IFNULL(poster_url, ''),
                        backdrop_url = IFNULL(backdrop_url, ''),
                        overview = IFNULL(overview, ''),
                        rating = IFNULL(rating, 0),
                        runtime = IFNULL(runtime, 0),
                        director = IFNULL(director, ''),
                        cast_json = IFNULL(cast_json, '[]'),
                        genres_json = IFNULL(genres_json, '[]'),
                        imdb_id = IFNULL(imdb_id, '')
                """)
            else:
                # SQLite uses COALESCE instead of IFNULL
                self.cursor.execute("""
                    UPDATE movies 
                    SET 
                        poster_url = COALESCE(poster_url, ''),
                        backdrop_url = COALESCE(backdrop_url, ''),
                        overview = COALESCE(overview, ''),
                        rating = COALESCE(rating, 0),
                        runtime = COALESCE(runtime, 0),
                        director = COALESCE(director, ''),
                        cast_json = COALESCE(cast_json, '[]'),
                        genres_json = COALESCE(genres_json, '[]'),
                        imdb_id = COALESCE(imdb_id, '')
                """)
            
            if hasattr(self.conn, 'connection') and self.conn.connection:
                self.conn.connection.commit()
            else:
                self.conn.commit()
                
            print("Existing data migrated successfully!")
            return True
            
        except Exception as e:
            print(f"Error migrating existing data: {e}")
            if hasattr(self.conn, 'connection') and self.conn.connection:
                self.conn.connection.rollback()
            elif hasattr(self.conn, 'rollback'):
                self.conn.rollback()
            return False

def main():
    print("=" * 50)
    print("Movie Catalog Database Update Tool")
    print("=" * 50)
    print()
    
    # Determine database type and path
    use_mysql = input("Are you using MySQL? (y/n): ").lower().strip() == 'y'
    
    updater = DatabaseUpdater()
    
    if not use_mysql:
        db_path = input("Enter the path to your SQLite database file: ").strip('\\')
        if not os.path.exists(db_path):
            print(f"Error: Database file not found: {db_path}")
            return 1
            
        updater.db_path = db_path
    
    # Connect to the database
    print("\nConnecting to database...")
    if not updater.connect():
        return 1
    
    try:
        # Check if update is needed
        if not updater.needs_update():
            print("\nYour database is already up to date!")
            return 0
        
        print("\nDatabase update is required.")
        print("The following changes will be made:")
        print("  - Add poster_url (TEXT)")
        print("  - Add backdrop_url (TEXT)")
        print("  - Add overview (TEXT)")
        print("  - Add rating (REAL)")
        print("  - Add runtime (INTEGER)")
        print("  - Add director (TEXT)")
        print("  - Add cast_json (TEXT)")
        print("  - Add genres_json (TEXT)")
        print("  - Add imdb_id (TEXT)")
        
        # Ask for confirmation
        confirm = input("\nDo you want to proceed with the update? (y/n): ").lower().strip()
        if confirm != 'y':
            print("Update cancelled.")
            return 0
        
        # Create backup
        if use_mysql:
            print("\nPlease ensure you have a backup of your MySQL database.")
            backup_confirm = input("Have you created a backup? (y/n): ").lower().strip()
            if backup_confirm != 'y':
                print("Please create a backup before proceeding.")
                return 1
        else:
            backup_path = f"{updater.db_path}.backup"
            if not updater.backup_database(backup_path):
                confirm = input("Failed to create backup. Continue anyway? (y/n): ").lower().strip()
                if confirm != 'y':
                    print("Update cancelled.")
                    return 0
        
        # Perform the update
        print("\nUpdating database schema...")
        if not updater.update_schema():
            print("Failed to update database schema.")
            return 1
        
        print("\nMigrating existing data...")
        if not updater.migrate_existing_data():
            print("Warning: Some data migration steps failed.")
        
        print("\nDatabase update completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        print("\nUpdate cancelled by user.")
        return 1
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return 1
    finally:
        updater.close()

if __name__ == "__main__":
    sys.exit(main())
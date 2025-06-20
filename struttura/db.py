import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import csv

class MySQLConfig:
    def __init__(self, root=None):
        self.root = root
        self.config_file = 'mysql_config.json'
        self.default_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '22243',
            'database': 'movie_catalog'
        }
        self.config = self.load_config()
        
    def show_config_form(self):
        if not self.root:
            return self.config
            
        def save_and_close():
            config = {
                'host': host_entry.get(),
                'user': user_entry.get(),
                'password': password_entry.get(),
                'database': database_entry.get()
            }
            if self.save_config(config):
                messagebox.showinfo("Success", "Configuration saved successfully!")
                config_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save configuration")
                
        config_window = tk.Toplevel(self.root)
        
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.default_config
        return self.default_config
        
    def save_config(self, config):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
            
    def show_config_form(self):
        def save_and_close():
            config = {
                'host': host_entry.get(),
                'user': user_entry.get(),
                'password': password_entry.get(),
                'database': database_entry.get()
            }
            if self.save_config(config):
                messagebox.showinfo("Success", "Configuration saved successfully!")
                config_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save configuration")
                
        config_window = tk.Toplevel()
        config_window.title("MySQL Configuration")
        config_window.geometry("400x400")
        
        # Create form elements
        ttk.Label(config_window, text="Host:").pack(pady=5)
        host_entry = ttk.Entry(config_window)
        host_entry.pack(pady=5)
        host_entry.insert(0, self.config['host'])
        
        ttk.Label(config_window, text="Username:").pack(pady=5)
        user_entry = ttk.Entry(config_window)
        user_entry.pack(pady=5)
        user_entry.insert(0, self.config['user'])
        
        ttk.Label(config_window, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(config_window, show="*")
        password_entry.pack(pady=5)
        password_entry.insert(0, self.config['password'])
        
        ttk.Label(config_window, text="Database Name:").pack(pady=5)
        database_entry = ttk.Entry(config_window)
        database_entry.pack(pady=5)
        database_entry.insert(0, self.config['database'])
        
        # Save button
        save_button = ttk.Button(config_window, text="Save Configuration", command=save_and_close)
        save_button.pack(pady=20)

class MySQLDatabase:
    def __init__(self, root):
        self.config = MySQLConfig(root)
        self.config.show_config_form()
        self.host = self.config.config['host']
        self.user = self.config.config['user']
        self.password = self.config.config['password']
        self.database = self.config.config['database']
        self.connection = None
        self.cursor = None
        self.is_mysql = True  # Add this line to indicate we're using MySQL
        
    def create_connection(self):
        """Create and return a new database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin='mysql_native_password'
            )
            return self.connection
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error connecting to MySQL: {err}")
            return None
            
    def create_database(self):
        """Create the database if it doesn't exist"""
        try:
            # First connect without database parameter
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                auth_plugin='mysql_native_password'
            )
            cursor = conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # Store the connection
            self.connection = conn
            self.cursor = cursor
            
            return conn
            
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error creating database: {err}")
            if conn and conn.is_connected():
                conn.close()
            return None
            
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        if not self.connection or not self.connection.is_connected():
            if not self.create_connection():
                return False
                
        cursor = self.connection.cursor(dictionary=True)
        try:
            # Create movies table with all necessary columns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movies (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    genre VARCHAR(255),
                    movie_name VARCHAR(255),
                    title VARCHAR(255),
                    year INT,
                    path VARCHAR(512) UNIQUE,
                    poster_url TEXT,
                    backdrop_url TEXT,
                    overview TEXT,
                    rating FLOAT,
                    runtime INT,
                    director VARCHAR(255),
                    cast_json TEXT,
                    genres_json TEXT,
                    imdb_id VARCHAR(50),
                    last_scanned DATETIME,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            
            # Add any missing columns
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'movies'
            """, (self.database,))
            
            existing_columns = [col['COLUMN_NAME'] for col in cursor.fetchall()]
            
            # Add missing columns if they don't exist
            columns_to_add = [
                ("genre", "ALTER TABLE movies ADD COLUMN genre VARCHAR(255) AFTER id"),
                ("movie_name", "ALTER TABLE movies ADD COLUMN movie_name VARCHAR(255) AFTER genre"),
                ("title", "ALTER TABLE movies ADD COLUMN title VARCHAR(255) AFTER movie_name"),
                ("year", "ALTER TABLE movies ADD COLUMN year INT AFTER title"),
                ("poster_url", "ALTER TABLE movies ADD COLUMN poster_url TEXT AFTER path"),
                ("backdrop_url", "ALTER TABLE movies ADD COLUMN backdrop_url TEXT AFTER poster_url"),
                ("overview", "ALTER TABLE movies ADD COLUMN overview TEXT AFTER backdrop_url"),
                ("rating", "ALTER TABLE movies ADD COLUMN rating FLOAT AFTER overview"),
                ("runtime", "ALTER TABLE movies ADD COLUMN runtime INT AFTER rating"),
                ("director", "ALTER TABLE movies ADD COLUMN director VARCHAR(255) AFTER runtime"),
                ("cast_json", "ALTER TABLE movies ADD COLUMN cast_json TEXT AFTER director"),
                ("genres_json", "ALTER TABLE movies ADD COLUMN genres_json TEXT AFTER cast_json"),
                ("imdb_id", "ALTER TABLE movies ADD COLUMN imdb_id VARCHAR(50) AFTER genres_json"),
                ("last_scanned", "ALTER TABLE movies ADD COLUMN last_scanned DATETIME AFTER imdb_id"),
                ("created_at", "ALTER TABLE movies ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER last_scanned"),
                ("updated_at", "ALTER TABLE movies ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at")
            ]
            
            for column_name, alter_query in columns_to_add:
                if column_name not in existing_columns:
                    try:
                        cursor.execute(alter_query)
                        print(f"Added column: {column_name}")
                    except mysql.connector.Error as err:
                        print(f"Error adding column {column_name}: {err}")
            
            self.connection.commit()
            return True
            
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error creating/updating tables: {err}")
            return False
            
    def close(self):
        """Close the database connection"""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def add_movie(self, genre, movie_name, path):
        conn = self.create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO movies (genre, movie_name, path, last_scanned)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                genre = VALUES(genre),
                movie_name = VALUES(movie_name),
                last_scanned = VALUES(last_scanned)
            ''', (genre, movie_name, path, datetime.now()))
            conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error adding movie: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
            
    def get_all_movies(self):
        conn = self.create_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT genre, movie_name, path 
                FROM movies 
                ORDER BY genre, movie_name
            ''')
            movies = cursor.fetchall()
            return movies
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error fetching movies: {err}")
            return []
        finally:
            cursor.close()
            conn.close()
            
    def store_scanned_files(self, files):
        """
        Store a list of scanned files in the database.
        
        Args:
            files: List of tuples containing (genre, movie_name, path)
        
        Returns:
            bool: True if all files were stored successfully, False otherwise
        """
        conn = self.create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        try:
            # Prepare the SQL statement
            sql = '''
                INSERT INTO movies (genre, movie_name, path, last_scanned)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                genre = VALUES(genre),
                movie_name = VALUES(movie_name),
                last_scanned = VALUES(last_scanned)
            '''
            
            # Add timestamp to each file tuple
            files_with_timestamp = [(genre, movie_name, path, datetime.now()) 
                                  for genre, movie_name, path in files]
            
            # Execute the query with multiple rows
            cursor.executemany(sql, files_with_timestamp)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error storing files: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
            
    def export_to_csv(self, filename):
        """
        Export movies to CSV file
        
        Args:
            filename: Path to the CSV file
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        try:
            # Get movies from database
            movies = self.get_all_movies()
            if not movies:
                messagebox.showwarning("Warning", "No movies found to export")
                return False
                
            # Ensure directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Write to CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Genre', 'Movie Name', 'Path', 'Last Scanned'])
                for genre, movie_name, path in movies:
                    writer.writerow([genre, movie_name, path, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            
            messagebox.showinfo("Success", f"Successfully exported {len(movies)} movies to {filename}")
            return True
            
        except PermissionError:
            messagebox.showerror("Error", "Permission denied. Please check file permissions.")
            return False
            
        except OSError as e:
            messagebox.showerror("Error", f"File error: {str(e)}")
            return False
            
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error exporting to CSV: {str(e)}")
            return False

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Movie Catalog Application
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import platform
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import mysql.connector
from mysql.connector import Error
import threading
import time
import json
from datetime import datetime
import csv
import lang.lang as lang
from pathlib import Path
import queue
from lang import lang
from struttura.version import __version__
from struttura.menu import AppMenu
from struttura import db
from lang.lang import get_string as tr
from struttura import logger
from struttura.traceback import setup_exception_handling
from struttura.movie_details_dialog import MovieDetailsDialog
from struttura.movie_metadata import MovieMetadata

# Configura il logger principale
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler('movie_catalog.log', maxBytes=5*1024*1024, backupCount=5)
    ]
)

# Crea un logger specifico per il modulo
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, root):
        """
        Inizializza la connessione al database.
        
        Args:
            root: Radice dell'applicazione
        """
        self.db = None
        self.root = root
        self.connection = None
        self.cursor = None
        self.is_mysql = True  # We're using MySQL
        self.logger = logger.logger.getChild('Database')
        self.logger.info("Database handler inizializzato")
        
    def initialize(self):
        """Initialize the database connection"""
        try:
            self.db = db.MySQLDatabase(self.root)
            
            # Create database and get connection
            self.connection = self.db.create_database()
            if not self.connection:
                return False
                
            # Create tables if they don't exist
            if not self.db.create_tables():
                return False
                
            # Get a cursor for executing queries
            self.cursor = self.connection.cursor(dictionary=True)
            return True
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
        
    def close(self):
        """Close the database connection"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
                self.connection.close()
            if hasattr(self, 'db') and self.db:
                self.db.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")
            
    def store_scanned_files(self, files):
        """
        Store a list of scanned files in the database.
        
        Args:
            files: List of tuples containing (genre, movie_name, path)
        
        Returns:
            bool: True if all files were stored successfully, False otherwise
        """
        if not hasattr(self, 'db') or not self.db:
            print("Error: Database not initialized")
            return False
        
        try:
            # Forward the call to the MySQLDatabase instance
            return self.db.store_scanned_files(files)
        except Exception as e:
            print(f"Error storing scanned files: {e}")
            return False
            
    def add_movie_with_metadata(self, title, year, path, poster_url, backdrop_url, overview,
                            rating, runtime, director, cast, genres, imdb_id):
        """
        Add a movie with full metadata to the database.
        
        Args:
            title (str): Movie title
            year (int): Release year
            path (str): Path to the movie file
            poster_url (str): URL to the movie poster
            backdrop_url (str): URL to the movie backdrop
            overview (str): Movie plot summary
            rating (float): Movie rating (0-10)
            runtime (int): Movie duration in minutes
            director (str): Movie director
            cast (list): List of cast members
            genres (list): List of genres
            imdb_id (str): IMDB ID (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure we have a valid connection
            if not self.connection or not self.connection.is_connected():
                if not self.initialize():
                    return False
            
            # Convert lists to JSON strings
            cast_json = json.dumps(cast) if cast else '[]'
            genres_json = json.dumps(genres) if genres else '[]'
            
            # Extract genre from path if not provided
            genre = ''
            if path:
                path_parts = path.replace('\\', '/').split('/')
                if len(path_parts) > 1:
                    genre = path_parts[-2]  # Assuming genre is the parent directory
            
            # Check if the table has the new schema
            self.cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'movies' 
                AND COLUMN_NAME = 'title'
            """)
            has_new_schema = bool(self.cursor.fetchone())
            
            # Check if updated_at column exists
            self.cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'movies' 
                AND COLUMN_NAME = 'updated_at'
            """)
            has_updated_at = bool(self.cursor.fetchone())
            
            if has_new_schema:
                # Build the base query
                columns = [
                    'title', 'year', 'path', 'poster_url', 'backdrop_url', 'overview',
                    'rating', 'runtime', 'director', 'cast_json', 'genres_json', 'imdb_id',
                    'genre', 'movie_name'
                ]
                placeholders = ', '.join(['%s'] * len(columns))
                
                # Build the ON DUPLICATE KEY UPDATE part
                update_columns = [
                    'title = VALUES(title)',
                    'year = VALUES(year)',
                    'poster_url = VALUES(poster_url)',
                    'backdrop_url = VALUES(backdrop_url)',
                    'overview = VALUES(overview)',
                    'rating = VALUES(rating)',
                    'runtime = VALUES(runtime)',
                    'director = VALUES(director)',
                    'cast_json = VALUES(cast_json)',
                    'genres_json = VALUES(genres_json)',
                    'imdb_id = VALUES(imdb_id)',
                    'genre = VALUES(genre)',
                    'movie_name = VALUES(movie_name)'
                ]
                
                # Add updated_at if the column exists
                if has_updated_at:
                    update_columns.append('updated_at = CURRENT_TIMESTAMP')
                
                query = f"""
                    INSERT INTO movies 
                    ({', '.join(columns)})
                    VALUES ({placeholders})
                    ON DUPLICATE KEY UPDATE
                    {', '.join(update_columns)}
                """
                
                params = (
                    title, year, path, poster_url, backdrop_url, overview,
                    rating, runtime, director, cast_json, genres_json, imdb_id,
                    genre, title  # Using title as movie_name for backward compatibility
                )
            else:
                # Fallback to old schema
                query = """
                    INSERT INTO movies 
                    (genre, movie_name, path)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    genre = VALUES(genre),
                    movie_name = VALUES(movie_name),
                    last_scanned = CURRENT_TIMESTAMP
                """
                params = (genre, title, path)
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"Error adding movie with metadata: {e}")
            if self.connection and self.connection.is_connected():
                self.connection.rollback()
            return False

    def add_movie_with_metadata_dialog(self):
        """Open dialog to add a movie with metadata."""
        def save_metadata(metadata):
            # Save to database
            movie_id = self.add_movie_with_metadata(
                title=metadata['title'],
                year=metadata['year'],
                path="",  # You'll need to set this
                poster_url=metadata['poster_url'],
                backdrop_url=metadata['backdrop_url'],
                overview=metadata['overview'],
                rating=metadata['rating'],
                runtime=metadata['runtime'],
                director=metadata['director'],
                cast=json.dumps(metadata['cast']),
                genres=json.dumps(metadata['genres']),
                imdb_id=metadata['imdb_id']
            )
            if movie_id:
                self.refresh_movie_list()
        
        dialog = MovieDetailsDialog(
            self.root,
            title="New Movie",
            on_save=save_metadata
        )
        dialog.transient(self.root)
        dialog.grab_set()

    def add_movie(self, genre, movie_name, path):
        if self.db:
            return self.db.add_movie(genre, movie_name, path)
        return False
        
    def get_all_movies(self, sort_by='title', sort_order='ASC'):
        if self.db:
            return self.db.get_all_movies(sort_by, sort_order)
        return []
        
    def export_to_csv(self, filename):
        if self.db:
            return self.db.export_to_csv(filename)
        return False
        
    def import_from_csv(self, filename):
        """
        Import movies from a CSV file into the database
        
        Args:
            filename: Path to the CSV file to import
            
        Returns:
            tuple: (success: bool, imported_count: int, error_message: str)
        """
        if not self.db:
            return False, 0, "Database not initialized"
        return self.db.import_from_csv(filename)

    def check_database_contents(self):
        """Check database connection and list tables/contents"""
        try:
            if not self.database or not self.database.connection or not self.database.connection.is_connected():
                print("No active database connection")
                return False
                
            cursor = self.database.connection.cursor(dictionary=True)
            
            # List all tables in the database
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\n=== Database Tables ===")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"\nTable: {table_name}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
                count = cursor.fetchone()['count']
                print(f"  Rows: {count}")
                
                # Show first few rows if table is not empty
                if count > 0:
                    cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 5")
                    rows = cursor.fetchall()
                    print("  First few rows:")
                    for row in rows:
                        print(f"  - {row}")
            
            cursor.close()
            return True
            
        except Exception as e:
            print(f"Error checking database: {str(e)}")
            return False

    def empty_database(self):
        """Svuota il database dei film"""
        if not hasattr(self, 'db') or self.db is None:
            messagebox.showerror(
                lang.get_string('error'),
                lang.get_string('db_not_initialized')
            )
            self.logger.error("Tentativo di svuotare il database non inizializzato")
            return False
                
        # Chiedi conferma all'utente
        confirm = messagebox.askyesno(
            lang.get_string('warning'),
            lang.get_string('confirm_empty_database')
        )
        
        if not confirm:
            return False

        try:
            # Mostra un messaggio di attesa
            if hasattr(self, 'status_frame'):
                self.status_frame.config(text=lang.get_string('emptying_database') + '...')
            self.root.update_idletasks()
            
            # Imposta un timeout più lungo per l'operazione
            success = False
            max_retries = 3
            retry_delay = 5  # secondi
            
            for attempt in range(max_retries):
                try:
                    # Prova a svuotare il database
                    success = self.db.empty_database()
                    if success:
                        break
                        
                except Exception as e:
                    error_msg = f"Errore durante lo svuotamento (tentativo {attempt + 1}/{max_retries}): {str(e)}"
                    self.logger.error(error_msg)
                    
                    if attempt < max_retries - 1:
                        self.logger.info(f"Riprovo tra {retry_delay} secondi...")
                        time.sleep(retry_delay)
                    else:
                        raise  # Rilancia l'eccezione dopo l'ultimo tentativo
            
            if success:
                # Aggiorna l'interfaccia utente
                if hasattr(self, 'tree'):
                    for item in self.tree.get_children():
                        self.tree.delete(item)
                
                messagebox.showinfo(
                    lang.get_string('success'),
                    lang.get_string('database_emptied_successfully')
                )
                self.logger.info("Database svuotato con successo")
                if hasattr(self, 'status_frame'):
                    self.status_frame.config(text=lang.get_string('database_emptied_successfully'))
            else:
                raise Exception("Operazione fallita senza errori specifici")
                
            return success
            
        except Exception as e:
            error_msg = f"{lang.get_string('error_emptying_database')}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            messagebox.showerror(
                lang.get_string('error'),
                error_msg
            )
            if hasattr(self, 'status_frame'):
                self.status_frame.config(text=lang.get_string('error_emptying_database'))
            return False

class MovieScanner:
    def __init__(self, root_path, queue):
        self.root_path = root_path
        self.queue = queue
        self.total_files = 0
        self.processed = 0
        
    def scan(self):
        print(f"Scanning directory: {self.root_path}")
        
        # First get all files and count them
        all_files = []
        for root, dirs, files in os.walk(self.root_path):
            print(f"Processing directory: {root}")
            all_files.extend([(root, file) for file in files])
            
        self.total_files = len(all_files)
        print(f"Total files found: {self.total_files}")
        
        self.processed = 0
        
        # Now process each file
        for root, file in all_files:
            print(f"Found file: {file}")
            if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm', '.mpg', '.mpeg', '.wmv', '.flv', '.m4v', '.vob', '.divx')):
                self.processed += 1
                full_path = os.path.join(root, file)
                print(f"Found movie file: {full_path}")
                
                # Extract genre from directory name
                # If in root directory, use 'Unknown' genre
                if root == self.root_path:
                    genre = 'Unknown'
                else:
                    genre = os.path.basename(os.path.dirname(full_path))
                    # If genre directory contains spaces, replace with underscores
                    genre = genre.replace(' ', '_')
                
                # Extract movie name from filename (remove extensions)
                movie_name = os.path.splitext(file)[0]
                
                # Send movie result to queue with 'movie' type
                movie_data = (genre, movie_name, full_path)
                self.queue.put(('movie', movie_data))
                print(f"Added movie to queue: {genre}, {movie_name}, {full_path}")
                
                # Send progress update with 'progress' type
                if self.total_files > 0:  # Prevent division by zero
                    progress = int((self.processed / self.total_files) * 100)
                    self.queue.put(('progress', progress))
                    print(f"Progress: {progress}%")
        
        # Send completion signal
        print("Sending 'finished' signal to queue")
        self.queue.put(('finished', None))
        print("Scan completed")

class MovieCatalogApp:
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title(f"Movie Catalog v{__version__}")
        self.root.geometry("1000x600")
        
        # Make sure the window is visible
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
        # Set up logging and exception handling
        self._setup_logging()
        print("Logging setup complete")
        
        # Configure styles
        self._configure_styles()
        print("Styles configured")
        
        # Initialize components
        self.result_queue = queue.Queue()
        self.movies_to_save = []
        self.scanning = False
        
        # Inizializza le variabili di ordinamento
        self.sort_by = tk.StringVar(value='title')
        self.sort_order = tk.StringVar(value='ASC')
        
        # Show loading message
        loading_label = ttk.Label(
            self.root, 
            text="Initializing database...", 
            font=('Helvetica', 12)
        )
        loading_label.pack(expand=True)
        self.root.update()  # Force UI update
        
        try:
            # Initialize database
            print("Initializing database...")
            self.database = Database(root)
            if not self.database.initialize():
                print("Database initialization failed")
                if messagebox.askretrycancel("Error", "Failed to initialize database. Retry?"):
                    self.root.after(100, self.retry_database_init)
                    return
                else:
                    self.root.quit()
                    return
                    
            # Remove loading message and create main UI
            loading_label.destroy()
            
            # Create main frame and UI components
            print("Creating main UI components...")
            self.main_frame = ttk.Frame(self.root)
            self.main_frame.pack(fill='both', expand=True)
            
            self._create_gui_components()
            self.menu = AppMenu(self)
            self.update_status('Ready')
            self.set_language('en')
            
            print("Application initialization complete")
            
        except Exception as e:
            import traceback
            error_msg = f"Failed to initialize application: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("Fatal Error", f"Failed to start application:\n{str(e)}")
            self.root.quit()
    
    def retry_database_init(self):
        """Retry database initialization"""
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
        self.__init__(self.root)
    
    def _setup_logging(self):
        """Set up logging and exception handling."""
        # Configure the root logger
        logger.logger.info("Starting Movie Catalog")
        
        # Set up global exception handling
        setup_exception_handling()
        
        # Log system information
        import platform
        logger.logger.info(f"Python version: {platform.python_version()}")
        logger.logger.info(f"System: {platform.system()} {platform.release()}")
        logger.logger.info(f"Working directory: {os.getcwd()}")
        
        # Initialize logger for this class
        self.logger = logging.getLogger('MovieCatalog.App')
        self.logger.info("Inizializzazione dell'applicazione")
    
    def set_language(self, lang_code):
        """Set the application language and update all UI texts."""
        lang.set_language(lang_code)
        self.update_ui_texts()
        # Update menu texts if menu exists
        if hasattr(self, 'menu') and hasattr(self.menu, 'update_menu_texts'):
            self.menu.update_menu_texts()

    def update_ui_texts(self):
        """Update all UI texts to the current language."""
        self.root.title(f"{lang.get_string('app_title')} v{__version__}")
        
        # Update directory frame
        if hasattr(self, 'dir_frame'):
            self.dir_frame.config(text=lang.get_string('select_directory'))
        
        # Update browse button
        if hasattr(self, 'browse_btn'):
            self.browse_btn.config(text=lang.get_string('browse'))
        
        # Update actions frame
        if hasattr(self, 'actions_frame'):
            self.actions_frame.config(text=lang.get_string('actions'))
        
        # Update action buttons
        if hasattr(self, 'scan_btn'):
            self.scan_btn.config(text=lang.get_string('scan_the_movies'))
        if hasattr(self, 'export_btn'):
            self.export_btn.config(text=lang.get_string('export_to_csv'))
        if hasattr(self, 'load_btn'):
            self.load_btn.config(text=lang.get_string('load_db'))
        
        # Update tree view headers
        if hasattr(self, 'tree'):
            self.tree.heading("id", text=lang.get_string('id'))
            self.tree.heading("genres", text=lang.get_string('genres'))
            self.tree.heading("movie_name", text=lang.get_string('movie_name'))
            self.tree.heading("title", text=lang.get_string('title'))
            self.tree.heading("year", text=lang.get_string('year'))
            self.tree.heading("path", text=lang.get_string('path'))
        
        # Update status
        if hasattr(self, 'status_frame'):
            self.status_frame.config(text=lang.get_string('ready'))

    def load_movies_from_database(self, search_term=None):
        """Carica i film dal database nell'albero con supporto per ricerca e ordinamento"""
        if not self.database:
            messagebox.showwarning(lang.get_string('error'), lang.get_string('db_not_initialized'))
            return
            
        try:
            # Ottieni i parametri di ordinamento
            sort_by = getattr(self, 'sort_by', tk.StringVar(value='title')).get()
            sort_order = getattr(self, 'sort_order', tk.StringVar(value='ASC')).get()
            
            # Stampa di debug per verificare i parametri
            print(f"Ordinamento richiesto: campo={sort_by}, ordine={sort_order}")
            
            # Recupera i film con l'ordinamento specificato
            movies = self.database.get_all_movies(sort_by=sort_by, sort_order=sort_order)
            
            # Filtra i risultati se è specificato un termine di ricerca
            if search_term:
                search_term = search_term.lower()
                movies = [m for m in movies if any(
                    search_term in str(field).lower() 
                    for field in m 
                    if field is not None
                )]
            
            # Pulisci la vista attuale
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Se non ci sono film, mostra un messaggio
            if not movies:
                self.tree.insert('', 'end', values=[lang.get_string('no_movies_found')])
                return
            
            # Popola la treeview con i film
            for movie in movies:
                # Converti i valori None in stringhe vuote per la visualizzazione
                movie_display = [str(field) if field is not None else '' for field in movie]
                self.tree.insert('', 'end', values=movie_display)
            
            # Aggiorna il contatore
            self.update_movie_count(len(movies))
            
        except Exception as e:
            messagebox.showerror(
                lang.get_string('error'), 
                f"Errore durante il caricamento dei film: {str(e)}"
            )
            self.logger.error(f"Errore nel caricamento dei film: {str(e)}")
    
    def on_search(self, event=None):
        """Gestisce l'evento di ricerca"""
        search_term = self.search_var.get()
        self.load_movies_from_database(search_term=search_term if search_term else None)
    
    def _new_database(self):
        """Create a new database"""
        if self.database.initialize():
            messagebox.showinfo(lang.get_string('success'), lang.get_string('db_created'))
        else:
            messagebox.showerror(lang.get_string('error'), lang.get_string('db_create_failed'))
    
    def _open_database(self):
        """Open database configuration form"""
        if self.database.db:
            self.database.db.config.show_config_form()
        else:
            messagebox.showerror(lang.get_string('error'), lang.get_string('db_not_initialized'))
    
    def _close_database(self):
        """Close database connection"""
        if self.database.db:
            self.database.db.close_connection()
            messagebox.showinfo(lang.get_string('success'), lang.get_string('db_closed'))
        else:
            messagebox.showerror(lang.get_string('error'), lang.get_string('db_not_initialized'))
    
    def _create_gui_components(self):
        """Create all GUI components"""
        # Directory selection frame
        self._create_directory_frame()
        
        # Actions frame
        self._create_actions_frame()
        
        # Search frame
        self._create_search_frame()
        
        # Progress bar
        self._create_progress_bar()
        
        # Tree view
        self._create_tree_view()
        
        # Status bar
        self._create_status_bar()
        
        # Controlli di ordinamento
        self._create_sort_controls()
    
    def _create_directory_frame(self):
        """Create directory selection frame"""
        self.dir_frame = ttk.LabelFrame(self.main_frame, text=lang.get_string('select_directory'))
        self.dir_frame.pack(fill='x', padx=10, pady=5)
        
        self.dir_entry = ttk.Entry(self.dir_frame, width=50)
        self.dir_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        
        self.browse_btn = ttk.Button(self.dir_frame, text=lang.get_string('browse'), command=self.browse_directory)
        self.browse_btn.pack(side='left', padx=5, pady=5)

    def _create_actions_frame(self):
        """Create actions frame with buttons"""
        self.actions_frame = ttk.LabelFrame(self.main_frame, text=lang.get_string('actions'))
        self.actions_frame.pack(fill='x', padx=10, pady=5)
        
        # Scan button
        self.scan_btn = ttk.Button(
            self.actions_frame,
            text=lang.get_string('scan_the_movies'),
            command=self.start_scan
        )
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        self.export_btn = ttk.Button(
            self.actions_frame,
            text=lang.get_string('export_to_csv'),
            command=self.export_to_csv
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Import button
        self.import_btn = ttk.Button(
            self.actions_frame,
            text=lang.get_string('import_csv'),
            command=self.import_from_csv
        )
        self.import_btn.pack(side=tk.LEFT, padx=5)
        
        # Load button
        self.load_btn = ttk.Button(
            self.actions_frame,
            text=lang.get_string('load_db'),
            command=self.load_movies_from_database
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        self.close_btn = ttk.Button(
            self.actions_frame,
            text=lang.get_string('close'),
            command=self.close_database
        )
        self.close_btn.pack(side=tk.RIGHT, padx=5)
    
    def _create_progress_bar(self):
        """Create progress bar"""
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill='x', padx=10, pady=5)
        
        self.progress = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill='x', padx=5, pady=5)
    
    def _create_tree_view(self):
        """Create tree view with scrollbar"""
        print("Creating tree view...")
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Define columns
        columns = ("id", "genres", "movie_name", "title", "year", "path")
        
        # Create Treeview
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("genres", text=lang.get_string('genres'))
        self.tree.heading("movie_name", text=lang.get_string('movie_name'))
        self.tree.heading("title", text=lang.get_string('title'))
        self.tree.heading("year", text=lang.get_string('year'))
        self.tree.heading("path", text=lang.get_string('path'))
        
        # Set column widths
        self.tree.column("id", width=50, anchor='center')
        self.tree.column("genres", width=150, anchor='w')
        self.tree.column("movie_name", width=200, anchor='w')
        self.tree.column("title", width=200, anchor='w')
        self.tree.column("year", width=80, anchor='center')
        self.tree.column("path", width=300, anchor='w')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout within tree frame
        self.tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', padx=5, pady=5)
        
        # Configure tree frame to expand with window
        tree_frame.pack_propagate(True)
        
        # Ensure tree is visible
        tree_frame.update_idletasks()
        
        print("Tree view created successfully")
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_frame = ttk.Label(
            self.root, 
            text=lang.get_string('ready'),
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Aggiorna il contatore iniziale
        self.update_movie_count(len(self.database.get_all_movies() if self.database else []))
        
    def update_movie_count(self, count):
        """Aggiorna il contatore dei film nella barra di stato"""
        if hasattr(self, 'status_frame'):
            self.status_frame.config(text=f"{lang.get_string('total_movies')}: {count}")
            
    def _create_search_frame(self):
        """Create search frame with search box and button"""
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill='x', padx=10, pady=(5, 0))
        
        # Search label
        ttk.Label(self.search_frame, text=tr('search') + ':').pack(side='left', padx=(0, 5))
        
        # Search entry with placeholder
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_frame, 
            textvariable=self.search_var, 
            width=40,
            style='Search.TEntry'
        )
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        self.search_entry.bind('<FocusIn>', self._on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_search_focus_out)
        
        # Set initial placeholder
        self._show_placeholder()
        
        # Clear button
        self.clear_btn = ttk.Button(
            self.search_frame, 
            text=tr('clear'), 
            command=self._clear_search,
            width=8
        )
        self.clear_btn.pack(side='left', padx=(5, 0))
        
        # Initialize movies list
        if not hasattr(self, 'all_movies'):
            self.all_movies = []
        
    def _show_placeholder(self):
        """Show placeholder text in search box"""
        if not self.search_var.get():
            self.search_entry.insert(0, tr('search_placeholder'))
            self.search_entry.config(foreground='grey')
    
    def _hide_placeholder(self):
        """Hide placeholder text"""
        if self.search_var.get() == tr('search_placeholder'):
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground='black')
    
    def _on_search_focus_in(self, event):
        """Handle focus in event for search box"""
        if self.search_var.get() == tr('search_placeholder'):
            self._hide_placeholder()
    
    def _on_search_focus_out(self, event):
        """Handle focus out event for search box"""
        if not self.search_var.get():
            self._show_placeholder()

    def _on_search_change(self, event=None):
        """Handle search text changes"""
        # Skip if the change was due to placeholder text
        if hasattr(self, 'search_var') and self.search_var.get() == tr('search_placeholder'):
            return
            
        search_term = self.search_var.get().lower() if hasattr(self, 'search_var') else ''
        
        # Clear current selection
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # If search is empty, show all movies
        if not search_term:
            for movie in self.all_movies:
                # Use the movie's path as the unique ID since it should be unique for each movie
                item_id = f"{movie[3]}"  # Assuming path is the 4th element (0-based index 3)
                try:
                    self.tree.insert('', 'end', values=movie[1:], iid=item_id)
                except tk.TclError:
                    # If item already exists, skip it
                    continue
            return
        
        # Filter movies based on search term
        found = False
        for movie in self.all_movies:
            # Check if any field contains the search term
            if any(search_term in str(field).lower() for field in movie[1:]):
                item_id = f"{movie[3]}"  # Using path as the unique ID
                try:
                    self.tree.insert('', 'end', values=movie[1:], iid=item_id)
                    found = True
                except tk.TclError:
                    # If item already exists, skip it
                    continue
        
        # Show message if no results found
        if not found and search_term:
            self.tree.insert('', 'end', values=['', tr('no_results'), ''], tags=('no_results',))
            self.tree.tag_configure('no_results', foreground='gray', font=('TkDefaultFont', 9, 'italic'))

    def _clear_search(self):
        """Clear the search box and show all movies"""
        if hasattr(self, 'search_var'):
            self.search_var.set('')
            self._on_search_change()
            if hasattr(self, 'search_entry'):
                self._show_placeholder()
                self.search_entry.focus_set()

    def update_status(self, message):
        """Aggiorna il messaggio di stato"""
        if hasattr(self, 'status_frame'):
            self.status_frame.config(text=message)
        self.root.update_idletasks()  # Force update to show status changes immediately

    def browse_directory(self):
        """Browse for directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def new_database(self):
        """Create a new database"""
        if messagebox.askyesno(lang.get_string('new_database'), lang.get_string('create_new_db')):
            try:
                # Create database in user's documents folder to avoid permission issues
                documents_path = os.path.join(os.path.expanduser("~"), "Documents")
                db_path = os.path.join(documents_path, "movie_catalog.db")
                
                # Remove existing database if it exists
                if os.path.exists(db_path):
                    os.remove(db_path)
                
                # Create new database
                self.database = Database(db_path)
                if not self.database.initialize():
                    raise Exception("Failed to initialize database")
                
                # Update GUI - only clear tree if it exists
                if hasattr(self, 'tree') and self.tree:
                    self.tree.delete(*self.tree.get_children())
                
                # Create tree view if it doesn't exist
                if not hasattr(self, 'tree') or not self.tree:
                    self._create_tree_view()
                
                # Update close button state
                if hasattr(self, 'close_database_btn'):
                    self.close_database_btn.configure(state='normal')
                
                messagebox.showinfo(lang.get_string('success'), f"{lang.get_string('db_created')} {db_path}")
                return True
            except Exception as e:
                messagebox.showerror(lang.get_string('error'), f"{lang.get_string('db_create_failed')}: {str(e)}")
                # Reset database to None if creation fails
                self.database = None
                return False
        return False

    def open_database(self):
        """Open an existing database"""
        filename = filedialog.askopenfilename(
            title=lang.get_string('open_database'),
            filetypes=[('SQLite Database', '*.db'), ('All files', '*.*')]
        )
        if filename:
            try:
                self.database = Database(filename)
                if not self.database.initialize():
                    raise Exception("Failed to initialize database")
                
                # Update GUI - only clear tree if it exists
                if hasattr(self, 'tree') and self.tree:
                    self.tree.delete(*self.tree.get_children())
                
                # Create tree view if it doesn't exist
                if not hasattr(self, 'tree') or not self.tree:
                    self._create_tree_view()
                
                # Update close button state
                if hasattr(self, 'close_database_btn'):
                    self.close_database_btn.configure(state='normal')
                
                messagebox.showinfo(lang.get_string('success'), f"{lang.get_string('db_opened')} {filename}")
                return True
            except Exception as e:
                messagebox.showerror(lang.get_string('error'), f"{lang.get_string('db_open_failed')}: {str(e)}")
                self.database = None
                return False
        return False

    def close_database(self):
        """Close the current database"""
        if messagebox.askyesno(lang.get_string('close_database'), lang.get_string('close_db')):
            try:
                self.database = None
                if self.tree:
                    self.tree.delete(*self.tree.get_children())
                if hasattr(self, 'close_database_btn'):
                    self.close_database_btn.configure(state='disabled')
                messagebox.showinfo(lang.get_string('success'), lang.get_string('db_closed'))
            except Exception as e:
                messagebox.showerror(lang.get_string('error'), f"{lang.get_string('db_close_failed')}: {str(e)}")
            return False
                
        return False

    def scan_directory(self, directory):
        """Scan directory for movies and update progress"""
        try:
            scanner = MovieScanner(directory, self.result_queue)
            scanner.scan()
        except Exception as e:
            messagebox.showerror(lang.get_string('error'), f"{lang.get_string('scan_failed')}: {str(e)}")
            self.scanning = False
            self.scan_btn.configure(state="normal")
            self.export_btn.configure(state="normal")
            self.load_btn.configure(state="normal")
            self.update_status(lang.get_string('ready'))
            self.result_queue.put('finished')

    def start_scan(self):
        """Start scanning for movies in selected directory"""
        if not self.database:
            messagebox.showwarning(lang.get_string('error'), lang.get_string('db_not_initialized'))
            return
            
        directory = self.dir_entry.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showwarning(lang.get_string('warning'), lang.get_string('select_valid_directory'))
            return
            
        self.scan_btn.configure(state="disabled")
        self.export_btn.configure(state="disabled")
        self.load_btn.configure(state="disabled")
        self.progress['value'] = 0
        
        # Clear movies to save
        self.movies_to_save.clear()
        
        # Start scanning thread
        self.scanning = True
        self.scan_thread = threading.Thread(target=self.scan_directory, args=(directory,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        # Start processing results
        self.process_results()

    def process_results(self):
        """Process scan results and update GUI"""
        try:
            while True:
                try:
                    result = self.result_queue.get_nowait()
                    if not result or len(result) < 2:
                        print(f"Unexpected result format: {result}")
                        continue
                        
                    result_type = result[0]
                    data = result[1]
                    
                    if result_type == 'progress':
                        progress_value = data
                        self.progress['value'] = progress_value
                        self.update_status(f"{lang.get_string('scanning')}... {progress_value}%")
                    elif result_type == 'finished':
                        # Store all results in one batch
                        if self.movies_to_save:  # Only save if there are movies to save
                            print(f"Saving {len(self.movies_to_save)} movies to database...")
                            success = self.database.store_scanned_files(self.movies_to_save)
                            if not success:
                                messagebox.showerror("Error", "Failed to save some movies to the database")
                        
                        self.movies_to_save.clear()
                        self.scanning = False
                        self.update_status(lang.get_string('ready'))
                        messagebox.showinfo(lang.get_string('scan_complete'), 
                                          lang.get_string('scan_completed_message'))
                        self.scan_btn.configure(state="normal")
                        self.export_btn.configure(state="normal")
                        self.load_btn.configure(state="normal")
                        
                        # Refresh the movie list from the database
                        self.load_movies_from_database()
                        break
                    elif result_type == 'movie':
                        if len(data) >= 3:  # Ensure we have all required fields
                            genre, movie_name, path = data[:3]  # Only take first 3 elements
                            print(f"Processing movie: {genre}, {movie_name}, {path}")
                            
                            # Add to tree view if it exists
                            if hasattr(self, 'tree') and self.tree:
                                self.tree.insert("", "end", values=(genre, movie_name, path))
                            
                            # Add to list of movies to save
                            self.movies_to_save.append((genre, movie_name, path))
                    else:
                        print(f"Unknown result type: {result}")
                        
                except queue.Empty:
                    if self.scanning:
                        # Schedule the next check
                        self.root.after(100, self.process_results)
                    break
                    
        except Exception as e:
            print(f"Error in process_results: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror(lang.get_string('error'), 
                               f"{lang.get_string('process_results_failed')}: {str(e)}")
            if self.scanning:
                self.root.after(100, self.process_results)
                
        # Ensure tree is visible
        if self.tree:
            self.tree.pack(fill='both', expand=True)

    def export_to_csv(self):
        """Export movies to a CSV file"""
        if not hasattr(self, 'database') or not self.database:
            messagebox.showerror("Error", "Database not connected")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title=lang.get_string('export_csv_title')
        )
        
        if filename:
            count = self.database.export_to_csv(filename)
            if count > 0:
                messagebox.showinfo(
                    lang.get_string('export_success'),
                    lang.get_string('export_success_message').format(count=count, filename=filename)
                )
            elif count == 0:
                messagebox.showinfo(
                    lang.get_string('info'),
                    lang.get_string('no_movies_to_export')
                )
            else:  # count < 0 means error
                messagebox.showerror(
                    lang.get_string('export_error'),
                    lang.get_string('export_error_message')
                )
    
    def import_from_csv(self):
        """
        Import movies from a CSV file into the database
        
        Args:
            filename: Path to the CSV file to import
            
        Returns:
            tuple: (success: bool, imported_count: int, error_message: str)
        """
        if not hasattr(self, 'database') or not self.database:
            messagebox.showerror(
                lang.get_string('error'),
                lang.get_string('database_not_connected')
            )
            return
            
        filename = filedialog.askopenfilename(
            filetypes=[
                ("CSV files", "*.csv"), 
                ("All files", "*.*")
            ],
            title=lang.get_string('import_csv_title')
        )
        
        if not filename:
            return  # User cancelled
            
        try:
            # Show progress dialog
            progress = tk.Toplevel(self.root)
            progress.title(lang.get_string('importing'))
            progress.geometry("400x150")
            
            tk.Label(
                progress, 
                text=lang.get_string('importing_file').format(filename=os.path.basename(filename))
            ).pack(pady=10)
            
            progress_bar = ttk.Progressbar(
                progress, 
                orient='horizontal', 
                length=300, 
                mode='indeterminate'
            )
            progress_bar.pack(pady=20)
            progress_bar.start()
            
            # Force UI update
            progress.update()
            
            # Log the import attempt
            self.logger.info(f"Attempting to import movies from: {filename}")
            
            # Perform the import
            imported_count, skipped_count, error_count, error_details = self.database.import_from_csv(filename)
            
            # Log the result
            self.logger.info(
                f"Import completed - "
                f"Imported: {imported_count}, "
                f"Skipped: {skipped_count}, "
                f"Errors: {error_count}"
            )
            
            # Update UI
            progress.destroy()
            
            # Mostra il risultato all'utente
            if error_count == 0 and imported_count > 0:
                # Successo completo
                message = lang.get_string('import_success_message').format(
                    count=imported_count,
                    skipped=skipped_count,
                    errors=error_count
                )
                return True, message, []
                
            elif imported_count > 0:
                # Successo parziale (con errori)
                message = lang.get_string('import_partial_success_message').format(
                    count=imported_count,
                    skipped=skipped_count,
                    errors=error_count
                )
                
                # Prepara i dettagli degli errori
                details = ["Dettagli errori:"]
                details.extend(error_details[:10])  # Mostra massimo 10 errori
                if len(error_details) > 10:
                    details.append(f"... e altri {len(error_details) - 10} errori")
                
                return False, message, details
                
            else:
                # Fallimento completo
                message = lang.get_string('import_failed_message')
                if error_details:
                    details = ["Dettagli errori:"]
                    details.extend(error_details[:10])  # Mostra massimo 10 errori
                    if len(error_details) > 10:
                        details.append(f"... e altri {len(error_details) - 10} errori")
                    return False, message, details
                return False, message, ["Nessun film è stato importato a causa di errori."]
                
        except Exception as e:
            import traceback
            error_msg = f"Errore durante l'importazione: {str(e)}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return False, error_msg, [f"Dettaglio errore: {str(e)}"]

    def load_from_database(self):
        """Load movies from database into treeview"""
        if not self.database:
            messagebox.showwarning(lang.get_string('error'), lang.get_string('db_not_initialized'))
            return
            
        try:
            movies = self.database.get_all_movies()
            if not self.tree:
                self._create_tree_view()
            
            # Clear existing items and store all movies
            self.all_movies = []
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insert movies and store them for filtering
            for i, movie in enumerate(movies):
                self.all_movies.append((i,) + movie)  # Add unique ID for each movie
                self.tree.insert("", "end", values=movie, iid=str(i))
                
            messagebox.showinfo(lang.get_string('success'), lang.get_string('movies_loaded'))
        except Exception as e:
            messagebox.showerror(lang.get_string('error'), f"{lang.get_string('load_movies_failed')}: {str(e)}")
            
    def _configure_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        
        # Configure search entry style
        style.configure('Search.TEntry',
                       padding=5,
                       relief='flat',
                       foreground='grey')
        
        # Configure treeview style
        style.configure('Treeview',
                       rowheight=25,
                       fieldbackground='white')
        style.configure('Treeview.Heading',
                       font=('TkDefaultFont', 10, 'bold'))
        
        # Configure button style
        style.configure('TButton', padding=5)
        
        # Configure status bar style
        style.configure('Status.TLabel',
                       padding=(5, 2, 5, 2),
                       background='#f0f0f0',
                       relief='sunken',
                       anchor='w')
        
        # Configure progress bar style
        style.configure('TProgressbar',
                       thickness=20,
                       background='#4CAF50')

    def show_options(self):
        """Show the options/settings dialog."""
        from struttura.options import OptionsDialog
        OptionsDialog(self.root)
        logger.logger.info("Options dialog opened")
    
    def check_for_updates(self):
        """Check for application updates."""
        from struttura.updates import check_for_updates
        
        try:
            check_for_updates(self.root, __version__)
        except Exception as e:
            logger.logger.error(f"Error in update check: {str(e)}")
            messagebox.showerror(
                lang.get_string('error'),
                f"{lang.get_string('error_checking_updates')}: {str(e)}"
            )

    def _add_movie_with_metadata(self):
        """Open the movie details dialog to add a new movie with metadata."""
        if not hasattr(self, 'database') or not self.database:
            messagebox.showwarning(tr('error'), tr('db_not_initialized'))
            return
            
        def on_save_metadata(metadata):
            try:
                # Save the movie to the database
                success = self.database.add_movie_with_metadata(
                    title=metadata['title'],
                    year=metadata['year'],
                    path="",  # You'll need to set this
                    poster_url=metadata['poster_url'],
                    backdrop_url=metadata['backdrop_url'],
                    overview=metadata['overview'],
                    rating=metadata['rating'],
                    runtime=metadata['runtime'],
                    director=metadata['director'],
                    cast=json.dumps(metadata['cast']),
                    genres=json.dumps(metadata['genres']),
                    imdb_id=metadata['imdb_id']
                )
                
                if success:
                    messagebox.showinfo(tr('success'), tr('movie_added_successfully'))
                    self.load_movies_from_database()
                else:
                    messagebox.showerror(tr('error'), tr('failed_to_add_movie'))
                    
            except Exception as e:
                messagebox.showerror(tr('error'), f"{tr('error_occurred')}: {str(e)}")
        
        # Open the movie details dialog
        dialog = MovieDetailsDialog(
            parent=self.root,
            title=tr('add_new_movie'),
            on_save=on_save_metadata
        )
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def empty_database(self):
        """Svuota il database dei film"""
        if not hasattr(self, 'database') or self.database is None:
            messagebox.showerror(
                lang.get_string('error'),
                lang.get_string('db_not_initialized')
            )
            self.logger.error("Tentativo di svuotare il database non inizializzato")
            return
            
        # Chiedi conferma all'utente
        confirm = messagebox.askyesno(
            lang.get_string('warning'),
            lang.get_string('confirm_empty_database')
        )
        
        if not confirm:
            return
            
        try:
            # Mostra un messaggio di attesa
            if hasattr(self, 'status_frame'):
                self.status_frame.config(text=lang.get_string('emptying_database') + '...')
            self.root.update_idletasks()
            
            # Imposta un timeout più lungo per l'operazione
            success = False
            max_retries = 3
            retry_delay = 5  # secondi
            
            for attempt in range(max_retries):
                try:
                    # Prova a svuotare il database
                    success = self.database.empty_database()
                    if success:
                        break
                        
                except Exception as e:
                    error_msg = f"Errore durante lo svuotamento (tentativo {attempt + 1}/{max_retries}): {str(e)}"
                    self.logger.error(error_msg)
                    
                    if attempt < max_retries - 1:
                        self.logger.info(f"Riprovo tra {retry_delay} secondi...")
                        time.sleep(retry_delay)
                    else:
                        raise  # Rilancia l'eccezione dopo l'ultimo tentativo
            
            if success:
                # Aggiorna l'interfaccia utente
                if hasattr(self, 'tree'):
                    for item in self.tree.get_children():
                        self.tree.delete(item)
                
                messagebox.showinfo(
                    lang.get_string('success'),
                    lang.get_string('database_emptied_successfully')
                )
                self.logger.info("Database svuotato con successo")
                if hasattr(self, 'status_frame'):
                    self.status_frame.config(text=lang.get_string('database_emptied_successfully'))
            else:
                raise Exception("Operazione fallita senza errori specifici")
                
            return success
            
        except Exception as e:
            error_msg = f"{lang.get_string('error_emptying_database')}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            messagebox.showerror(
                lang.get_string('error'),
                error_msg
            )
            if hasattr(self, 'status_frame'):
                self.status_frame.config(text=lang.get_string('error_emptying_database'))
            return False

    def _create_sort_controls(self):
        """Crea i controlli per l'ordinamento"""
        # Frame per i controlli di ordinamento
        sort_frame = ttk.LabelFrame(self.main_frame, text=lang.get_string('sort_by'), padding=5)
        sort_frame.pack(fill='x', padx=5, pady=5)
        
        # Inizializza le variabili di ordinamento se non esistono
        if not hasattr(self, 'sort_by'):
            self.sort_by = tk.StringVar(value='title')
        if not hasattr(self, 'sort_order'):
            self.sort_order = tk.StringVar(value='ASC')
        
        # Etichetta e menu a tendina per il campo di ordinamento
        ttk.Label(sort_frame, text=lang.get_string('sort_field') + ":").pack(side='left', padx=5)
        
        # Opzioni di ordinamento con testi localizzati
        sort_options = [
            ('title', lang.get_string('sort_field_title')),
            ('year', lang.get_string('sort_field_year')),
            ('genre', lang.get_string('sort_field_genre')),
            ('rating', lang.get_string('sort_field_rating')),
            ('runtime', lang.get_string('sort_field_runtime')),
            ('path', lang.get_string('sort_field_path')),
            ('movie_name', lang.get_string('sort_field_movie_name'))
        ]
        
        # Crea il menu a tendina con i valori localizzati
        sort_menu = ttk.Combobox(
            sort_frame, 
            textvariable=self.sort_by,
            values=[opt[1] for opt in sort_options],
            state='readonly',
            width=15
        )
        sort_menu.pack(side='left', padx=5)
        
        # Imposta il valore predefinito
        sort_menu.set(lang.get_string('sort_field_title'))
        
        # Mappa i valori localizzati ai nomi dei campi del database
        self.sort_field_map = {opt[1]: opt[0] for opt in sort_options}
        
        # Pulsanti per l'ordine crescente/decrescente
        sort_order_frame = ttk.Frame(sort_frame)
        sort_order_frame.pack(side='left', padx=5)
        
        ttk.Radiobutton(
            sort_order_frame, 
            text="↑ " + lang.get_string('sort_asc'),
            variable=self.sort_order, 
            value='ASC',
            command=self.on_sort_changed
        ).pack(side='left', padx=2)
        
        ttk.Radiobutton(
            sort_order_frame, 
            text="↓ " + lang.get_string('sort_desc'),
            variable=self.sort_order, 
            value='DESC',
            command=self.on_sort_changed
        ).pack(side='left', padx=2)
        
        # Pulsante di aggiornamento
        ttk.Button(
            sort_frame, 
            text=lang.get_string('refresh'),
            command=self.load_movies_from_database
        ).pack(side='right', padx=5)
        
        # Associa l'evento di cambio selezione al menu a tendina
        sort_menu.bind('<<ComboboxSelected>>', self.on_sort_changed)
        
        # Pulsante per resettare i filtri
        ttk.Button(
            sort_frame,
            text=lang.get_string('reset_filters'),
            command=self.reset_filters
        ).pack(side='right', padx=5)
        
    def on_sort_changed(self, event=None):
        """Gestisce il cambio del criterio di ordinamento"""
        self.load_movies_from_database()

if __name__ == "__main__":
    try:
        print("Starting Movie Catalog Application...")
        print("Initializing Tkinter...")
        root = tk.Tk()
        print("Creating MovieCatalogApp instance...")
        app = MovieCatalogApp(root)
        print("Application initialized successfully")
        
        # Check database connection and contents
        print("\n=== Database Status ===")
        if hasattr(app, 'database') and app.database:
            print("Database connection established")
            
            # List all tables
            try:
                cursor = app.database.connection.cursor(dictionary=True)
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print("\n=== Database Tables ===")
                for table in tables:
                    table_name = list(table.values())[0]
                    print(f"\nTable: {table_name}")
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
                    count = cursor.fetchone()['count']
                    print(f"  Rows: {count}")
                    
                    # Show first few rows if table is not empty
                    if count > 0:
                        cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 5")
                        rows = cursor.fetchall()
                        print("  First few rows:")
                        for row in rows:
                            print(f"  - {row}")
                
                cursor.close()
                
                # List all movies if movies table exists
                if any('movies' in t.values() for t in tables):
                    print("\n=== Movies in Database ===")
                    cursor = app.database.connection.cursor(dictionary=True)
                    cursor.execute("SELECT COUNT(*) as count FROM movies")
                    count = cursor.fetchone()['count']
                    print(f"Found {count} movies in database")
                    
                    if count > 0:
                        cursor.execute("""
                            SELECT id, title, year, path, genre, 
                                   director, rating, runtime, last_scanned
                            FROM movies
                            ORDER BY title
                            LIMIT 5
                        """)
                        movies = cursor.fetchall()
                        print("\nSample movies:")
                        for movie in movies:
                            print(f"\nID: {movie['id']}")
                            print(f"Title: {movie.get('title', 'N/A')}")
                            print(f"Year: {movie.get('year', 'N/A')}")
                            print(f"Genre: {movie.get('genre', 'N/A')}")
                            print(f"Path: {movie.get('path', 'N/A')}")
                    cursor.close()
                else:
                    print("\nNo movies table found in the database")
                    
            except Exception as e:
                print(f"Error checking database contents: {str(e)}")
        else:
            print("No database connection available")
        
        print("\nStarting main event loop...")
        root.mainloop()
        
    except Exception as e:
        import traceback
        error_msg = f"""
        Fatal error starting application:
        {str(e)}
        
        Traceback:
        {traceback.format_exc()}
        """
        print(error_msg)
        if 'root' in locals() and isinstance(root, tk.Tk):
            messagebox.showerror("Fatal Error", f"Failed to start application:\n{str(e)}")
        else:
            input("Press Enter to exit...")

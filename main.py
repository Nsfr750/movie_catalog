import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import json
from lang import lang
__version__ = "1.7.1"  # Keep this in sync with struttura/__init__.py
from struttura.menu import AppMenu
from struttura import db
from lang.lang import get_string as tr
from struttura import logger
from struttura.traceback import setup_exception_handling
from struttura.movie_details_dialog import MovieDetailsDialog
from struttura.movie_metadata import MovieMetadata

class Database:
    def __init__(self, root):
        self.db = None
        self.root = root
        self.connection = None
        self.cursor = None
        self.is_mysql = True  # We're using MySQL
        
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
        
    def get_all_movies(self):
        if self.db:
            return self.db.get_all_movies()
        return []
        
    def export_to_csv(self, filename):
        if self.db:
            return self.db.export_to_csv(filename)
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
                
                # Send results to queue
                self.queue.put((genre, movie_name, full_path))
                print(f"Added to queue: {genre}, {movie_name}, {full_path}")
                
                # Send progress update
                if self.total_files > 0:  # Prevent division by zero
                    progress = int((self.processed / self.total_files) * 100)
                    self.queue.put(('progress', progress))
        
        self.queue.put(('finished', None))
        print("Scan completed")

class MovieCatalogApp:
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title(f"{lang.get_string('app_title')} v{__version__}")
        self.root.geometry("1000x600")
        
        # Set up logging and exception handling
        self._setup_logging()
        
        # Configure styles
        self._configure_styles()
        
        # Initialize components
        self.result_queue = queue.Queue()
        self.database = Database(root)
        self.movies_to_save = []
        self.scanning = False
        
        # Initialize database before creating menu
        if not self.database.initialize():
            messagebox.showerror(lang.get_string('error'), lang.get_string('db_init_failed'))
            self.root.quit()
            return

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        self._create_gui_components()
        self.menu = AppMenu(self)
        self.update_status(lang.get_string('ready'))
        self.set_language('en')
        
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
            self.tree.heading("Genre", text=lang.get_string('genre'))
            self.tree.heading("Movie Name", text=lang.get_string('movie_name'))
            self.tree.heading("Path", text=lang.get_string('path'))
        
        # Update status
        if hasattr(self, 'status_label'):
            self.status_label.config(text=lang.get_string('ready'))

    def load_movies_from_database(self):
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
            for movie in movies:
                # Store movie with unique ID based on path
                movie_with_id = (movie[0],) + movie  # Keep original ID and add to values
                self.all_movies.append(movie_with_id)
                
                # Insert into tree with unique ID based on genre and name
                item_id = f"{movie[0]}_{movie[1]}"  # Using genre and movie name for ID
                self.tree.insert("", "end", values=movie, iid=item_id)
                
            messagebox.showinfo(lang.get_string('success'), lang.get_string('movies_loaded'))
        except Exception as e:
            messagebox.showerror(lang.get_string('error'), f"{lang.get_string('load_movies_failed')}: {str(e)}")
            
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
        
        # Add Movie button
        self.add_btn = ttk.Button(
            self.actions_frame,
            text=tr('add_movie'),
            command=self._add_movie_with_metadata
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        # Scan button
        self.scan_btn = ttk.Button(
            self.actions_frame,
            text=tr('scan'),
            command=self.start_scan
        )
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        # Load button
        self.load_btn = ttk.Button(
            self.actions_frame,
            text=tr('load_movies'),
            command=self.load_movies_from_database
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        self.export_btn = ttk.Button(
            self.actions_frame,
            text=tr('export_csv'),
            command=self.export_to_csv
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        self.close_btn = ttk.Button(
            self.actions_frame,
            text=tr('close_db'),
            command=self.close_database,
            state='disabled'
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
        
        # Create tree frame with proper padding
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Tree view with columns
        self.tree = ttk.Treeview(tree_frame, columns=("Genre", "Movie Name", "Path"), show="headings")
        
        # Set column headings
        self.tree.heading("Genre", text=lang.get_string('genre'))
        self.tree.heading("Movie Name", text=lang.get_string('movie_name'))
        self.tree.heading("Path", text=lang.get_string('path'))
        
        # Configure columns
        self.tree.column("Genre", width=100)
        self.tree.column("Movie Name", width=300)
        self.tree.column("Path", width=500)
        
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
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill='x', padx=10, pady=5)
        self.status_frame.pack_propagate(True)
        
        self.status_label = ttk.Label(self.status_frame, text=lang.get_string('ready'), anchor=tk.W)
        self.status_label.pack(fill='x', padx=5, pady=5)

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
        self.search_entry.bind('<KeyRelease>', self._on_search_change)
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
        """Update the status bar message"""
        self.status_label['text'] = message
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
                    result_type = result[0]
                    data = result[1]
                    
                    if result_type == 'progress':
                        progress_value = data
                        self.progress['value'] = progress_value
                        self.update_status(f"{lang.get_string('scanning')}... {progress_value}%")
                    elif result_type == 'finished':
                        # Store all results in one batch
                        self.database.db.store_scanned_files(self.movies_to_save)
                        self.movies_to_save.clear()
                        
                        self.scanning = False
                        self.update_status(lang.get_string('ready'))
                        messagebox.showinfo(lang.get_string('scan_complete'), lang.get_string('scan_completed_message'))
                        self.scan_btn.configure(state="normal")
                        self.export_btn.configure(state="normal")
                        self.load_btn.configure(state="normal")
                        break
                    elif result_type == 'movie':
                        genre, movie_name, path = data
                        print(f"Processing movie: {genre}, {movie_name}, {path}")
                        print(f"Tree exists: {self.tree is not None}")
                        if self.tree:
                            print(f"Tree items before insert: {len(self.tree.get_children())}")
                            # Insert movie into tree
                            self.tree.insert("", "end", values=(genre, movie_name, path))
                            print(f"Tree items after insert: {len(self.tree.get_children())}")
                        self.movies_to_save.append((genre, movie_name, path))
                    else:
                        print(f"Unknown result type: {result}")
                        continue
                except queue.Empty:
                    if self.scanning:
                        self.root.after(100, self.process_results)
                    break
        except Exception as e:
            print(f"Error in process_results: {str(e)}")
            messagebox.showerror(lang.get_string('error'), f"{lang.get_string('process_results_failed')}: {str(e)}")
            if self.scanning:
                self.root.after(100, self.process_results)
                
        # Ensure tree is visible
        if self.tree:
            self.tree.pack(fill='both', expand=True)

    def export_to_csv(self):
        """Export movies to CSV file"""
        filename = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            title=lang.get_string('export_to_csv')
        )
        if filename:
            try:
                self.database.export_to_csv(filename)
                messagebox.showinfo(lang.get_string('success'), f"{lang.get_string('data_exported')} {filename}")
            except Exception as e:
                messagebox.showerror(lang.get_string('error'), f"{lang.get_string('export_failed')}: {str(e)}")

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
                    path="",  # You might want to add a file dialog for this
                    poster_url=metadata['poster_url'],
                    backdrop_url=metadata['backdrop_url'],
                    overview=metadata['overview'],
                    rating=metadata['rating'],
                    runtime=metadata['runtime'],
                    director=metadata['director'],
                    cast=metadata['cast'],
                    genres=metadata['genres'],
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

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieCatalogApp(root)
    root.mainloop()

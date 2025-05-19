import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from queue import Queue, Empty
import csv
from db import MySQLDatabase
from datetime import datetime
from pathlib import Path
import re
from PIL import Image, ImageTk
from version import get_version
from about import About
from help import Help
from sponsor import Sponsor

class Database:
    def __init__(self, root):
        self.db = None
        self.root = root
        
    def initialize(self):
        self.db = MySQLDatabase(self.root)
        if not self.db.create_database():
            return False
            
        # Create tables if they don't exist
        if not self.db.create_tables():
            return False
            
        return True
        
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
        self.root = root
        self.root.title("Movie Catalog")
        self.root.geometry("1000x700")
        
        # Configure root window
        root.configure(bg='#f0f0f0')
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
        # Create menu
        self.create_menu()
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        
        # Initialize state
        self.scan_thread = None
        self.result_queue = Queue()
        self.scanning = False
        self.movies_to_save = []
        self.tree = None
        
        # Create database instance
        self.database = Database(root)
        if not self.database.initialize():
            # If database initialization fails, show config form
            config = self.database.db.config.show_config_form()
            if config:
                # Try initializing again with new config
                if not self.database.initialize():
                    messagebox.showerror("Error", "Failed to initialize database even after configuration")
                    root.destroy()
                    return
            else:
                messagebox.showerror("Error", "Failed to initialize database")
                root.destroy()
                return
        
        # Initialize GUI components
        self._create_gui_components()
        
        # Load movies from database
        self.load_movies_from_database()
        
        # Update status
        self.update_status("Ready")

    def load_movies_from_database(self):
        """Load movies from database into treeview"""
        if not self.database:
            return
            
        movies = self.database.get_all_movies()
        if not movies:
            return
            
        # Clear existing items
        if self.tree:
            for item in self.tree.get_children():
                self.tree.delete(item)
        
        # Insert movies
        for genre, movie_name, path in movies:
            self.tree.insert("", "end", values=(genre, movie_name, path))
    
    def _create_gui_components(self):
        """Create all GUI components"""
        # Directory selection frame
        self._create_directory_frame()
        
        # Actions frame
        self._create_actions_frame()
        
        # Progress bar
        self._create_progress_bar()
        
        # Tree view
        self._create_tree_view()
        
        # Status bar
        self._create_status_bar()
    
    def _create_directory_frame(self):
        """Create directory selection frame"""
        frame = ttk.LabelFrame(self.main_frame, text="Movie Directory", padding="10 5")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=(10, 5))
        
        self.path_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.path_var, width=50).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self.browse_directory).grid(row=0, column=1, padx=5, pady=5)
    
    def _create_actions_frame(self):
        """Create actions frame with buttons"""
        frame = ttk.LabelFrame(self.main_frame, text="Actions", padding="10 5")
        frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        # Create buttons
        self.scan_btn = ttk.Button(frame, text="Scan Movies", command=self.start_scan)
        self.export_btn = ttk.Button(frame, text="Export to CSV", command=self.export_to_csv)
        self.load_btn = ttk.Button(frame, text="Load from Database", command=self.load_from_database)
        
        # Grid buttons
        self.scan_btn.grid(row=0, column=0, padx=5, pady=5)
        self.export_btn.grid(row=0, column=1, padx=5, pady=5)
        self.load_btn.grid(row=0, column=2, padx=5, pady=5)
    
    def _create_progress_bar(self):
        """Create progress bar"""
        frame = ttk.Frame(self.main_frame)
        frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.progress = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
    
    def _create_tree_view(self):
        """Create tree view with scrollbar"""
        print("Creating tree view...")
        
        # Create tree frame with proper padding
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tree view with columns
        self.tree = ttk.Treeview(tree_frame, columns=("Genre", "Movie Name", "Path"), show="headings")
        
        # Set column headings
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Movie Name", text="Movie Name")
        self.tree.heading("Path", text="Path")
        
        # Configure columns
        self.tree.column("Genre", width=100)
        self.tree.column("Movie Name", width=300)
        self.tree.column("Path", width=500)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout within tree frame
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure tree frame to expand with window
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Ensure tree is visible
        tree_frame.update_idletasks()
        
        print("Tree view created successfully")
    
    def _create_status_bar(self):
        """Create status bar"""
        frame = ttk.Frame(self.main_frame)
        frame.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(frame, text="Ready", anchor=tk.W)
        self.status_label.grid(row=0, column=0, padx=5, pady=5)
        

    
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Add File menu items
        items = [
            ("New Database", self.new_database),
            ("Open Database", self.open_database),
            "separator",
            ("Close Database", self.close_database),
            "separator",
            ("Scan Directory", self.start_scan),
            "separator",
            ("Export to CSV", self.export_to_csv),
            "separator",
            ("Load from Database", self.load_from_database),
            "separator",
            ("Exit", self.root.quit)
        ]
        
        # Add items to menu
        for item in items:
            if item == "separator":
                file_menu.add_separator()
            else:
                label, command = item
                file_menu.add_command(label=label, command=command)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Add Help menu items
        help_menu.add_command(label="Help", command=lambda: Help.show_help(self.root))
        help_menu.add_command(label="About", command=lambda: About.show_about(self.root))
        help_menu.add_command(label="Sponsor", command=lambda: Sponsor(self.root).show_sponsor())

    def update_status(self, message):
        """Update the status bar message"""
        self.status_label['text'] = message
        self.root.update_idletasks()  # Force update to show status changes immediately

    def browse_directory(self):
        """Browse for directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)

    def new_database(self):
        """Create a new database"""
        if messagebox.askyesno("New Database", "Create a new database? This will clear all existing data."):
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
                
                messagebox.showinfo("Success", f"New database created successfully at: {db_path}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create new database: {str(e)}")
                # Reset database to None if creation fails
                self.database = None
                return False
        return False

    def open_database(self):
        """Open an existing database"""
        filename = filedialog.askopenfilename(
            title="Open Database",
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
                
                messagebox.showinfo("Success", f"Database opened successfully: {filename}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open database: {str(e)}")
                self.database = None
                return False
        return False

    def close_database(self):
        """Close the current database"""
        if messagebox.askyesno("Close Database", "Close the current database?"):
            try:
                self.database = None
                if self.tree:
                    self.tree.delete(*self.tree.get_children())
                if hasattr(self, 'close_database_btn'):
                    self.close_database_btn.configure(state='disabled')
                messagebox.showinfo("Success", "Database closed successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to close database: {str(e)}")

    def scan_directory(self, directory):
        """Scan directory for movies and update progress"""
        try:
            scanner = MovieScanner(directory, self.result_queue)
            scanner.scan()
        except Exception as e:
            messagebox.showerror("Error", f"Error scanning directory: {str(e)}")
            self.scanning = False
            self.scan_btn.configure(state="normal")
            self.export_btn.configure(state="normal")
            self.load_btn.configure(state="normal")
            self.update_status("Ready")
            self.result_queue.put('finished')

    def start_scan(self):
        """Start scanning for movies in selected directory"""
        if not self.database:
            messagebox.showwarning("Error", "Please create or open a database first")
            return
            
        directory = self.path_var.get()
        if not os.path.exists(directory):
            messagebox.showwarning("Error", "Please select a valid directory")
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
                    
                    if isinstance(result, tuple) and len(result) == 2 and result[0] == 'progress':
                        progress_value = result[1]
                        self.progress['value'] = progress_value
                        self.update_status(f"Scanning... {progress_value}%")
                    elif isinstance(result, tuple) and len(result) == 2 and result[0] == 'finished':
                        # Store all results in one batch
                        self.database.db.store_scanned_files(self.movies_to_save)
                        self.movies_to_save.clear()
                        
                        self.scanning = False
                        self.update_status("Ready")
                        messagebox.showinfo("Scan Complete", "Movie scanning completed!")
                        self.scan_btn.configure(state="normal")
                        self.export_btn.configure(state="normal")
                        self.load_btn.configure(state="normal")
                        break
                    elif isinstance(result, tuple) and len(result) == 3:
                        genre, movie_name, path = result
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
                except Empty:
                    if self.scanning:
                        self.root.after(100, self.process_results)
                    break
        except Exception as e:
            print(f"Error in process_results: {str(e)}")
            messagebox.showerror("Error", f"Error processing results: {str(e)}")
            if self.scanning:
                self.root.after(100, self.process_results)
                
        # Ensure tree is visible
        if self.tree:
            self.tree.update_idletasks()

    def export_to_csv(self):
        """Export movies to CSV file"""
        filename = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            title='Export to CSV'
        )
        if filename:
            try:
                self.database.export_to_csv(filename)
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")

    def load_from_database(self):
        """Load movies from database into treeview"""
        if not self.database:
            messagebox.showwarning("Error", "Please create or open a database first")
            return
            
        try:
            movies = self.database.get_all_movies()
            if not self.tree:
                self._create_tree_view()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insert movies
            for movie in movies:
                self.tree.insert("", "end", values=movie)
                
            messagebox.showinfo("Success", "Movies loaded from database")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load movies: {str(e)}")

    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            title='Save as CSV'
        )
        if filename:
            try:
                self.database.export_to_csv(filename)
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def load_from_database(self):
        """Load movies from database into treeview"""
        self.load_movies_from_database()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieCatalogApp(root)
    root.mainloop()

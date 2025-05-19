import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from queue import Queue
import sqlite3
import csv
from datetime import datetime
from pathlib import Path
import re
from PIL import Image, ImageTk
from version import get_version
from about import About
from help import Help
from sponsor import Sponsor

class Database:
    def __init__(self, db_path='movies.db'):
        self.db_path = db_path
        
    def create_connection(self):
        return sqlite3.connect(self.db_path)
        
    def create_tables(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT,
                movie_name TEXT,
                path TEXT UNIQUE,
                last_scanned DATETIME
            )
        ''')
        conn.commit()
        conn.close()
        
    def add_movie(self, genre, movie_name, path):
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO movies (genre, movie_name, path, last_scanned)
                VALUES (?, ?, ?, ?)
            ''', (genre, movie_name, path, datetime.now()))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        finally:
            conn.close()
            
    def get_all_movies(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT genre, movie_name, path FROM movies ORDER BY genre, movie_name')
        movies = cursor.fetchall()
        conn.close()
        return movies
        
    def export_to_csv(self, filename):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT genre, movie_name, path FROM movies ORDER BY genre, movie_name')
        movies = cursor.fetchall()
        conn.close()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Genre', 'Movie Name', 'Path'])
            writer.writerows(movies)

class MovieScanner:
    def __init__(self, root_path, queue):
        self.root_path = root_path
        self.queue = queue
        self.total_files = 0
        self.processed = 0
        
    def scan(self):
        self.total_files = sum([len(files) for r, d, files in os.walk(self.root_path)])
        self.processed = 0
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                    self.processed += 1
                    full_path = os.path.join(root, file)
                    
                    # Extract genre from directory name
                    genre = os.path.basename(os.path.dirname(full_path))
                    
                    # Extract movie name from filename (remove extensions)
                    movie_name = os.path.splitext(file)[0]
                    
                    # Send results to queue
                    self.queue.put((genre, movie_name, full_path))
                    
                    # Send progress update
                    self.queue.put(('progress', int((self.processed / self.total_files) * 100)))
        
        self.queue.put(('finished', None))

class MovieCatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Catalog")
        self.root.geometry("1000x700")
        
        # Configure root window
        root.configure(bg='#f0f0f0')
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
        # Create database instance
        self.database = Database()
        self.database.create_tables()
        
        # Create menu
        self.create_menu()
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        
        # Initialize GUI components
        self._create_gui_components()
        
        # Initialize state
        self.scan_thread = None
        self.result_queue = Queue()
        self.scanning = False
        self.movies_to_save = []
        
        # Initialize tree
        self.tree = None
        
        # Update status
        self.update_status("Ready")
    
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
        frame = ttk.LabelFrame(self.main_frame, text="Movie Catalog", padding="10 5")
        frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(5, 10))
        
        # Configure grid
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        # Create tree view
        self.tree = ttk.Treeview(frame, columns=("Genre", "Movie Name", "Path"), show="headings")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Movie Name", text="Movie Name")
        self.tree.heading("Path", text="Path")
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
    
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
            ("Close Database", self.close_database, 'disabled'),
            "separator",
            ("Exit", self.root.quit)
        ]
        
        for item in items:
            if item == "separator":
                file_menu.add_separator()
            else:
                label, command, *state = item
                if state:
                    file_menu.add_command(label=label, command=command, state=state[0])
                else:
                    file_menu.add_command(label=label, command=command)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Add Help menu items
        items = [
            ("Help", lambda: Help.show_help(self.root)),
            ("About", lambda: About.show_about(self.root)),
            ("Sponsor", lambda: Sponsor(self.root).show_sponsor())
        ]
        
        for label, command in items:
            help_menu.add_command(label=label, command=command)
    
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
        
    def update_status(self, message):
        """Update the status bar message"""
        self.status_label['text'] = message
        self.root.update_idletasks()  # Force update to show status changes immediately
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Add menu items with labels
        menu_items = set()
        
        # Add File menu items
        items = [
            ("New Database", self.new_database),
            ("Open Database", self.open_database),
            "separator",
            ("Close Database", self.close_database, 'disabled'),
            "separator",
            ("Exit", self.root.quit)
        ]
        
        for item in items:
            if item == "separator":
                file_menu.add_separator()
            else:
                label, command, *state = item
                if label not in menu_items:
                    menu_items.add(label)
                    if state:
                        file_menu.add_command(label=label, command=command, state=state[0])
                    else:
                        file_menu.add_command(label=label, command=command)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Add Help menu items
        items = [
            ("Help", lambda: Help.show_help(self.root)),
            ("About", lambda: About.show_about(self.root)),
            ("Sponsor", lambda: Sponsor(self.root).show_sponsor())
        ]
        
        for label, command in items:
            if label not in menu_items:
                menu_items.add(label)
                help_menu.add_command(label=label, command=command)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
            
    def start_scan(self):
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
        
        # Clear tree view
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Clear movies to save
        self.movies_to_save.clear()
        
        # Start scanning thread
        self.scanning = True
        self.scan_thread = threading.Thread(target=self.scan_directory, args=(directory,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        # Start processing results
        self.process_results()
        
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
                self.database.create_tables()
                
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
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create new database: {str(e)}")
                # Reset database to None if creation fails
                self.database = None
                
    def open_database(self):
        """Open an existing database"""
        filename = filedialog.askopenfilename(
            title="Open Database",
            filetypes=[('SQLite Database', '*.db'), ('All files', '*.*')]
        )
        if filename:
            try:
                self.database = Database(filename)
                self.database.create_tables()
                self.tree.delete(*self.tree.get_children())
                movies = self.database.get_all_movies()
                for movie in movies:
                    self.tree.insert("", "end", values=movie)
                self.close_database_btn.configure(state='normal')
                messagebox.showinfo("Success", f"Database {filename} opened successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open database: {str(e)}")
                
    def close_database(self):
        """Close the current database"""
        if messagebox.askyesno("Close Database", "Close the current database?"):
            try:
                self.database = None
                self.tree.delete(*self.tree.get_children())
                self.close_database_btn.configure(state='disabled')
                messagebox.showinfo("Success", "Database closed successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to close database: {str(e)}")
                
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
            
    def start_scan(self):
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
        
        # Clear tree view
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Clear movies to save
        self.movies_to_save.clear()
        
        # Start scanning thread
        self.scanning = True
        self.scan_thread = threading.Thread(target=self.scan_directory, args=(directory,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        # Start processing results
        self.process_results()
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
            
    def start_scan(self):
        directory = self.path_var.get()
        if not os.path.exists(directory):
            messagebox.showwarning("Error", "Please select a valid directory")
            return
            
        self.scan_btn.configure(state="disabled")
        self.export_btn.configure(state="disabled")
        self.load_btn.configure(state="disabled")
        self.progress['value'] = 0
        
        # Clear tree view
        for item in self.tree.get_children():
            self.tree.delete(item)
            
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
        try:
            while True:
                result = self.result_queue.get_nowait()
                
                if result[0] == 'progress':
                    self.progress['value'] = result[1]
                elif result[0] == 'finished':
                    # Save all movies to database in main thread
                    for genre, movie_name, path in self.movies_to_save:
                        self.database.add_movie(genre, movie_name, path)
                    
                    self.scanning = False
                    messagebox.showinfo("Scan Complete", "Movie scanning completed!")
                    self.scan_btn.configure(state="normal")
                    self.export_btn.configure(state="normal")
                    self.load_btn.configure(state="normal")
                    break
                else:
                    genre, movie_name, path = result
                    # Store movie for later database save
                    self.movies_to_save.append((genre, movie_name, path))
                    # Add to tree view immediately
                    self.tree.insert("", "end", values=(genre, movie_name, path))
                    
        except Exception:
            if self.scanning:
                self.root.after(100, self.process_results)

        # Scan button
        self.scan_btn = ttk.Button(buttons_frame, text="Scan Movies", command=self.start_scan)
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        self.export_btn = ttk.Button(buttons_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Load from database button
        self.load_btn = ttk.Button(buttons_frame, text="Load from Database", command=self.load_from_database)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Tree view
        self.tree = ttk.Treeview(self.main_frame, columns=("Genre", "Movie Name", "Path"), show="headings")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Movie Name", text="Movie Name")
        self.tree.heading("Path", text="Path")
        self.tree.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Scrollbar for tree view
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.scan_thread = None
        self.result_queue = Queue()
        self.scanning = False
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
            
    def start_scan(self):
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
        
        # Clear tree view if it exists
        if self.tree:
            for item in self.tree.get_children():
                self.tree.delete(item)
        else:
            messagebox.showwarning("Error", "Tree view not initialized")
            return
            
        # Clear movies to save
        self.movies_to_save.clear()
        
        # Start scanning thread
        self.scanning = True
        self.scan_thread = threading.Thread(target=self.scan_directory, args=(directory,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        # Start processing results
        self.process_results()
        
    def scan_directory(self, directory):
        scanner = MovieScanner(directory, self.result_queue)
        scanner.scan()
        
    def process_results(self):
        try:
            while True:
                result = self.result_queue.get_nowait()
                
                if result[0] == 'progress':
                    self.progress['value'] = result[1]
                elif result[0] == 'finished':
                    self.scanning = False
                    messagebox.showinfo("Scan Complete", "Movie scanning completed!")
                    self.scan_btn.configure(state="normal")
                    self.export_btn.configure(state="normal")
                    self.load_btn.configure(state="normal")
                    break
                else:
                    genre, movie_name, path = result
                    self.tree.insert("", "end", values=(genre, movie_name, path))
                    
        except Exception:
            if self.scanning:
                self.root.after(100, self.process_results)
    
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
        movies = self.database.get_all_movies()
        
        # Clear tree view
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add movies from database
        for movie in movies:
            self.tree.insert("", "end", values=movie)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieCatalogApp(root)
    root.mainloop()

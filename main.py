import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
from lang import lang
from struttura.version import get_version
from struttura.menu import AppMenu
from struttura import db

class Database:
    def __init__(self, root):
        self.db = None
        self.root = root
        
    def initialize(self):
        self.db = db.MySQLDatabase(self.root)
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
        self.root.title(f"{lang.get_string('app_title')} v{get_version()}")
        self.root.geometry("1000x600")
        
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
        
    def set_language(self, lang_code):
        lang.set_language(lang_code)
        self.update_ui_texts()

    def update_ui_texts(self):
        """Update all UI texts to the current language."""
        self.root.title(f"{lang.get_string('app_title')} v{get_version()}")
        self.dir_frame.config(text=lang.get_string('select_directory'))
        self.browse_btn.config(text=lang.get_string('browse'))
        self.actions_frame.config(text=lang.get_string('actions'))
        self.scan_btn.config(text=lang.get_string('scan_movies'))
        self.export_btn.config(text=lang.get_string('export_csv'))
        self.load_btn.config(text=lang.get_string('load_from_db'))
        self.tree.heading("Genre", text=lang.get_string('genre'))
        self.tree.heading("Movie Name", text=lang.get_string('movie_name'))
        self.tree.heading("Path", text=lang.get_string('path'))

    def load_movies_from_database(self):
        """Load movies from database into treeview"""
        if not self.database or not self.database.db:
            messagebox.showerror(lang.get_string('error'), lang.get_string('db_not_initialized'))
            return
            
        movies = self.database.get_all_movies()
        if not movies:
            messagebox.showinfo(lang.get_string('info'), lang.get_string('no_movies_found'))
            return
            
        # Clear existing items
        if self.tree:
            for item in self.tree.get_children():
                self.tree.delete(item)
        
        # Insert movies
        for genre, movie_name, path in movies:
            self.tree.insert("", "end", values=(genre, movie_name, path))
    
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
        
        # Create buttons
        self.scan_btn = ttk.Button(self.actions_frame, text=lang.get_string('scan_movies'), command=self.start_scan)
        self.export_btn = ttk.Button(self.actions_frame, text=lang.get_string('export_csv'), command=self.export_to_csv)
        self.load_btn = ttk.Button(self.actions_frame, text=lang.get_string('load_from_db'), command=self.load_from_database)
        
        # Grid buttons
        self.scan_btn.pack(side='left', padx=5, pady=5)
        self.export_btn.pack(side='left', padx=5, pady=5)
        self.load_btn.pack(side='left', padx=5, pady=5)
    
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
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insert movies
            for movie in movies:
                self.tree.insert("", "end", values=movie)
                
            messagebox.showinfo(lang.get_string('success'), lang.get_string('movies_loaded'))
        except Exception as e:
            messagebox.showerror(lang.get_string('error'), f"{lang.get_string('load_movies_failed')}: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieCatalogApp(root)
    root.mainloop()

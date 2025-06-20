import tkinter as tk
from tkinter import ttk
import webbrowser

class Help:
    def __init__(self, root):
        self.root = root

    def show(self):
        help_dialog = tk.Toplevel(self.root)
        help_dialog.title('Help')
        help_dialog.geometry('500x600') # larg X alt
        help_dialog.transient(self.root)
        help_dialog.grab_set()

        # Create a notebook for different help sections
        notebook = ttk.Notebook(help_dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Usage Tab
        usage_frame = ttk.Frame(notebook)
        notebook.add(usage_frame, text='Usage')
        
        usage_text = '''
        Movie Catalog Help
        
        1. Basic Usage:
        - Click "Browse" to select your movie directory
        - Click "Scan Movies" to start scanning
        - Progress will be shown in the progress bar
        - Movies will be displayed in the tree view
        
        2. Database Features:
        - Movies are automatically saved to MySQL database
        - Click "Load from Database" to view stored movies
        - Use "Export to CSV" to save movies to a CSV file
        - Database configuration can be modified in MySQLConfig
        
        3. File Organization:
        - Movies should be organized in genre directories
        - Supported file extensions: .mp4, .mkv, .avi, .mov, .webm, .mpg, .mpeg, .wmv, .flv, .m4v, .vob, .divx
        - Genre is extracted from directory names
        - Movie name is extracted from filenames
        - Progress is shown during scanning
        - Status updates are displayed in the status bar
        
        4. Additional Features:
        - Help dialog provides detailed usage information
        - About dialog shows application information
        - Sponsorship options available
        - Improved error handling and user feedback
        '''
        
        usage_label = ttk.Label(usage_frame, text=usage_text, justify='left')
        usage_label.pack(padx=5, pady=5)

        # Documentation Tab
        docs_frame = ttk.Frame(notebook)
        notebook.add(docs_frame, text='Documentation')
        
        docs_text = '''
        Documentation Links:
        - GitHub Repository: https://github.com/Nsfr750/movie_catalog
        - Project Documentation: https://nsfr750.github.io/movie_catalog
        - Issue Tracker: https://github.com/Nsfr750/movie_catalog/issues
        
        5. Support:
        - For support, please open an issue in GitHub
        - Check the documentation for more information
        - Visit the project website for updates and news
        - GitHub Repository: https://github.com/Nsfr750/movie-catalog
        - User Guide: https://github.com/Nsfr750/movie-catalog/docs/readme.md
        - Report Issues: https://github.com/Nsfr750/movie-catalog/issues
        '''
        
        docs_label = ttk.Label(docs_frame, text=docs_text, justify='left')
        docs_label.pack(padx=5, pady=5)

        # Support Tab
        support_frame = ttk.Frame(notebook)
        notebook.add(support_frame, text='Support')
        
        support_text = '''
        Support Options:
        - Email: nsfr750@yandex.com
        - GitHub Issues: https://github.com/Nsfr750/movie-catalog/issues
        - Discord: https://discord.gg/BvvkUEP9
        '''
        
        support_label = ttk.Label(support_frame, text=support_text, justify='left')
        support_label.pack(padx=5, pady=5)

        # Add a close button
        close_btn = ttk.Button(help_dialog, text='Close', command=help_dialog.destroy)
        close_btn.pack(pady=5)

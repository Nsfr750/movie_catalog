import tkinter as tk
from tkinter import ttk
import sys
import os

# Add project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from struttura.version import __version__
from lang.lang import get_string as tr

class About:
    def __init__(self, root):
        self.root = root
        self.about_dialog = None

    def show(self):
        """Show the about dialog."""
        if self.about_dialog is None or not self.about_dialog.winfo_exists():
            self.about_dialog = tk.Toplevel(self.root)
            self.about_dialog.title(tr('about_menu'))
            self.about_dialog.geometry('350x250')
            self.about_dialog.transient(self.root)
            self.about_dialog.grab_set()

            # Add app icon or logo here if you have one
            title = ttk.Label(self.about_dialog, text=tr('app_title'), font=('Helvetica', 16, 'bold'))
            title.pack(pady=20)

            # Get version dynamically from version.py
            version = ttk.Label(self.about_dialog, text=f"{tr('version')} {__version__}")
            version.pack()

            description = ttk.Label(self.about_dialog, text='', justify=tk.CENTER)
            description.pack(pady=20)

            copyright = ttk.Label(self.about_dialog, text='© 2025 Nsfr750')
            copyright.pack(pady=10)

            ttk.Button(
                self.about_dialog, 
                text=tr('close'), 
                command=self.about_dialog.destroy
            ).pack(pady=20)
        else:
            self.about_dialog.lift()

import tkinter as tk
from tkinter import ttk
from version import get_version

class About:
    @staticmethod
    def show_about(root):
        about_dialog = tk.Toplevel(root)
        about_dialog.title('About Movie Catalog')
        about_dialog.geometry('400x250') # larg X alt
        about_dialog.transient(root)
        about_dialog.grab_set()

        # Add app icon or logo here if you have one
        title = ttk.Label(about_dialog, text='Movie Catalog', font=('Helvetica', 16, 'bold'))
        title.pack(pady=20)

        # Get version dynamically from version.py
        version = ttk.Label(about_dialog, text=f'Version {get_version()}')
        version.pack()

        description = ttk.Label(about_dialog, text='A modern Python GUI application for\n managing and cataloging your movie collection.', justify=tk.CENTER)
        description.pack(pady=10)

        copyright = ttk.Label(about_dialog, text=' 2025 Nsfr750')
        copyright.pack(pady=10)

        ttk.Button(about_dialog, text='Close', command=about_dialog.destroy).pack(pady=10)

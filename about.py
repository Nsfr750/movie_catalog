import tkinter as tk
from tkinter import ttk
from version import get_version

class About:
    @staticmethod
    def show_about(root):
        about_dialog = tk.Toplevel(root)
        about_dialog.title('About Movie Catalog')
        about_dialog.geometry('600x400')
        about_dialog.transient(root)
        about_dialog.grab_set()

        # Add app icon or logo here if you have one
        title = ttk.Label(about_dialog, text='Movie Catalog', font=('Helvetica', 16, 'bold'))
        title.pack(pady=20)

        # Get version dynamically from version.py
        version = ttk.Label(about_dialog, text=f'Version {get_version()}')
        version.pack()

        description = ttk.Label(about_dialog, text='A Python GUI application for cataloging movies on your hard disk.\n This application recursively scans directories, extracts genres from directory names,\n and identifies movie files based on their extensions.', justify=tk.CENTER)
        description.pack(pady=20)

        copyright = ttk.Label(about_dialog, text=' 2025 Nsfr750')
        copyright.pack(pady=10)

        ttk.Button(about_dialog, text='Close', command=about_dialog.destroy).pack(pady=20)

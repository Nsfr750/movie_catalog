import tkinter as tk
from tkinter import ttk
import webbrowser
import os
import sys

# Add project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from lang.lang import get_string as tr

class Sponsor:
    def __init__(self, root):
        self.root = root
        self.sponsor_dialog = None

    def show_sponsor(self):
        """Show the sponsor dialog"""
        if not self.sponsor_dialog or not self.sponsor_dialog.winfo_exists():
            self.sponsor_dialog = tk.Toplevel(self.root)
            self.sponsor_dialog.title("Support the Project")
            self.sponsor_dialog.geometry("400x300")
            self.sponsor_dialog.transient(self.root)
            self.sponsor_dialog.grab_set()
            
            # Center the dialog
            window_width = 400
            window_height = 300
            screen_width = self.sponsor_dialog.winfo_screenwidth()
            screen_height = self.sponsor_dialog.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            self.sponsor_dialog.geometry(f'{window_width}x{window_height}+{x}+{y}')
            
            # Make window modal
            self.sponsor_dialog.protocol("WM_DELETE_WINDOW", self.on_close)
            
            # Add content
            ttk.Label(self.sponsor_dialog, text="Support the Project", font=('Helvetica', 14, 'bold')).pack(pady=10)
            ttk.Label(self.sponsor_dialog, text="If you find this project useful, please consider supporting it:").pack(pady=5)
            
            # GitHub Sponsors
            ttk.Button(
                self.sponsor_dialog, 
                text="GitHub Sponsors", 
                command=lambda: webbrowser.open("https://github.com/sponsors/Nsfr750")
            ).pack(pady=5, fill='x', padx=20)
            
            # Discord
            ttk.Button(
                self.sponsor_dialog, 
                text="Join Discord", 
                command=lambda: webbrowser.open("https://discord.gg/BvvkUEP9")
            ).pack(pady=5, fill='x', padx=20)
            
            # Buy Me a Coffee
            ttk.Button(
                self.sponsor_dialog, 
                text="Buy Me a Coffee", 
                command=lambda: webbrowser.open("https://paypal.me/3dmega")
            ).pack(pady=5, fill='x', padx=20)
            
            # Patreon
            ttk.Button(
                self.sponsor_dialog, 
                text="Become a Patron", 
                command=lambda: webbrowser.open("https://www.patreon.com/Nsfr750")
            ).pack(pady=5, fill='x', padx=20)
            
            # Close button
            ttk.Button(
                self.sponsor_dialog,
                text="Close",
                command=self.on_close
            ).pack(pady=10)
            
            # Set focus to the dialog
            self.sponsor_dialog.focus_set()
        else:
            self.sponsor_dialog.lift()
    
    # Close button
    def on_close(self):
        if self.sponsor_dialog:
            self.sponsor_dialog.destroy()
        else:
            self.about_dialog.lift()

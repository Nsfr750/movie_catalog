"""
Help dialog for the Movie Catalog application.

This module provides a comprehensive help system with multiple tabs for different
help topics, including usage instructions, documentation links, and support options.
"""
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import webbrowser
import os
import sys
from typing import Optional, Dict, Any

# Local imports
import sys
import os
from lang.lang import get_string as tr

# Try to get version
from struttura.version import __version__
VERSION = __version__

# Constants
GITHUB_REPO = "https://github.com/Nsfr750/movie_catalog"
ISSUE_TRACKER = f"{GITHUB_REPO}/issues"
DISCORD_LINK = "https://discord.gg/BvvkUEP9"
EMAIL = "nsfr750@yandex.com"

class HyperlinkManager:
    """Manage hyperlinks in a Text widget."""
    
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._on_enter)
        self.text.tag_bind("hyper", "<Leave>", self._on_leave)
        self.text.tag_bind("hyper", "<Button-1>", self._on_click)
        self.links: Dict[str, str] = {}
        self.text.config(cursor="arrow")

    def _on_enter(self, event):
        self.text.config(cursor="hand2")

    def _on_leave(self, event):
        self.text.config(cursor="arrow")

    def _on_click(self, event):
        for tag in self.text.tag_names("current"):
            if tag.startswith("hyper-"):
                url = self.links[tag]
                webbrowser.open(url)
                return

    def add(self, url: str) -> str:
        """Add a URL to the text widget."""
        tag = f"hyper-{len(self.links)}"
        self.links[tag] = url
        return tag

class HelpDialog:
    """Main help dialog for the application."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the help dialog.
        
        Args:
            root: The root window
        """
        self.root = root
        self.dialog: Optional[tk.Toplevel] = None
    
    def show(self) -> None:
        """Show the help dialog."""
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.lift()
            return
            
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title(f"{tr('help')} - Movie Catalog v{VERSION}")
        self.dialog.geometry('700x600')
        self.dialog.transient(self.root)
        self.dialog.grab_set()
        
        # Set minimum size
        self.dialog.minsize(600, 500)
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        
        # Create main container
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky='nsew')
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_font = tkfont.Font(size=12, weight='bold')
        ttk.Label(
            main_frame,
            text=tr('movie_catalog_help'),
            font=title_font
        ).grid(row=0, column=0, sticky='w', pady=(0, 10))
        
        # Create notebook for different help sections
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky='nsew', pady=(0, 10))
        
        # Add tabs
        self._create_usage_tab(notebook)
        self._create_documentation_tab(notebook)
        self._create_support_tab(notebook)
        self._create_shortcuts_tab(notebook)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, sticky='ew')
        
        ttk.Label(
            status_frame,
            text=f"Movie Catalog v{VERSION}",
            foreground='gray'
        ).pack(side='left')
        
        # Close button
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, sticky='e')
        
        ttk.Button(
            btn_frame,
            text=tr('close').capitalize(),
            command=self.dialog.destroy
        ).pack(side='right', padx=5)
        
        # Bind Escape key to close
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
    
    def _create_usage_tab(self, notebook: ttk.Notebook) -> None:
        """Create the Usage tab."""
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=tr('usage').capitalize())
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill='both', expand=True)
        
        yscroll = ttk.Scrollbar(text_frame)
        yscroll.pack(side='right', fill='y')
        
        text = tk.Text(
            text_frame,
            wrap='word',
            yscrollcommand=yscroll.set,
            padx=5,
            pady=5,
            font=('TkDefaultFont', 10),
            relief='flat',
            highlightthickness=0
        )
        text.pack(fill='both', expand=True)
        yscroll.config(command=text.yview)
        
        # Make text widget read-only
        text.config(state='normal')
        
        # Insert help text with formatting
        sections = [
            (tr('basic_usage').upper(), [
                tr('click_browse'),
                tr('click_scan'),
                tr('progress_shown'),
                tr('movies_displayed')
            ]),
            (tr('database_features').upper(), [
                tr('auto_save_db'),
                tr('load_from_db'),
                tr('export_csv'),
                tr('db_config')
            ]),
            (tr('file_organization').upper(), [
                tr('genre_directories'),
                tr('supported_formats'),
                tr('genre_extraction'),
                tr('name_extraction')
            ])
        ]
        
        for section, items in sections:
            text.insert('end', f"{section}\n", 'heading')
            for item in items:
                text.insert('end', f"• {item}\n")
            text.insert('end', '\n')
        
        # Configure tags for formatting
        text.tag_configure('heading', font=('TkDefaultFont', 10, 'bold'), spacing3=5)
        text.tag_configure('bullet', lmargin1=20, lmargin2=40)
        
        text.config(state='disabled')
    
    def _create_documentation_tab(self, notebook: ttk.Notebook) -> None:
        """Create the Documentation tab."""
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=tr('documentation').capitalize())
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill='both', expand=True)
        
        yscroll = ttk.Scrollbar(text_frame)
        yscroll.pack(side='right', fill='y')
        
        text = tk.Text(
            text_frame,
            wrap='word',
            yscrollcommand=yscroll.set,
            padx=5,
            pady=5,
            font=('TkDefaultFont', 10),
            relief='flat',
            highlightthickness=0,
            cursor='arrow'
        )
        text.pack(fill='both', expand=True)
        yscroll.config(command=text.yview)
        
        # Make text widget read-only
        text.config(state='normal')
        
        # Create hyperlink manager
        hyperlink = HyperlinkManager(text)
        
        # Insert documentation links
        text.insert('end', f"{tr('documentation_links').upper()}\n", 'heading')
        
        links = [
            (tr('github_repo'), GITHUB_REPO),
            (tr('user_guide'), f"{GITHUB_REPO}/blob/main/README.md"),
            (tr('api_docs'), f"{GITHUB_REPO}/wiki/API-Documentation")
        ]
        
        for name, url in links:
            tag = hyperlink.add(url)
            text.insert('end', '• ', 'bullet')
            text.insert('end', f"{name}: ", 'normal')
            text.insert('end', f"{url}\n", (tag, 'hyper'))
        
        text.insert('end', '\n')
        
        # Add support section
        text.insert('end', f"{tr('support').upper()}\n", 'heading')
        text.insert('end', f"• {tr('github_issue')}\n")
        text.insert('end', f"• {tr('check_docs')}\n")
        text.insert('end', f"• {tr('visit_website')}\n")
        
        # Configure tags
        text.tag_configure('heading', font=('TkDefaultFont', 10, 'bold'), spacing3=5)
        text.tag_configure('normal', font=('TkDefaultFont', 10))
        text.tag_configure('bullet', lmargin1=20, lmargin2=40)
        
        text.config(state='disabled')
    
    def _create_support_tab(self, notebook: ttk.Notebook) -> None:
        """Create the Support tab."""
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=tr('support').capitalize())
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill='both', expand=True)
        
        yscroll = ttk.Scrollbar(text_frame)
        yscroll.pack(side='right', fill='y')
        
        text = tk.Text(
            text_frame,
            wrap='word',
            yscrollcommand=yscroll.set,
            padx=5,
            pady=5,
            font=('TkDefaultFont', 10),
            relief='flat',
            highlightthickness=0,
            cursor='arrow'
        )
        text.pack(fill='both', expand=True)
        yscroll.config(command=text.yview)
        
        # Make text widget read-only
        text.config(state='normal')
        
        # Create hyperlink manager
        hyperlink = HyperlinkManager(text)
        
        # Insert support information
        text.insert('end', f"{tr('support_options').upper()}\n", 'heading')
        
        # Email
        text.insert('end', '• ', 'bullet')
        text.insert('end', f"{tr('email')}: ", 'normal')
        email_tag = hyperlink.add(f"mailto:{EMAIL}")
        text.insert('end', f"{EMAIL}\n", (email_tag, 'hyper'))
        
        # GitHub Issues
        text.insert('end', '• ', 'bullet')
        text.insert('end', f"{tr('github_issues')}: ", 'normal')
        issue_tag = hyperlink.add(ISSUE_TRACKER)
        text.insert('end', f"{ISSUE_TRACKER}\n", (issue_tag, 'hyper'))
        
        # Discord
        text.insert('end', '• ', 'bullet')
        text.insert('end', f"{tr('discord')}: ", 'normal')
        discord_tag = hyperlink.add(DISCORD_LINK)
        text.insert('end', f"{DISCORD_LINK}\n", (discord_tag, 'hyper'))
        
        # Configure tags
        text.tag_configure('heading', font=('TkDefaultFont', 10, 'bold'), spacing3=5)
        text.tag_configure('normal', font=('TkDefaultFont', 10))
        text.tag_configure('bullet', lmargin1=20, lmargin2=40)
        
        text.config(state='disabled')
    
    def _create_shortcuts_tab(self, notebook: ttk.Notebook) -> None:
        """Create the Keyboard Shortcuts tab."""
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=tr('keyboard_shortcuts').capitalize())
        
        # Create treeview for shortcuts
        columns = ('action', 'shortcut')
        tree = ttk.Treeview(
            frame,
            columns=columns,
            show='headings',
            selectmode='browse',
            height=10
        )
        
        # Define columns
        tree.heading('action', text=tr('action'))
        tree.heading('shortcut', text=tr('shortcut'))
        
        # Set column widths
        tree.column('action', width=250, anchor='w')
        tree.column('shortcut', width=150, anchor='w')
        
        # Add scrollbar
        yscroll = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=yscroll.set)
        
        # Pack tree and scrollbar
        tree.pack(side='left', fill='both', expand=True)
        yscroll.pack(side='right', fill='y')
        
        # Add shortcuts data
        shortcuts = [
            (tr('open_file'), 'Ctrl+O'),
            (tr('save'), 'Ctrl+S'),
            (tr('exit'), 'Alt+F4'),
            (tr('refresh'), 'F5'),
            (tr('search'), 'Ctrl+F'),
            (tr('open_settings'), 'Ctrl+,'),
            (tr('show_help'), 'F1')
        ]
        
        for action, shortcut in shortcuts:
            tree.insert('', 'end', values=(action, shortcut))

# For backward compatibility
Help = HelpDialog

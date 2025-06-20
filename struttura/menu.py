import tkinter as tk
from tkinter import Menu
from lang.lang import get_string, set_language
from .about import About
from .help import Help
from .sponsor import Sponsor

class AppMenu:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.create_menu()

    def create_menu(self):
        """Create application menu"""
        # File menu
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=get_string('file'), menu=self.file_menu)
        self.file_menu.add_command(label=get_string('new_database'), command=self.app.new_database)
        self.file_menu.add_command(label=get_string('open_database'), command=self.app.open_database)
        self.file_menu.add_command(label=get_string('close_database'), command=self.app.close_database)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=get_string('exit'), command=self.root.quit)

        # Language menu
        self.lang_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=get_string('language'), menu=self.lang_menu)
        self.lang_menu.add_command(label="English", command=lambda: self.app.set_language('en'))
        self.lang_menu.add_command(label="Italiano", command=lambda: self.app.set_language('it'))

        # Help menu
        self.create_help_menu()

    def create_help_menu(self):
        self.help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=get_string('help'), menu=self.help_menu)
        self.help_menu.add_command(label=get_string('documentation'), command=self.show_help_dialog)
        self.help_menu.add_command(label=get_string('sponsor'), command=self.show_sponsor_dialog)
        self.help_menu.add_separator()
        self.help_menu.add_command(label=get_string('about'), command=self.show_about_dialog)

    def show_about_dialog(self):
        about = About(self.app.root)
        about.show()

    def show_help_dialog(self):
        help_dialog = Help(self.app.root)
        help_dialog.show()

    def show_sponsor_dialog(self):
        sponsor = Sponsor(self.app.root)
        sponsor.show()

    def update_menu_text(self):
        """Update all menu texts."""
        self.menubar.entryconfig(self.menubar.index(self.file_menu), label=get_string('file'))
        self.file_menu.entryconfig(0, label=get_string('new_database'))
        self.file_menu.entryconfig(1, label=get_string('open_database'))
        self.file_menu.entryconfig(2, label=get_string('close_database'))
        self.file_menu.entryconfig(4, label=get_string('exit'))

        self.menubar.entryconfig(self.menubar.index(self.lang_menu), label=get_string('language'))

        self.menubar.entryconfig(self.menubar.index(self.help_menu), label=get_string('help'))
        self.help_menu.entryconfig(0, label=get_string('documentation'))
        self.help_menu.entryconfig(1, label=get_string('sponsor'))
        self.help_menu.entryconfig(self.help_menu.index('end'), label=get_string('about'))

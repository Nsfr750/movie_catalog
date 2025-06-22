import tkinter as tk
from tkinter import Menu
import lang.lang as lang
from lang.lang import get_string, set_language
from struttura.about import About
from struttura.help import Help
from struttura.sponsor import Sponsor
from struttura.log_viewer import LogViewer

class AppMenu:
    def __init__(self, app):
        self.app = app
        self.about_dialog = About(app.root)
        self.sponsor_dialog = Sponsor(app.root)
        self.help_dialog = Help(app.root)
        self.root = app.root
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.create_menu()

    def create_menu(self):
        """Create application menu"""
        # File menu
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=get_string('file_menu'), menu=self.file_menu)
        self.file_menu.add_command(label=get_string('new_database'), command=self.app.new_database)
        self.file_menu.add_command(label=get_string('open_database'), command=self.app.open_database)
        self.file_menu.add_command(label=get_string('close_database'), command=self.app.close_database)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=get_string('exit'), command=self.root.quit)

        # Language menu
        self.lang_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=get_string('language_menu'), menu=self.lang_menu)
        self.lang_menu.add_command(label="English", command=lambda: self.app.set_language('en'))
        self.lang_menu.add_command(label="Italiano", command=lambda: self.app.set_language('it'))

        # Tools menu
        self.tools_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=get_string('tools'), menu=self.tools_menu)
        
        # Database tools submenu
        self.db_tools_menu = Menu(self.tools_menu, tearoff=0)
        self.tools_menu.add_cascade(label=get_string('database_tools'), menu=self.db_tools_menu)
        
        # Add database tools
        self.db_tools_menu.add_command(
            label=get_string('create_database'),
            command=self.run_create_database
        )
        self.db_tools_menu.add_command(
            label=get_string('update_database'),
            command=self.run_update_database
        )
        self.db_tools_menu.add_command(
            label=get_string('empty_database'), 
            command=self.app.empty_database
        )
        
        self.tools_menu.add_separator()
        self.tools_menu.add_command(
            label=get_string('options'),
            command=self.app.show_options
        )
        self.tools_menu.add_command(
            label=get_string('log_viewer'),
            command=self.show_log_viewer
        )
        self.tools_menu.add_separator()
        self.tools_menu.add_command(
            label=get_string('check_for_updates'),
            command=self.app.check_for_updates
        )

        # Help menu
        self.create_help_menu()

    def create_help_menu(self):
        self.help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=get_string('help_menu'), menu=self.help_menu)
        self.help_menu.add_command(label=get_string('documentation'), command=self.show_help_dialog)
        self.help_menu.add_command(label=get_string('sponsor_menu'), command=self.show_sponsor)
        self.help_menu.add_separator()
        self.help_menu.add_command(label=get_string('about_menu'), command=self.show_about)

    def show_about(self):
        """Show the About dialog."""
        self.about_dialog.show()
        
    def show_help_dialog(self):
        """Show the Help dialog."""
        self.help_dialog.show()

    def show_sponsor(self):
        """Show the Sponsor dialog."""
        self.sponsor_dialog.show_sponsor()

    def show_log_viewer(self):
        """Show the log viewer window."""
        LogViewer(self.root)
        
    def run_create_database(self):
        """Run the create_database script."""
        try:
            from struttura.create_database import main as create_db_main
            create_db_main()
            messagebox.showinfo(
                get_string('success'),
                get_string('database_created_success')
            )
        except Exception as e:
            messagebox.showerror(
                get_string('error'),
                f"{get_string('database_creation_failed')}: {str(e)}"
            )
    
    def run_update_database(self):
        """Run the update_database script."""
        try:
            from struttura.update_database import main as update_db_main
            update_db_main()
            messagebox.showinfo(
                get_string('success'),
                get_string('database_updated_success')
            )
        except Exception as e:
            messagebox.showerror(
                get_string('error'),
                f"{get_string('database_update_failed')}: {str(e)}"
            )

    def update_menu_texts(self):
        """Update all menu texts with the current language"""
        # Get current menu state
        current_lang = lang.get_current_language()
        
        # Clear all menu items
        self.menubar.delete(0, 'end')
        
        # Recreate the menu structure with updated texts
        self.create_menu()
        
        # Restore the language selection
        lang.set_language(current_lang)
        
        # Update dialogs if they have the update_texts method
        for dialog in ['about_dialog', 'help_dialog']:
            if hasattr(self, dialog) and hasattr(getattr(self, dialog), 'update_texts'):
                getattr(self, dialog).update_texts()

    def update_menu_text(self):
        """Update all menu texts."""
        self.menubar.entryconfig(self.menubar.index(self.file_menu), label=get_string('file_menu'))
        self.file_menu.entryconfig(0, label=get_string('new_database'))
        self.file_menu.entryconfig(1, label=get_string('open_database'))
        self.file_menu.entryconfig(2, label=get_string('close_database'))
        self.file_menu.entryconfig(4, label=get_string('empty_database'))
        self.file_menu.entryconfig(6, label=get_string('exit'))

        self.menubar.entryconfig(self.menubar.index(self.lang_menu), label=get_string('language_menu'))

        self.menubar.entryconfig(self.menubar.index(self.help_menu), label=get_string('help_menu'))
        self.help_menu.entryconfig(0, label=get_string('documentation'))
        self.help_menu.entryconfig(1, label=get_string('sponsor_menu'))
        self.help_menu.entryconfig(self.help_menu.index('end'), label=get_string('about_menu'))

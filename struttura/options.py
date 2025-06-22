"""
Options/Settings dialog for the Movie Catalog application.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from lang.lang import get_string as tr
from pathlib import Path

# Get the application directory
APP_DIR = Path(__file__).parent.parent
SETTINGS_FILE = APP_DIR / 'settings.json'

# Default settings
DEFAULT_SETTINGS = {
    'appearance': {
        'theme': 'system',
        'language': 'en',
        'font_size': 10
    },
    'updates': {
        'check_on_startup': True,
        'channel': 'stable',
        'last_checked': None
    },
    'advanced': {
        'log_level': 'INFO',
        'log_location': os.path.join(os.path.expanduser('~'), '.movie_catalog', 'logs'),
        'enable_analytics': False
    },
    'window': {
        'width': 1024,
        'height': 768,
        'x': None,
        'y': None,
        'maximized': False
    }
}

class OptionsDialog(tk.Toplevel):
    """Options dialog for application settings."""
    
    def __init__(self, parent):
        """Initialize the options dialog."""
        super().__init__(parent)
        self.parent = parent
        self.settings_file = SETTINGS_FILE
        self.settings = {}
        
        # Crea la directory delle impostazioni se non esiste
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        
        self.title(f"{tr('options')} - {tr('app_title')}")
        self.geometry("600x400")
        
        # Make the window modal
        self.transient(parent)
        self.grab_set()
        
        # Load settings
        self._load_settings()
        
        # Create UI
        self._create_widgets()
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _load_settings(self):
        """Load settings from file or use defaults."""
        # Load settings from file if it exists
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                # Merge with default settings to ensure all keys exist
                self._merge_with_defaults()
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading settings: {e}")
                self.settings = DEFAULT_SETTINGS.copy()
        else:
            self.settings = DEFAULT_SETTINGS.copy()
    
    def _merge_with_defaults(self):
        """Ensure all default settings are present in the loaded settings."""
        for category, values in DEFAULT_SETTINGS.items():
            if category not in self.settings:
                self.settings[category] = values
            else:
                for key, value in values.items():
                    if key not in self.settings[category]:
                        self.settings[category][key] = value
    
    def save_settings(self):
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            return True
        except (IOError, TypeError) as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, category, key, default=None):
        """Get a specific setting value."""
        return self.settings.get(category, {}).get(key, default)
    
    def set_setting(self, category, key, value):
        """Set a specific setting value."""
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value
    
    def _create_widgets(self):
        """Create and arrange the UI widgets."""
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for different settings sections
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # General tab
        general_frame = ttk.Frame(notebook, padding=10)
        notebook.add(general_frame, text=tr('general'))
        
        # Appearance section
        ttk.Label(
            general_frame, 
            text=tr('appearance'), 
            font=('TkDefaultFont', 10, 'bold')
        ).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))
        
        # Theme selection
        ttk.Label(general_frame, text=f"{tr('theme')}:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.theme_var = tk.StringVar(value=self.get_setting('appearance', 'theme'))
        theme_combo = ttk.Combobox(
            general_frame, 
            textvariable=self.theme_var,
            values=['light', 'dark', 'system'],
            state='readonly',
            width=15
        )
        theme_combo.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Language selection
        ttk.Label(general_frame, text=f"{tr('language')}:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.lang_var = tk.StringVar(value=self.get_setting('appearance', 'language'))
        self.lang_combo = ttk.Combobox(
            general_frame, 
            textvariable=self.lang_var,
            values=[('English', 'en'), ('Italiano', 'it')],
            state='readonly',
            width=15
        )
        self.lang_combo.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # Font size
        ttk.Label(general_frame, text=f"{tr('font_size')}:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.font_size_var = tk.StringVar(value=str(self.get_setting('appearance', 'font_size')))
        ttk.Spinbox(
            general_frame,
            from_=8,
            to=24,
            textvariable=self.font_size_var,
            width=5
        ).grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        # Updates tab
        updates_frame = ttk.Frame(notebook, padding=10)
        notebook.add(updates_frame, text=tr('updates'))
        
        # Updates section
        ttk.Label(
            updates_frame, 
            text=tr('update_settings'), 
            font=('TkDefaultFont', 10, 'bold')
        ).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))
        
        # Check for updates on startup
        self.check_updates_var = tk.BooleanVar(value=self.get_setting('updates', 'check_on_startup'))
        ttk.Checkbutton(
            updates_frame,
            text=tr('check_updates_startup'),
            variable=self.check_updates_var
        ).grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        # Update channel
        ttk.Label(updates_frame, text=f"{tr('update_channel')}:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.channel_var = tk.StringVar(value=self.get_setting('updates', 'channel'))
        channel_combo = ttk.Combobox(
            updates_frame,
            textvariable=self.channel_var,
            values=[
                (tr('stable'), 'stable'),
                (tr('beta'), 'beta'),
                (tr('development'), 'dev')
            ],
            state='readonly',
            width=15
        )
        channel_combo.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # Last checked label
        last_checked = self.get_setting('updates', 'last_checked')
        last_checked_text = f"{tr('last_checked')}: {last_checked}" if last_checked else tr('never_checked')
        self.last_checked_var = tk.StringVar(value=last_checked_text)
        ttk.Label(
            updates_frame,
            textvariable=self.last_checked_var
        ).grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        # Check now button
        ttk.Button(
            updates_frame,
            text=tr('check_now'),
            command=self._check_for_updates
        ).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Advanced tab
        advanced_frame = ttk.Frame(notebook, padding=10)
        notebook.add(advanced_frame, text=tr('advanced'))
        
        # Logging section
        ttk.Label(
            advanced_frame, 
            text=tr('logging'), 
            font=('TkDefaultFont', 10, 'bold')
        ).grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 10))
        
        # Log level
        ttk.Label(advanced_frame, text=f"{tr('log_level')}:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.log_level_var = tk.StringVar(value=self.get_setting('advanced', 'log_level'))
        log_level_combo = ttk.Combobox(
            advanced_frame, 
            textvariable=self.log_level_var,
            values=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            state='readonly',
            width=15
        )
        log_level_combo.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Log file location
        ttk.Label(advanced_frame, text=f"{tr('log_location')}:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.log_location_var = tk.StringVar(value=self.get_setting('advanced', 'log_location'))
        ttk.Entry(
            advanced_frame, 
            textvariable=self.log_location_var,
            width=40
        ).grid(row=2, column=1, sticky='we', padx=5, pady=5)
        ttk.Button(
            advanced_frame,
            text=tr('browse'),
            command=self._browse_log_location
        ).grid(row=2, column=2, padx=5, pady=5)
        
        # Analytics
        self.analytics_var = tk.BooleanVar(value=self.get_setting('advanced', 'enable_analytics'))
        ttk.Checkbutton(
            advanced_frame,
            text=tr('enable_analytics'),
            variable=self.analytics_var
        ).grid(row=3, column=0, columnspan=3, sticky='w', padx=5, pady=5)
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Buttons
        ttk.Button(
            btn_frame,
            text=tr('apply'),
            command=self._apply_settings
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame,
            text=tr('cancel'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame,
            text=tr('ok'),
            command=self._save_and_close
        ).pack(side=tk.RIGHT, padx=5)
    
    def _browse_log_location(self):
        """Open a file dialog to select log file location."""
        log_dir = filedialog.askdirectory(
            title=tr('select_log_directory'),
            mustexist=True
        )
        if log_dir:
            self.log_location_var.set(log_dir)
    
    def _check_for_updates(self):
        """Check for updates now."""
        try:
            from struttura.updates import check_for_updates
            from struttura import __version__
            
            # Disable the button during check
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Button) and widget['text'] == tr('check_now'):
                    widget.config(state=tk.DISABLED)
            
            # Simulate update check (replace with actual implementation)
            self.after(1000, lambda: self._update_check_complete(True, "1.2.3"))
            
        except ImportError:
            messagebox.showerror(
                tr('error'),
                tr('update_module_not_found')
            )
    
    def _update_check_complete(self, updates_available, version=None):
        """Handle completion of update check."""
        # Re-enable the button
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Button) and widget['text'] == tr('check_now'):
                widget.config(state=tk.NORMAL)
        
        # Update last checked time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_checked_var.set(f"{tr('last_checked')}: {now}")
        
        # Show result
        if updates_available and version:
            messagebox.showinfo(
                tr('updates_available'),
                tr('new_version_available').format(version=version)
            )
        else:
            messagebox.showinfo(
                tr('no_updates'),
                tr('using_latest_version')
            )
    
    def _apply_settings(self):
        """Apply the current settings without closing the dialog."""
        try:
            # Appearance
            self.set_setting('appearance', 'theme', self.theme_var.get())
            self.set_setting('appearance', 'language', self.lang_var.get())
            self.set_setting('appearance', 'font_size', int(self.font_size_var.get()))
            
            # Updates
            self.set_setting('updates', 'check_on_startup', self.check_updates_var.get())
            self.set_setting('updates', 'channel', self.channel_var.get())
            
            # Advanced
            self.set_setting('advanced', 'log_level', self.log_level_var.get())
            self.set_setting('advanced', 'log_location', self.log_location_var.get())
            self.set_setting('advanced', 'enable_analytics', self.analytics_var.get())
            
            # Save to file
            if self.save_settings():
                messagebox.showinfo(
                    tr('settings_saved'),
                    tr('settings_saved_message')
                )
                return True
            else:
                messagebox.showerror(
                    tr('error'),
                    tr('error_saving_settings')
                )
                return False
                
        except Exception as e:
            messagebox.showerror(
                tr('error'),
                f"{tr('error_processing_settings')}: {str(e)}"
            )
            return False
    
    def _save_and_close(self):
        """Save settings and close the dialog."""
        if self._apply_settings():
            self.destroy()
            # Notify parent to apply settings
            if hasattr(self.parent, 'apply_settings'):
                self.parent.apply_settings()
    
    def get_settings(self):
        """Return the current settings."""
        return self.settings

# Helper function to load settings without UI
def load_settings(settings_file=None):
    """Load settings from file or return defaults."""
    if settings_file is None:
        settings_file = SETTINGS_FILE
    
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            # Merge with default settings to ensure all keys exist
            for category, values in DEFAULT_SETTINGS.items():
                if category not in settings:
                    settings[category] = values
                else:
                    for key, value in values.items():
                        if key not in settings[category]:
                            settings[category][key] = value
            return settings
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings: {e}")
    
    # Return defaults if file doesn't exist or there was an error
    return DEFAULT_SETTINGS.copy()

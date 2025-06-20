"""
Options/Settings dialog for the Movie Catalog application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from lang.lang import get_string as tr

class OptionsDialog(tk.Toplevel):
    """Options dialog for application settings."""
    
    def __init__(self, parent):
        """Initialize the options dialog."""
        super().__init__(parent)
        self.parent = parent
        self.title(f"{tr('options')} - {tr('app_title')}")
        self.geometry("600x400")
        
        # Make the window modal
        self.transient(parent)
        self.grab_set()
        
        # Create UI
        self._create_widgets()
        self._load_settings()
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
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
        self.theme_var = tk.StringVar()
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
        self.lang_var = tk.StringVar()
        lang_combo = ttk.Combobox(
            general_frame, 
            textvariable=self.lang_var,
            values=[('English', 'en'), ('Italiano', 'it')],
            state='readonly',
            width=15
        )
        lang_combo.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
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
        self.check_updates_var = tk.BooleanVar()
        ttk.Checkbutton(
            updates_frame,
            text=tr('check_updates_startup'),
            variable=self.check_updates_var
        ).grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        # Update channel
        ttk.Label(updates_frame, text=f"{tr('update_channel')}:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.channel_var = tk.StringVar()
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
        self.last_checked_var = tk.StringVar()
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
        ).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))
        
        # Log level
        ttk.Label(advanced_frame, text=f"{tr('log_level')}:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.log_level_var = tk.StringVar()
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
        self.log_location_var = tk.StringVar()
        ttk.Entry(
            advanced_frame, 
            textvariable=self.log_location_var,
            width=40,
            state='readonly'
        ).grid(row=2, column=1, sticky='we', padx=5, pady=5)
        ttk.Button(
            advanced_frame,
            text=tr('browse'),
            command=self._browse_log_location
        ).grid(row=2, column=2, padx=5, pady=5)
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Buttons
        ttk.Button(
            btn_frame,
            text=tr('save'),
            command=self._save_settings
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame,
            text=tr('cancel'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _browse_log_location(self):
        """Open a file dialog to select log file location."""
        from tkinter import filedialog
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
            
            # Force update check
            check_for_updates(self, __version__, force_check=True)
            
        except Exception as e:
            messagebox.showerror(
                tr('error'),
                f"{tr('error_checking_updates')}: {str(e)}",
                parent=self
            )
        finally:
            # Re-enable the button
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Button) and widget['text'] == tr('check_now'):
                    widget.config(state=tk.NORMAL)
    
    def _load_settings(self):
        """Load current settings into the dialog."""
        try:
            # TODO: Load actual settings from configuration
            self.theme_var.set('system')
            self.lang_var.set('en')
            self.check_updates_var.set(True)
            self.channel_var.set('stable')
            self.log_level_var.set('INFO')
            self.log_location_var.set('logs/movie_catalog.log')
            self.last_checked_var.set(f"{tr('last_checked')}: {tr('never')}")
        except Exception as e:
            messagebox.showerror(
                tr('error'),
                f"{tr('error_loading_settings')}: {str(e)}",
                parent=self
            )
    
    def _save_settings(self):
        """Save the settings and close the dialog."""
        try:
            # TODO: Save settings to configuration
            # Example:
            # config.set('updates.check_on_startup', self.check_updates_var.get())
            # config.set('updates.channel', self.channel_var.get())
            # config.save()
            
            # Update last checked time
            from datetime import datetime
            last_checked = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.last_checked_var.set(f"{tr('last_checked')}: {last_checked}")
            
            messagebox.showinfo(
                tr('success'),
                tr('settings_saved'),
                parent=self
            )
            self.destroy()
        except Exception as e:
            messagebox.showerror(
                tr('error'),
                f"{tr('error_saving_settings')}: {str(e)}",
                parent=self
            )

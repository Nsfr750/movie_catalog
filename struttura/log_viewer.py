"""
Log viewer for the Movie Catalog application.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
import os
from datetime import datetime
from struttura import logger
from lang.lang import get_string as tr

class LogViewer(tk.Toplevel):
    """A window for viewing application logs."""
    
    def __init__(self, parent):
        """Initialize the log viewer window."""
        super().__init__(parent)
        self.parent = parent
        self.title(f"{tr('log_viewer')} - {tr('app_title')}")
        self.geometry("900x600")
        
        # Configure window
        self.transient(parent)
        self.grab_set()
        
        # Create UI
        self._create_widgets()
        self._load_logs()
    
    def _create_widgets(self):
        """Create and arrange the UI widgets."""
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(
            controls_frame,
            text=tr('refresh'),
            command=self._load_logs
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear logs button
        clear_btn = ttk.Button(
            controls_frame,
            text=tr('clear_logs'),
            command=self._confirm_clear_logs
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Log level filter
        ttk.Label(controls_frame, text=f"{tr('log_level')}:").pack(side=tk.LEFT, padx=(20, 5))
        
        self.log_level = tk.StringVar(value="ALL")
        log_levels = ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        log_level_menu = ttk.OptionMenu(
            controls_frame,
            self.log_level,
            "ALL",
            *log_levels,
            command=lambda _: self._load_logs()
        )
        log_level_menu.pack(side=tk.LEFT, padx=5)
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=('Courier New', 10),
            bg='black',
            fg='white',
            insertbackground='white',
            selectbackground='#3465a4',
            selectforeground='white',
            undo=True,
            width=100,
            height=30
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add right-click context menu
        self._create_context_menu()
        
        # Configure tags for log levels
        self._configure_tags()
    
    def _create_context_menu(self):
        """Create the right-click context menu."""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(
            label=tr('copy'),
            command=self._copy_selected,
            accelerator="Ctrl+C"
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label=tr('select_all'),
            command=self._select_all,
            accelerator="Ctrl+A"
        )
        self.context_menu.add_command(
            label=tr('clear_display'),
            command=self._clear_display
        )
        
        # Bind right-click event
        self.log_text.bind("<Button-3>", self._show_context_menu)
        
        # Bind keyboard shortcuts
        self.log_text.bind("<Control-c>", lambda e: self._copy_selected())
        self.log_text.bind("<Control-a>", lambda e: self._select_all())
    
    def _show_context_menu(self, event):
        """Show the context menu at the cursor position."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def _copy_selected(self):
        """Copy selected text to clipboard."""
        try:
            selected = self.log_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(selected)
        except tk.TclError:
            pass  # No selection
    
    def _select_all(self):
        """Select all text in the log display."""
        self.log_text.tag_add(tk.SEL, "1.0", tk.END)
        self.log_text.mark_set(tk.INSERT, "1.0")
        self.log_text.see(tk.INSERT)
        return 'break'  # Prevent default behavior
    
    def _clear_display(self):
        """Clear the log display."""
        self.log_text.delete(1.0, tk.END)
    
    def _configure_tags(self):
        """Configure text tags for different log levels."""
        self.log_text.tag_configure('DEBUG', foreground='gray')
        self.log_text.tag_configure('INFO', foreground='white')
        self.log_text.tag_configure('WARNING', foreground='yellow')
        self.log_text.tag_configure('ERROR', foreground='orange')
        self.log_text.tag_configure('CRITICAL', foreground='red', font=('Courier New', 10, 'bold'))
    
    def _load_logs(self):
        """Load and display logs based on current filter."""
        log_file = Path("logs/movie_catalog.log")
        
        if not log_file.exists():
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"{tr('no_logs_found')}\n")
            return
        
        try:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            
            selected_level = self.log_level.get()
            
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if selected_level != "ALL" and not line.strip():
                        continue
                        
                    if selected_level == "ALL" or f" {selected_level} - " in line:
                        self._add_log_line(line)
            
            # Auto-scroll to the end
            self.log_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror(
                tr('error'),
                f"{tr('error_loading_logs')}: {str(e)}"
            )
        finally:
            self.log_text.config(state=tk.DISABLED)
    
    def _add_log_line(self, line):
        """Add a single log line with appropriate formatting."""
        # Determine log level for coloring
        log_level = 'INFO'  # Default
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            if f' {level} - ' in line:
                log_level = level
                break
        
        # Insert the line with the appropriate tag
        self.log_text.insert(tk.END, line, (log_level,))
    
    def _confirm_clear_logs(self):
        """Show confirmation dialog before clearing logs."""
        if messagebox.askyesno(
            tr('confirm'),
            tr('confirm_clear_logs'),
            parent=self
        ):
            self._clear_logs()
    
    def _clear_logs(self):
        """Clear all log files."""
        try:
            log_dir = Path("logs")
            for log_file in log_dir.glob("*.log*"):
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write("")
            
            # Reload to show empty logs
            self._load_logs()
            messagebox.showinfo(
                tr('success'),
                tr('logs_cleared'),
                parent=self
            )
        except Exception as e:
            messagebox.showerror(
                tr('error'),
                f"{tr('error_clearing_logs')}: {str(e)}",
                parent=self
            )

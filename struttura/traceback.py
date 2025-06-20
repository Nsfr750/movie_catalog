"""
Traceback utilities for the Movie Catalog application.
"""
import sys
import traceback
from typing import Optional, Type, Any
from . import logger

def format_exception(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: Optional[Any] = None
) -> str:
    """
    Format an exception with traceback information.
    
    Args:
        exc_type: The exception type
        exc_value: The exception value
        exc_traceback: The traceback object (optional)
        
    Returns:
        Formatted exception string with traceback
    """
    if exc_traceback is None:
        exc_traceback = sys.exc_info()[2]
    
    try:
        # Format the exception
        exc_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        formatted_traceback = "".join(exc_lines)
        
        # Add some context if available
        if hasattr(exc_value, '__context__') and exc_value.__context__ is not None:
            context = exc_value.__context__
            exc_lines = traceback.format_exception(
                type(context), context, context.__traceback__
            )
            formatted_traceback += "\nDuring handling of the above exception, another exception occurred:\n\n"
            formatted_traceback += "".join(exc_lines)
        
        return formatted_traceback
    except Exception as e:
        logger.logger.error(f"Error formatting exception: {str(e)}")
        return f"Error formatting exception: {str(e)}"

def log_unhandled_exception(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: Optional[Any] = None
) -> None:
    """
    Log an unhandled exception.
    
    Args:
        exc_type: The exception type
        exc_value: The exception value
        exc_traceback: The traceback object (optional)
    """
    if exc_type is KeyboardInterrupt:
        # Don't log keyboard interrupts
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    try:
        # Format the exception
        error_msg = format_exception(exc_type, exc_value, exc_traceback)
        
        # Log the error
        logger.logger.critical(
            "Unhandled exception\n%s",
            error_msg,
            exc_info=(exc_type, exc_value, exc_traceback)
        )
        
        # Also print to stderr for good measure
        print(error_msg, file=sys.stderr)
        
    except Exception as e:
        # If something goes wrong in the exception handler, log it
        logger.logger.error("Error in log_unhandled_exception: %s", str(e))
        # Fall back to default handler
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

def setup_exception_handling() -> None:
    """Set up global exception handling."""
    sys.excepthook = log_unhandled_exception

class ExceptionDialog:
    """A dialog to display detailed exception information."""
    
    def __init__(self, parent, title: str, message: str, exc_info: tuple):
        """
        Initialize the exception dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Error message
            exc_info: Exception info tuple (type, value, traceback)
        """
        self.parent = parent
        self.title = title
        self.message = message
        self.exc_info = exc_info
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the dialog UI."""
        import tkinter as tk
        from tkinter import ttk, scrolledtext
        
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("800x600")
        self.window.minsize(600, 400)
        
        # Make the window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Error message
        msg_frame = ttk.Frame(main_frame)
        msg_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            msg_frame,
            text=self.message,
            wraplength=700,
            foreground="red"
        ).pack(fill=tk.X)
        
        # Exception details in a notebook
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Traceback tab
        tb_frame = ttk.Frame(notebook, padding="5")
        notebook.add(tb_frame, text="Traceback")
        
        tb_text = scrolledtext.ScrolledText(
            tb_frame,
            wrap=tk.WORD,
            font=('Courier New', 10),
            bg='#2b2b2b',
            fg='#f8f8f8',
            insertbackground='white',
            selectbackground='#3465a4',
            selectforeground='white',
            undo=True,
            width=100,
            height=20
        )
        tb_text.pack(fill=tk.BOTH, expand=True)
        
        # Format and insert the traceback
        exc_type, exc_value, exc_tb = self.exc_info
        tb_text.insert(tk.END, format_exception(exc_type, exc_value, exc_tb))
        tb_text.config(state=tk.DISABLED)
        
        # Local variables tab (if we have a traceback)
        if exc_tb is not None:
            locals_frame = ttk.Frame(notebook, padding="5")
            notebook.add(locals_frame, text="Local Variables")
            
            locals_text = scrolledtext.ScrolledText(
                locals_frame,
                wrap=tk.WORD,
                font=('Courier New', 10),
                bg='#2b2b2b',
                fg='#f8f8f8',
                insertbackground='white',
                selectbackground='#3465a4',
                selectforeground='white',
                undo=True,
                width=100,
                height=20
            )
            locals_text.pack(fill=tk.BOTH, expand=True)
            
            # Try to get local variables from the traceback
            try:
                import pprint
                from types import TracebackType
                
                tb: TracebackType = exc_tb
                while tb.tb_next is not None:
                    tb = tb.tb_next
                
                if tb.tb_frame.f_locals:
                    locals_text.insert(
                        tk.END,
                        pprint.pformat(tb.tb_frame.f_locals, indent=2)
                    )
                else:
                    locals_text.insert(tk.END, "No local variables found.")
            except Exception as e:
                locals_text.insert(tk.END, f"Could not retrieve local variables: {str(e)}")
            
            locals_text.config(state=tk.DISABLED)
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Copy button
        def copy_to_clipboard():
            self.window.clipboard_clear()
            self.window.clipboard_append(tb_text.get(1.0, tk.END))
            
        ttk.Button(
            btn_frame,
            text="Copy to Clipboard",
            command=copy_to_clipboard
        ).pack(side=tk.LEFT, padx=5)
        
        # Close button
        ttk.Button(
            btn_frame,
            text="Close",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

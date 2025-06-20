# struttura/movie_details_dialog.py
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from PIL import Image, ImageTk
import io
import requests
from dataclasses import asdict

class MovieDetailsDialog(tk.Toplevel):
    def __init__(
        self,
        parent,
        title: str,
        year: Optional[int] = None,
        on_save: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        self.title(f"Movie Details: {title}")
        self.on_save = on_save
        self.metadata = None
        self.image_cache = {}
        
        # Main container
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search frame
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search TMDB:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        search_entry.bind('<Return>', lambda e: self.search_metadata())
        
        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_metadata
        ).pack(side=tk.LEFT)
        
        # Details frame
        self.details_frame = ttk.Frame(self.main_frame)
        self.details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Save",
            command=self.on_save_clicked
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side=tk.RIGHT)
        
        # Set initial focus
        search_entry.focus_set()
        
    def search_metadata(self):
        """Search for movie metadata from TMDB."""
        query = self.search_var.get().strip()
        if not query:
            return
            
        # TODO: Show loading state
        
        try:
            # Initialize TMDB client (you'll need to get an API key)
            from struttura.movie_metadata import TMDBClient
            client = TMDBClient(api_key="API_KEY")
            
            # Search for the movie
            self.metadata = client.get_metadata(query)
            
            if self.metadata:
                self.display_metadata()
            else:
                # Show "not found" message
                pass
                
        except Exception as e:
            # Show error message
            print(f"Error fetching metadata: {e}")
    
    def display_metadata(self):
        """Display the fetched movie metadata."""
        # Clear previous content
        for widget in self.details_frame.winfo_children():
            widget.destroy()
            
        if not self.metadata:
            ttk.Label(
                self.details_frame,
                text="No metadata found or error occurred.",
                style='Error.TLabel'
            ).pack(pady=20)
            return
            
        # Create main content frame with 2 columns
        content_frame = ttk.Frame(self.details_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Poster
        poster_frame = ttk.Frame(content_frame, width=200)
        poster_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        if self.metadata.poster_url:
            try:
                # Load and display poster image
                response = requests.get(self.metadata.poster_url, stream=True)
                response.raise_for_status()
                img_data = response.content
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((200, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Store reference to prevent garbage collection
                self.image_cache['poster'] = photo
                
                poster_label = ttk.Label(poster_frame, image=photo)
                poster_label.image = photo  # Keep a reference
                poster_label.pack()
                
            except Exception as e:
                print(f"Error loading poster: {e}")
                ttk.Label(
                    poster_frame,
                    text="No poster available",
                    style='Secondary.TLabel'
                ).pack()
        
        # Right column - Details
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Movie title and year
        ttk.Label(
            details_frame,
            text=f"{self.metadata.title} ({self.metadata.year})",
            style='Title.TLabel'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Director
        ttk.Label(
            details_frame,
            text=f"Director: {self.metadata.director}",
            style='Subtitle.TLabel'
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Rating and Runtime
        details_text = f"Rating: {self.metadata.rating}/10 • {self.metadata.runtime} min"
        ttk.Label(details_frame, text=details_text).pack(anchor=tk.W, pady=(0, 10))
        
        # Genres
        if self.metadata.genres:
            genres_text = ", ".join(self.metadata.genres)
            ttk.Label(
                details_frame,
                text=f"Genres: {genres_text}",
                wraplength=400
            ).pack(anchor=tk.W, pady=(0, 10))
        
        # Overview
        ttk.Label(
            details_frame,
            text="Overview:",
            style='Subtitle.TLabel'
        ).pack(anchor=tk.W, pady=(10, 5))
        
        ttk.Label(
            details_frame,
            text=self.metadata.overview,
            wraplength=500
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Cast
        if self.metadata.cast:
            ttk.Label(
                details_frame,
                text="Cast:",
                style='Subtitle.TLabel'
            ).pack(anchor=tk.W, pady=(10, 5))
            
            for actor in self.metadata.cast:
                ttk.Label(
                    details_frame,
                    text=f"• {actor['name']} as {actor['character']}",
                    wraplength=500
                ).pack(anchor=tk.W, pady=(0, 2))
    
    def on_save_clicked(self):
        """Handle save button click."""
        if self.on_save and self.metadata:
            self.on_save(asdict(self.metadata))
        self.destroy()
    
    def _show_loading(self, show=True):
        """Show or hide loading indicator."""
        if hasattr(self, '_loading_label'):
            self._loading_label.destroy()
            
        if show:
            self._loading_label = ttk.Label(
                self.main_frame,
                text="Loading...",
                style='Secondary.TLabel'
            )
            self._loading_label.pack(pady=10)
            self.update_idletasks()

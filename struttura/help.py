import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from lang.lang import get_string as tr
import sys
import os


# Help Class
class Help:
    def __init__(self, root):
        self.root = root

    def show(self):
        help_dialog = tk.Toplevel(self.root)
        help_dialog.title(tr('Help'))
        help_dialog.geometry('500x600') # larg X alt
        help_dialog.transient(self.root)
        help_dialog.grab_set()

        # Create a notebook for different help sections
        notebook = ttk.Notebook(help_dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Usage Tab
        usage_frame = ttk.Frame(notebook)
        notebook.add(usage_frame, text=tr('Usage'))
        
        usage_text = f'''
        {tr('movie_catalog_help')}
        
        {tr('basic_usage')}:
        - {tr('click_browse')}
        - {tr('click_scan')}
        - {tr('progress_shown')}
        - {tr('movies_displayed')}
        
        {tr('database_features')}:
        - {tr('auto_save_db')}
        - {tr('load_from_db')}
        - {tr('export_csv')}
        - {tr('db_config')}
        
        {tr('file_organization')}:
        - {tr('genre_directories')}
        - {tr('supported_formats')}
        - {tr('genre_extraction')}
        - {tr('name_extraction')}
        - {tr('progress_shown')}
        - {tr('status_updates')}
        
        {tr('additional_features')}:
        - {tr('help_dialog')}
        - {tr('about_dialog')}
        - {tr('sponsor_options')}
        - {tr('error_handling')}
        '''
        
        usage_label = ttk.Label(usage_frame, text=usage_text, justify='left')
        usage_label.pack(padx=5, pady=5)

        # Documentation Tab
        docs_frame = ttk.Frame(notebook)
        notebook.add(docs_frame, text=tr('Documentation'))
        
        docs_text = f'''
        {tr('documentation_links')}:
        - {tr('github_repo')}: https://github.com/Nsfr750/movie_catalog
        - {tr('project_docs')}: https://nsfr750.github.io/movie_catalog
        - {tr('issue_tracker')}: https://github.com/Nsfr750/movie_catalog/issues
        
        {tr('support')}:
        - {tr('github_issue')}
        - {tr('check_docs')}
        - {tr('visit_website')}
        - {tr('github_repo')}: https://github.com/Nsfr750/movie-catalog
        - {tr('user_guide')}: https://github.com/Nsfr750/movie-catalog/docs/readme.md
        - {tr('report_issues')}: https://github.com/Nsfr750/movie-catalog/issues
        '''
        
        docs_label = ttk.Label(docs_frame, text=docs_text, justify='left')
        docs_label.pack(padx=5, pady=5)

        # Support Tab
        support_frame = ttk.Frame(notebook)
        notebook.add(support_frame, text=tr('Support'))
        
        support_text = f'''
        {tr('support_options')}:
        - {tr('email')}: nsfr750@yandex.com
        - {tr('github_issues')}: https://github.com/Nsfr750/movie-catalog/issues
        - {tr('discord')}: https://discord.gg/BvvkUEP9
        '''
        
        support_label = ttk.Label(support_frame, text=support_text, justify='left')
        support_label.pack(padx=5, pady=5)

        # Add a close button
        close_btn = ttk.Button(help_dialog, text=tr('close'), command=help_dialog.destroy)
        close_btn.pack(pady=5)

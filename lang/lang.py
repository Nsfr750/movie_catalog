# -*- coding: utf-8 -*-

"""
This module handles the localization of the application.
"""

# English translations
en = {
    "app_title": "Movie Catalog",
    "file_menu": "File",
    "exit_menu": "Exit",
    "help_menu": "Help",
    "about_menu": "About",
    "button_ok": "OK",
    "button_cancel": "Cancel",
    "error": "Error",
    "db_config_failed": "Failed to configure database",
    "ready": "Ready",
    "db_not_initialized": "Database not initialized",
    "success": "Success",
    "movies_loaded": "Movies loaded from database",
    "load_movies_failed": "Failed to load movies",
    "select_directory": "Select Movie Directory",
    "browse": "Browse...",
    "actions": "Actions",
    "scan_movies": "Scan Movies",
    "export_csv": "Export to CSV",
    "load_from_db": "Load from DB",
    "genre": "Genre",
    "movie_name": "Movie Name",
    "path": "Path",
    "new_database": "New Database",
    "open_database": "Open Database",
    "close_database": "Close Database",
    "language_menu": "&Language",
    "sponsor_menu": "Sponsor",
    "db_created": "Database created successfully!",
    "db_create_failed": "Failed to create database",
    "db_connected": "Database connected successfully!",
    "db_connect_failed": "Failed to connect to database",
    "db_closed": "Database connection closed.",
    "warning": "Warning",
    "select_valid_directory": "Please select a valid directory.",
    "scanning": "Scanning...",
    "scan_complete": "Scan Complete",
    "scan_completed_message": "Movie scanning completed!",
    "export_to_csv": "Export to CSV",
    "data_exported": "Data exported to",
    "export_failed": "Failed to export data",
    "save_as_csv": "Save as CSV"
}

# Italian translations
it = {
    "app_title": "Movie Catalog",
    "file_menu": "File",
    "exit_menu": "Esci",
    "help_menu": "Aiuto",
    "about_menu": "Informazioni su",
    "button_ok": "OK",
    "button_cancel": "Annulla",
    "error": "Errore",
    "db_config_failed": "Impossibile configurare il database",
    "ready": "Pronto",
    "db_not_initialized": "Database non inizializzato",
    "success": "Successo",
    "movies_loaded": "Film caricati dal database",
    "load_movies_failed": "Impossibile caricare i film",
    "select_directory": "Seleziona la cartella dei film",
    "browse": "Sfoglia...",
    "actions": "Azioni",
    "scan_movies": "Scansiona film",
    "export_csv": "Esporta in CSV",
    "load_from_db": "Carica dal DB",
    "genre": "Genere",
    "movie_name": "Nome del film",
    "path": "Percorso",
    "new_database": "Nuovo database",
    "open_database": "Apri database",
    "close_database": "Chiudi database",
    "language_menu": "&Lingua",
    "sponsor_menu": "Sponsor",
    "db_created": "Database creato con successo!",
    "db_create_failed": "Impossibile creare il database",
    "db_connected": "Connessione al database riuscita!",
    "db_connect_failed": "Impossibile connettersi al database",
    "db_closed": "Connessione al database chiusa.",
    "warning": "Attenzione",
    "select_valid_directory": "Seleziona una directory valida.",
    "scanning": "Scansione in corso...",
    "scan_complete": "Scansione completata",
    "scan_completed_message": "La scansione dei film è terminata!",
    "export_to_csv": "Esporta in CSV",
    "data_exported": "Dati esportati in",
    "export_failed": "Impossibile esportare i dati",
    "save_as_csv": "Salva come CSV"
}

# Dictionary of available languages
LANGUAGES = {
    "en": en,
    "it": it,
}

# Variable to hold the current language dictionary
current_lang = en

def set_language(language_code):
    """Sets the application language."""
    global current_lang
    current_lang = LANGUAGES.get(language_code, en)

def get_string(key):
    """Gets a string in the current language."""
    return current_lang.get(key, key)

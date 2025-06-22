# -*- coding: utf-8 -*-

"""
Language module for Movie Catalog Application.

This module provides multi-language support for the Movie Catalog application.
It loads translations from JSON files in the lang directory.
"""

import os
import json

# Constants
DEFAULT_LANGUAGE = 'en'
LANGUAGES = {
    'en': 'English',
    'it': 'Italiano'
}

# Global variables
_current_language = DEFAULT_LANGUAGE
_current_dict = {}

def load_language(language_code):
    """
    Load language dictionary from JSON file.
    
    Args:
        language_code (str): The language code to load (e.g., 'en', 'it')
        
    Returns:
        dict: The loaded language dictionary, or empty dict if not found
    """
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the language file
        lang_file = os.path.join(current_dir, f"{language_code}.json")
        
        with open(lang_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load language file for '{language_code}': {e}")
        return {}

# Load default language on import
_current_dict = load_language(DEFAULT_LANGUAGE)

def set_language(language_code):
    """
    Set the current language.
    
    Args:
        language_code (str): The language code to set (e.g., 'en', 'it')
        
    Returns:
        bool: True if the language was set successfully, False otherwise
    """
    global _current_language, _current_dict
    
    if language_code in LANGUAGES:
        loaded_dict = load_language(language_code)
        if loaded_dict:  # Only update if loading was successful
            _current_dict = loaded_dict
            _current_language = language_code
            return True
    return False

def get_string(key):
    """
    Get a translated string for the given key.
    
    Args:
        key (str): The key for the string to translate
        
    Returns:
        str: The translated string, or the key if not found
    """
    return _current_dict.get(key, key)

def get_available_languages():
    """
    Get a list of available languages.
    
    Returns:
        dict: Dictionary mapping language codes to language names
    """
    return LANGUAGES.copy()

def get_current_language():
    """
    Get the current language code.
    
    Returns:
        str: The current language code
    """
    return _current_language

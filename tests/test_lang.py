import sys
import os

# Add the parent directory to the path so we can import the lang module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lang.lang import set_language, get_string, get_current_language, get_available_languages

def test_language_switching():
    print("Testing language switching...")
    
    # Test getting available languages
    print("\nAvailable languages:")
    for code, name in get_available_languages().items():
        print(f"  {code}: {name}")
    
    # Test English
    print("\nTesting English:")
    if set_language('en'):
        print(f"Current language: {get_current_language()}")
        print(f"App title: {get_string('app_title')}")
        print(f"File menu: {get_string('file_menu')}")
        print(f"Help menu: {get_string('help_menu')}")
    else:
        print("Failed to set English language")
    
    # Test Italian
    print("\nTesting Italian:")
    if set_language('it'):
        print(f"Current language: {get_current_language()}")
        print(f"App title: {get_string('app_title')}")
        print(f"File menu: {get_string('file_menu')}")
        print(f"Help menu: {get_string('help_menu')}")
    else:
        print("Failed to set Italian language")
    
    # Test invalid language
    print("\nTesting invalid language:")
    if not set_language('xx'):
        print("Correctly failed to set invalid language 'xx'")
    
    print("\nLanguage switching test completed!")

if __name__ == "__main__":
    test_language_switching()

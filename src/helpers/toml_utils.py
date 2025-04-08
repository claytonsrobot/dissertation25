"""
Title: toml-handler.py
Author: Clayton Bennett
Created: 22 February 2025
"""
from pathlib import Path
import os
import sys
# Use tomllib if the Python version is 3.11+. Otherwise use the toml package.
if sys.version_info >= (3, 11):
    import tomllib  # Built-in TOML module in Python 3.11+
else:
    import toml  # Third-party TOML package for older versions
    
def load_toml(filepath):
    if check_file(filepath):
        #with open(filepath,"r", encoding="utf-8") as f:
        with open(filepath,"rb", encoding="utf-8") as f:
            if sys.version_info >= (3,11):
                data = tomllib.load(f)
            else:
                data = toml.load(f)
            
            data = check_for_null(data)
        return data
    else:
        return False
    
def load_toml_tuple(filepath):
    data = load_toml(filepath)
    data_tuple = tuple(data.items())
    return data_tuple
    

def import_toml(filepath):
    """
    Simple function to import a TOML file.
    :param filepath: Path to the TOML file
    :return: Parsed TOML data as a dictionary
    Does not involve null checks.
    """
    try:
        # Open in binary mode for Python 3.11+; no encoding argument needed
        with open(filepath, "rb" if sys.version_info >= (3, 11) else "r", encoding=None if sys.version_info >= (3, 11) else "utf-8") as file:
            if sys.version_info >= (3, 11):
                return tomllib.load(file)  # Parse using tomllib
            else:
                return toml.load(file)  # Parse using toml
    except Exception as e:
        print(f"Error loading TOML file: {e}")
        return {}



def check_for_null(data):
    # Check if the data is a nested dictionary or flat
    if all(isinstance(value, dict) for value in data.values()):
        # If the data has section headers (nested structure)
        for section_key, section in data.items():
            for key, value in section.items():
                # If the value is a string and equals "null", replace it with None
                if isinstance(value, str) and value.lower() == "null":
                    section[key] = None
                    data[section_key] = section
    else:
        # If the data is flat (no section headers)
        for key, value in data.items():
            # If the value is a string and equals "null", replace it with None
            if isinstance(value, str) and value.lower() == "null":
                data[key] = None

    return data


def check_file(filepath):
    if not(os.path.isfile(filepath)):
        print(f"\nThe file does not exist: {filepath}")
        # Raise RuntimeError("Stopping execution")
        raise SystemExit
    else:
        # The file exists
        return True


if "__main__" == __name__:
   filepath = r"C:\\stuff\\"
   filepath = Path(os.path.normpath(filepath))
   t = load_toml(filepath)
   print(t)

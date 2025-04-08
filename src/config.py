import platform
import toml

import src.toml_utils

from pprint import pprint

from src.directories import Directories
class Config:
    def __init__(self):
        pass
    def load_config(self):
        pass
    def load_config_from_default(self):
        pass
    def load_config_from_project(self):
        pass


def define_and_load_default_config_input(self):
    "config_input.define_and_load_default_config_input()"
    # Load the config file
    raw_loaded_config = toml.load(Directories.get_config_entry())
    # Dynamically map the parsed config values to loaded_config
    self.loaded_config = {key: self.clean_imported_numerics(value) 
                          for key, value in raw_loaded_config.get("config", {}).items()}
    # Print and return the results
    #pprint(f"loaded_config = {self.loaded_config}")
    return self.loaded_config

def expressions(self):
    """math and dynamic expresions"""
    #print("os.getlogin() =",os.getlogin())
    #print("operator =",operator)
    #print("location =",location)
    #today = date.today()
    #datestring = today.strftime("%b-%d-%Y")
    #inchonvert = (((math.pi*(0.764))*31.4136)/359) # converts displacement to inches, wheel diameter = 31.4136
    "today" = "date.today()"

import subprocess
import os
import sys
import platform

# Ensure the root directory is part of sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.helpers.toml_utils import import_toml

# Path to the configuration file
CONFIG_FILE = os.path.join(script_dir, "update_desktop_ini_config.toml")

def run_powershell_script():
    # Load the configuration file
    config = import_toml(CONFIG_FILE)

    # Retrieve verbosity and relative_ico_path settings from the TOML file
    verbose = config["config"].get("verbose", False)
    relative_ico_path = config["config"].get("relative_ico_path", "\\media\\media-ico\\")
    
    # Define the path to the PowerShell script
    powershell_script = os.path.join(script_dir, "update_desktop_ini.ps1")

    # Verify the PowerShell script exists
    if not os.path.isfile(powershell_script):
        print(f"Error: PowerShell script not found at {powershell_script}")
        return

    try:
        # Pass configuration values to the PowerShell script
        verbosity_flag = "-Verbose" if verbose else "-Silent"
        #subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", powershell_script, verbosity_flag, f"-RelativeIcoPathTemplate:{relative_ico_path}"], check=True)
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", powershell_script, verbosity_flag, f"-RelativeIcoPath:{relative_ico_path}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the PowerShell script: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

def run_bash_script():
    # Load the configuration file
    config = import_toml(CONFIG_FILE)

    # Retrieve verbosity and relative_ico_path settings from the TOML file
    verbose = config["config"].get("verbose", False)
    relative_ico_path = config["config"].get("relative_ico_path", "{library}/media/media-ico/{icon_filename}")

    # Define the path to the Bash script
    bash_script = os.path.join(script_dir, "update_desktop_ini.sh")

    # Verify the Bash script exists
    if not os.path.isfile(bash_script):
        print(f"Error: Bash script not found at {bash_script}")
        return

    # Determine the verbosity flag
    verbosity_flag = "-Verbose" if verbose else "-Silent"

    # Determine the current operating system
    current_os = platform.system()
    if current_os != "Linux" and current_os != "Darwin":  # Darwin refers to macOS
        print(f"Error: Bash script is not supported on {current_os}")
        return

    try:
        # Pass configuration values to the Bash script
        subprocess.run(["bash", bash_script, verbosity_flag, f"--relative_ico_path={relative_ico_path}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Bash script: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    current_os = platform.system()

    if current_os == "Windows":
        run_powershell_script()
    elif current_os in ["Linux", "Darwin"]:  # Darwin is macOS
        run_bash_script()
    else:
        print(f"Error: Unsupported operating system: {current_os}")
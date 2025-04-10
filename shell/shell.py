'''
Title: CLI.py
Created: 21 May 2024
Author: Clayton Bennett

Purpose: 
Drive Pavlov from the command line. Choose options using command inputs and by editing json configuration files.
It might be good to have one config file driving the others?

Resources: 
https://medium.com/@noransaber685/simple-guide-to-creating-a-command-line-interface-cli-in-python-c2de7b8f5e05
'''

import cmd2
import os
import pprint
#from src import main
from src.hidden_prints import HiddenPrints
import src.pavlovmain
import time
from datetime import datetime
#import subprocess
#from sparklines import sparklines
#import gui_customtk_basic
from src.filemanagement import DirectoryControl
from src import filemanagement as fm
import src.environment
#import copy
import importlib
import ast
import operator
import readline # for adding history to self.history when loading the history file
import sys
#print(sys.path)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests import Test
from src.helpers import toml_utils

from src.directories import Directories
try:
    import psutil # overkill
except:
    pass

from src.datapoint import DataPoint

class HistoryEntry:
    """Custom history item to store and display commands properly."""
    def __init__(self, command: str):
        self.command = command.strip()  # Ensure no trailing or leading whitespace

    def pr(self, idx: int, script: bool = False, expanded: bool = False, verbose: bool = False) -> str:
        """Format history for printing, ensuring clean and consistent output."""
        return f"{idx}: {self.command}"

    def __str__(self):
        "return self.command"
        return f"{'-'}: {self.command}"


    
class PalovianCLI(cmd2.Cmd):

    scene_object = None
    style_object = None
    config_input_object = None
    user_input_object = None
    export_control_object = None
    pointcloud_bool = None
    createFBX_object = None
    export_object = None
    verbose = False

    project_active = None
    last_export_path = None
    all_export_paths = []

    name = f"Dissertation25 Command Line Interface"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Determine the path to the startup script
        startup_script_path = os.path.join("startup", "shell_startup.txt") # "relative path"
    
        self.add_settable(cmd2.Settable('DataPoint', object, 'The DataPoint class, imported in main and accessible in the shell.', DataPoint))
        
        # Check if the file exists before setting it
        if os.path.exists(startup_script_path):
            self.startup_script = startup_script_path
            print(f"Startup script set to: {self.startup_script}")
        else:
            self.startup_script = None  # Gracefully handle missing file
            print("No startup script found. Proceeding without one.")
        
        # Optional: Add your own intro message # Set above in class variables.
        # self.intro = "Welcome to PavlovShell. Type 'help' to get started."

        self.vars = {}
        self.modules = {}
        self.context = {'self': self,
                        'pprint': pprint.pprint,
                        'list': list,
                        'str': str,
                        'int': int,
                        'float': float,
                        'dict': dict,
                        'dir': dir,
                        'set': set,
                        'tuple': tuple,
                        'len': len,
                        'sum': sum,
                        'min': min,
                        'max': max,
                        'sorted': sorted,
                        'type': type,
                        'range': range,
                        'enumerate': enumerate,
                        'zip': zip,
                        'map': map,
                        'filter': filter,
                        'any': any,
                        'all': all,
                        'abs': abs,
                        'round': round,
                        'repr': repr,}
        self.debug = True  # Set the default debug value to True
        
        # Set startup script - if the file does not exist, there will be problems
        self.startup_script = os.path.join(os.path.dirname(__file__), "startup.txt")

        # Store command history
        history_dir = os.path.join(os.path.dirname(__file__), 'history-shell')
        os.makedirs(history_dir, exist_ok=True)  # Ensure the directory exists
        self.persistent_history_file = os.path.join(history_dir, 'shell_history.txt')

        # Auto-load history from the file if it exists
        if os.path.exists(self.persistent_history_file):
            self._load_history()

    def get_version():
        # for later on storing automatically, not worth the squeeze rn
        version = "Version: 2025-03March-29" # manually updated
        return version
    version = get_version()

    import cmd2


    def do_python(self, arg: str):
        """Execute Python commands interactively."""
        try:
            # Evaluate expressions (e.g., `2 + 2`) and print the result
            result = eval(arg, globals(), locals())
            self.poutput(f"Result: {result}")
        except Exception:
            try:
                # Execute statements (e.g., `x = 5`) without returning a result
                exec(arg, globals(), locals())
                self.poutput("Executed successfully.")
            except Exception as e:
                self.perror(f"Error: {e}")

    def help_python(self):
        """Display help for the Python command."""
        self.poutput("Run Python commands interactively. Example usage:")
        self.poutput("  python 2 + 2")
        self.poutput("  python x = 5")

    
    @classmethod
    def initialize_scene_object(cls):
        cls.scene_object = None
    @classmethod
    def link_initial_project_directory(cls):
        #cls.project_active = None
        Directories.set_project_dir(Directories.get_src_dir()+r"/projects/sample/")
        print(f"project_active = {Directories.get_project_dir()}")
        # dynamic, points to default-project.json file
        #cls.set_project_active(cls.get_startup_project("./projects/default-project.json")) # pull from config file
        Directories.initialize_startup_project() # pull from config file
    
    @classmethod
    def set_project_active(cls,project_dir):
        Directories.set_project_dir(project_dir)
        print(f"Directories.set_project_dir() = {Directories.get_project_dir()}")
    
    @classmethod
    def get_project_active(cls):
        return Directories.get_project_dir()

    def _load_history(self):
        """Load commands from the persistent history file at startup."""
        try:
            if os.path.exists(self.persistent_history_file):
                with open(self.persistent_history_file, 'r', encoding='utf-8') as history_file:
                    for line in history_file:
                        command = line.strip()
                        if command:
                            self.history.append(HistoryEntry(command))  
                            readline.add_history(command)
                print(f"Loaded {len(self.history)} commands from history.")
            else:
                print("No history file found, starting with an empty history.")
        except Exception as e:
            self.perror(f"Error loading history: {e}")

    
    def postcmd(self, stop, statement):
        """Called after every command to append it to the history file."""
        try:
            full_command = statement.raw.strip()
            if full_command:
                with open(self.persistent_history_file, 'a', encoding='utf-8') as history_file:
                    history_file.write(full_command + '\n')

                self.history.append(HistoryEntry(full_command))  # Store properly
            else:
                print("Skipped saving empty or invalid command.")
        except Exception as e:
            self.perror(f"Error saving command to history: {e}")
        return stop
    


    def do_debug_history(self, args):
        """Debugging command to display raw history entries with hidden characters."""
        for i, item in enumerate(self.history, start=1):
            self.poutput(repr(str(item)))  # Use string representation to ensure compatibility

    


    def run(self):
        #self.scene_object = None
        self.initialize_scene_object()
        self.link_initial_project_directory()
        Directories.initialize_startup_project()
        self.cmdloop()

    def do_status(self,line):
        "Get a rough idea of what the program has done so far."
        print(f"""\
        Exist:
        scene_object: {self.scene_object != None} :: 1
        style_object: {self.style_object != None} :: 1
        config_input_object: {self.config_input_object != None} :: 2
        user_input_object: {self.user_input_object != None} :: 2
        export_control_object: {self.export_control_object != None} :: 4
        pointcloud_bool: {self.pointcloud_bool != None} :: 5
        createFBX_object: {self.createFBX_object != None} :: 6
        """)


    def do_h(self,line):
        """
        Abbreviation for help.
        Example: h
        """
        self.do_help(line)

    def do_i(self,line):
        """
        Abbreviation for instructions.
        Example: i
        """
        self.do_instructions(line)
        
    def do_instructions(self,line):
        """
        run 'instructons' or 'i' to see instructions. 
        i
        """
        instructions = "Talk to Clayton."
        print(instructions)

    def do_where(self,line):
        "Print working directory location. This is where import and export files are managed." 
        try:

            print(f"Working directory: {Directories.get_program_dir()}")
            
        except Exception as e: 
            print("Scene not yet created. Run (1) make scene.")
        dev_location = "Memphis, Tennessee, 38104"
        print(dev_location)

    def do_when(self,line):
        """
        Print unix time, which represent the time when the scene was generation, via make scene. 
        """
        try:
            time_start = str(datetime.fromtimestamp(float(self.scene_object.unix_start)))
            #print(f"self.scene_object.unix_start = {self.scene_object.unix_start}")
            print(f"Unix time at scene creation: {self.scene_object.unix_start}")
            print(f"Date time at scene creation: {time_start}")
            

            #datetime.fromtimestamp(float(line))
            
        except Exception as e: 
            print("Scene not yet created. Run (1) make scene.")
        print(f"Date time now: {str(datetime.fromtimestamp(float(int(time.time()))))}")


    def do_test(self,line):
        "See CPU frequency."
        print(f"Test = {Test}")
        self.poutput("Test command executed successfully!")
        try:
            cpu_freq = psutil.cpu_freq()
            print("Current CPU Frequency:", round(cpu_freq.current),"hz, or so.") 
        except:
            pass

    def do_test_command_execution(self,line):
        """Programmatically run the 'test' command."""
        try:
            self.onecmd_plus_hooks("test")
        except Exception as e:
            print(f"Error executing 'test': {e}")

    def do_runall(self, arg):
        """Run a series of predefined commands."""
        commands = ["1", "2","3a","3b","4","5","6"]
        for cmd in commands:
            self.poutput(f"Running: {cmd}")
            self.onecmd_plus_hooks(cmd)

    def do_why(self,line):
        "Why?"
        why = "Dissertations are hard." 
        print(f"{why}")

    def do_how(self,line):
        "Prints instructions"
        self.do_instructions(None)

    def do_what(self,line):
        "What?"
        self.pretty_title(None)
    def do_v(self,line):
        "Abbreviation for version"
        self.do_version(None)
    def do_version(self,line):
        "See version."
        print(self.name)
        print(self.version)
        
    def do_about(self,line):
        "A foolish consistency is the hobgoblin of little minds."
        self.pretty_title(None)
        self.do_version(None)

    def do_futurework(self,line):
        "See futurework."
        fw = """
        Task1, task2, task 3.
        Three weeks to glory.
        """
        print(fw)

    def do_1(self,line):
        "make scene"
        self.make_scene(None)
    def do_2(self,line):
        "make config"
        self.makeconfig(None)
    def do_3(self,line):
        "skipinterface"
        self.do_skipinterface(None)
    def do_4(self,line):
        "import data, or, make data"
        self.import_data(None)
    def do_5(self,line):
        "make pointcloud, or, build_pointcoud"
        self.build_pointcloud(None)
    def do_6(self,line):
        "export or make export"
        self.do_export("fbx")

    def do_main(self,line):
        "main will run Pavlov with current config_input and config_settings values"
        #print('Warning: main should be converted to a class - now it runs on import')
        print('Running Pavlov....')
        print('Have fun, and may the odds be ever in your favor.')
        #global scene_object
        self.scene_object, self.hierarchy_object, self.createFBX_object = src.pavlovmain.main()
        #self.hierarchy_object = copy.deepcopy(self.scene_object.hierarchy_object)
        self.record_export_path()

        #self.scene_object = scene_object

        #self.curve_object = self.hierarchy_object.dict_curve_objects_all[list(self.hierarchy_object.dict_curve_objects_all.keys())[0]]
        #return scene_object
    
    def do_wipe(self,line):
        """
        Resets the session. Arguments are not accepted. 
        Example: wipe
        """
        if line == "":
            self.scene_object,self.style_object,self.hierarchy_object = None,None,None
            self.config_input_object,self.user_input_object = None,None
            self.export_control_object = None
            self.pointcloud_bool = None
            self.createFBX_object = None
            self.exportPNG_object = None
            self.do_status(None)
        else:
            msg=\
        """
        wipe does not accept arguments.
        wipe is meant to reset the session. 
        """
            print(msg)      

    def make_scene(self,line):
        "Instead of running main.main(), independantly make the scene."
        #global scene_object
        request = None
        scene_object,style_object,hierarchy_object = src.pavlovmain.set_up(request)
        self.scene_object,self.style_object,self.hierarchy_object = scene_object,style_object,hierarchy_object
        #scene_object = self.scene_object
        print('Built: scene, style, hierarchy')
        print("Hint: Next: (2) make config")


    def makeconfig(self,line):
        "Independantly generate config_input_object & user_input_object"
        try:
            self.config_input_object,self.user_input_object = \
                src.pavlovmain.get_configuration(self.scene_object,
                                    self.style_object)
            print("make config, done")
        except Exception as e:
            # if user did not make scene first, that's okay, do it automatially
            self.make_scene(None)
            self.makeconfig(None)
        print("Hint: Next: (3) skipinterface")


    def do_prep(self,line):
        "Run (1) make scene and (2) make config. Hide print."
        with HiddenPrints():
            self.make_scene(None)
            self.makeconfig(None)

    def do_rage(self,like):
        "Suggestions"
        print("I suggest you take a walk and do some breathing exercises.")

    def do_skipinterface(self,line):
        "Skip interface (3), use direct json file. Rather than editing defaults with a GUI."
        #try:
        self.user_input_object.pull_config_input_object(self.config_input_object)
        if self.config_input_object.grouping_algorithm == "group-by-text":
            self.build_grouping(None) # jammed in here for now - need to process when a gui is used as well
        
        print("Hint: Next: (4) make data, or, import data ")
        #except Exception as e:
        #    print("See instructions for necessary steps.")
        
    def do_no(self,line):
        "(3) skipinterface, hide print"
        with HiddenPrints():
            self.do_skipinterface(None)
        
    def do_go(self,line):
        "Run (4) import data , (5) make pointcloud, and (6) make export. Hide print."

        try:
            print("Generating model...")
            with HiddenPrints():
                self.import_data(None)
                self.build_pointcloud(None)
                self.export_model(None)
            print("Model exported :)")
        except Exception as e:
            print("Export failure.")
            print("See instructions for necessary steps.")

    def import_data(self,line):
        "Independantly import data (4). Generates export_control_object. Requires scene_object, style_object, and user_input_object to already exist."
        
        #try:
        print(f"\nself.scene_object = {self.scene_object}")
        self.export_control_object = src.pavlovmain.import_data(self.scene_object,
                                                self.style_object,
                                                self.user_input_object,
                                                self.hierarchy_object)
        print(f"\nself.scene_object = {self.scene_object}")
        print("Hint: Next: (5) make pointcloud")
        #except Exception as e:
        #    print("If the import fails for pyinstaller, ensure that the import plugin is registered in style.py")
        #    print("Failed to import data. See instructions for necessary steps.")
        

    def build_grouping(self,line):
        # jam in do_3(None), skipinterface for now
        src.pavlovmain.build_grouping(self.hierarchy_object,self.user_input_object,loaded_grouping = self.config_input_object.loaded_grouping)

    def build_pointcloud(self,line):
        "Independantly build the point cloud"  
        #try:
        src.pavlovmain.build_point_cloud(self.scene_object,
                            self.style_object,
                            self.user_input_object,
                            self.hierarchy_object)
        print(f'subprocesses:\n\
                .construct_scene_heirarchy\n\
                .build_ticks\n\
                .build_texts\n\
                .layout_spatial\n\
                .build_fences\n\
                ')
        
        self.pointcloud_bool = True
        print("Hint: Next: (6) make export")
        #except Exception as e:
        #    print("Failed to build pointcloud.")
        #    pass

    
    def do_export(self,line):
        """
        Generate export. 
        Examples: 
            export fbx
            export fbx -glb
            export plot
            export plot -pdf
            export plot -png 
            export plot -svg
            export blend

        plot option defaults to pdf
        """ 
        #try:
        if True:
            if "fbx" in line:
                self.createFBX_object = self.export_model(None)
                self.record_export_path()
            elif "plot" in line:
                print("createPlot.py Under constructions") 
            else:
                print("Hint: help export")
            print("Hint: open --last, or, o -l") #
        #except Exception as e:
        #    print("Export failure. Model not yet fully prepared.")
        #    pass

    def record_export_path(self):
        self.last_export_path = self.scene_object.filepath
        self.all_export_paths.append(self.last_export_path)
        print(f"self.all_export_paths = {self.all_export_paths}")
    def export_model(self,line):
        "Independantly generate export" 
    
        self.createFBX_object = src.pavlovmain.generate_export(self.scene_object,
                            self.style_object,
                            self.user_input_object)
        return self.createFBX_object
        #except Exception as e:
        #    print("See instructions for necessary steps.")
    ''' End main. element access'''
    
    config_parser = cmd2.Cmd2ArgumentParser()
    config_parser.add_argument('-l','--list',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. This will not include project diretories saved elsewhere, until some future date when a registration file will track those recent locations.')
    config_parser.add_argument('-le','--listexternal',nargs = "?", default=False, const=True, help='see project directories in the external-project-register.json file') 
    config_parser.add_argument('-t','--tree',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. ')
    config_parser.add_argument('-n','--new', nargs = "?",const="config_"+str(int(time.time())), default=False,help='Create new project directory, and make it the active directory.')
    config_parser.add_argument('-s','--sample', nargs = "?",const="sample-config_"+str(int(time.time())), default=False,help='Generate a sample proect directory, complete with sample files.')
    #config_parser.add_argument('-d','--destroy',nargs = "?", default=False, const=True, help='User is able to destroy existing project directory, when th ')
    config_parser.add_argument('-o','--open',help='Access an existing project directory.')
    config_parser.add_argument('-c','--current',nargs = "?",default=False, const=True,help='See current project.')
    config_parser.add_argument('-cc','--copy',nargs = "?",default=False, const=True,help='Copy current project. New name is hardcoded.')
    @cmd2.with_argparser(config_parser)
    def do_config(self,line):
        "inspect and change values from config_input.json"

    groupmap_parser = cmd2.Cmd2ArgumentParser()
    groupmap_parser.add_argument('-l','--list',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. This will not include project diretories saved elsewhere, until some future date when a registration file will track those recent locations.')
    groupmap_parser.add_argument('-t','--tree',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. ')
    groupmap_parser.add_argument('-n','--new', nargs = "?",const="groupmap_"+str(int(time.time())), default=False,help='Create new project directory, and make it the active directory.')
    groupmap_parser.add_argument('-s','--sample', nargs = "?",const="sample-config_"+str(int(time.time())), default=False,help='Generate a sample proect directory, complete with sample files.')
    #groupmap_parser.add_argument('-d','--destroy',nargs = "?", default=False, const=True, help='User is able to destroy existing project directory, when th ')
    groupmap_parser.add_argument('-o','--open',help='Access an existing project directory.')
    groupmap_parser.add_argument('-c','--current',nargs = "?",default=False, const=True,help='See current project.') 
    groupmap_parser.add_argument('-cc','--copy',nargs = "?",default=False, const=True,help='Copy current project. New name is hardcoded.')
    @cmd2.with_argparser(groupmap_parser)
    def do_groupmap(self,line):
        "inspect and change values from config_input.json"
        

    def do_exit(self,line):
        "Same as quit"
        true = self.do_quit(None)
        return true
        
    def do_quit(self,line):
        "Quit the CLI."
        return True # returning true quits the program
    
    def do_documentation(self,line):
        "See README.md."
        #return False
        print("Future work.")

    def do_license(self,line):
        "See the license. BSD 3-clause."
        bsd3 = """
        Copyright 2025 George Clayton Bennett

        Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

        1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

        3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        """
        print(bsd3)

    def do_copyright(self,line):
        "See copyright information."
        cr = """\
        Copyright 2025 George Clayton Bennett
        """
        
        print(cr)

    def do_credits(self,line):
        "see credits"
        credit =\
        """
        Clayton Bennett, 2025
        Pavlov Software & Services LLC, incorportated 2023.
        """
        self.pretty_title(None)
        print(credit)
    
    edit_parser = cmd2.Cmd2ArgumentParser()
    edit_parser.add_argument("-c","--config",help ="")
    @cmd2.with_argparser(edit_parser)
    def do_edit(self,args):
        "edit the user_input_object. Once you do this, you must run 4,5,6 again."

        if args.config is not None:
            print(f"args.config = {args.config}")
            key = args.config.split("=")[0]
            print(f"key = {key}")
            new_value = args.config.split("=")[1]
            print(f"new_value = {new_value}")
            if key in list(self.user_input_object.__dict__.keys()):
                self.user_input_object.__dict__[key] =  new_value

    def do_o(self,line):
        "open, abbreviated"
        self.do_open(line)
    open_parser = cmd2.Cmd2ArgumentParser()
    open_parser.add_argument('-f','--filepath',help='open file')
    open_parser.add_argument("-a","--allnew", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-l","--last", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-c","--config", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-e","--entry", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-b","--browser", nargs = "?", const=Directories.get_program_dir(), default=False, help ="")
    open_parser.add_argument("-g","--guide", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-m","--groupmap", nargs = "?", default=False, const=True, help ="")
    open_parser.add_argument("-p","--project", nargs = "?", default=False, const=True, help ="")

    @cmd2.with_argparser(open_parser)
    def do_open(self,args):
        """
        Open files with the system's default app.
        Include the file extension. 
        Provide the entire path or the filename in the current directory.

        If you are trying to open an FBX file, ensure CAD Assistant is installed.
        Hint: viewer

        If you do not like to default program that it opening your file, change it on your system using: Choose defaults by file type. 

        Examples:
            open C:\\user\\Documents\\pavlov_test.fbx
            open pavlov_awesome.fbx
            open pavlov_hooray.glb
            open exports\\pavlov_stellar.glb

        """
        #print(args.__dict__)
        if args.last is True:
            print(f"args.last = {args.last}")
            fm.openfile(self.last_export_path)

        elif args.filepath is not None:
            fm.openfile(args.filepath)

        elif args.allnew is True:
            if len(self.all_export_paths) ==0:
                print("No export files have yet been generated.")
                pass
            else:
                for filepath in self.all_export_paths:
                    fm.openfile(filepath)

        elif args.config is True:
            fm.openfile(self.config_input_object.config_input_path)

        elif args.entry is True:
            fm.openfilegui(self.config_input_object.config_entry_filepath)

        elif args.browser is not None and args.browser is not False:
            #print(f"args.browser = {args.browser}")
            #fm.opendir(self.config_input_object.script_dir)
            fm.opendir(args.browser)

        elif args.project is True:
            #print(f"args.browser = {args.browser}")
            #fm.opendir(self.config_input_object.script_dir)
            fm.opendir(Directories.get_project_dir())

        # style guide pdf, for what input can be used in the cofiguration files, and the expected keys
        elif args.guide is True:
            fm.openfile(self.config_input_object.config_guide_filepath)

        elif args.groupmap is True:
            fm.openfile(self.config_input_object.groupmap_filepath) # shouldP

        else:
            self.do_help("open")


    def pretty_title(self,line):
        print(self.pyfiglet_title)
        
    def do_unix2time(self,line):
        """
        See unix time as datetime
        Output: YYY-MM-DD HH:MM:SS
        Decimal places in a unix time value represent partial seconds, base 10, with direct correlation.

        Examples:
            unix2time 1734202184.912056
            unix2time 1734202184
        """        
        try:
            datetime_object = datetime.fromtimestamp(float(line))
            print(datetime_object)
        except Exception as e:
            self.do_help("unix2time")

    
    project_parser = cmd2.Cmd2ArgumentParser()
    project_parser.add_argument('-l','--list',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. This will not include project diretories saved elsewhere, until some future date when a registration file will track those recent locations.')
    project_parser.add_argument('-le','--listexternal',nargs = "?", default=False, const=True, help='see project directories in the external-project-register.json file') 
    project_parser.add_argument('-t','--tree',nargs = "?", default=False, const=True, help='See all project directories that are in the Pavlov program location. ')
    project_parser.add_argument('-n','--new', nargs = "?",const="project_"+str(int(time.time())), default=False,help='Create new project directory, and make it the active directory.')
    project_parser.add_argument('-s','--sample', nargs = "?",const="sample-project_"+str(int(time.time())), default=False,help='Generate a sample proect directory, complete with sample files.')
    project_parser.add_argument('-d','--destroy',nargs = "?", default=False, const=True, help='User is able to destroy existing project directory, when th ')
    project_parser.add_argument('-o','--open',help='Access an existing project directory.')
    project_parser.add_argument('-c','--current',nargs = "?",default=False, const=True,help='See current project.')
    project_parser.add_argument('-cc','--copy',nargs = "?",default=False, const=True,help='Copy current project. New name is hardcoded.')
    @cmd2.with_argparser(project_parser)
    def do_project(self,args):
        "Manage project directories"
        #print(f"args.sample = {args.sample}")
        #print(f"args.new = {args.new}")
        if args.tree is True:
            fm.tree("./projects/")

        elif args.list is True:
            #pprint.pprint(DirectoryControl.walk(args.list))
            pprint.pprint(DirectoryControl.walk(Directories.get_program_dir()+"/projects/"))
        
        elif args.listexternal is True:
            toml_filepath = Directories.get_program_dir()+"\\projects\\external_project_register.toml"
            data_tuple = toml_utils.load_toml_tuple(toml_filepath)
            print(data_tuple)

        elif args.current is True:
            print(f"Current project: {Directories.get_project_dir()}")
            
        elif args.new is not None and args.new is not False:
            dir_project_new = DirectoryControl.create_directory_with_structure(args.new,option="empty")
            #dir_project_new = DirectoryControl.create_directory(args.new)
            self.set_project_active(project_dir=dir_project_new)
            
        elif args.sample is not None and args.sample is not False:
            dir_project_new = DirectoryControl.create_directory_with_structure(args.sample,option="sample")
            #dir_project_new = DirectoryControl.create_directory(args.new)
            self.set_project_active(project_dir=dir_project_new) 
            
        elif args.open is not None:
            # Assess if the input textstring is a whole path or is a relative path.
            # A relative path will look in only the ./projects/ directory. 
            self.set_project_active(project_dir=args.open)
            # notes: [[]] https://realpython.com/python-pathlib/

        elif args.copy is True:
            DirectoryControl.copy_project_directory(Directories.get_project_dir(),option="empty")


        elif args.destroy is not None and args.destroy is not False:
            
            # deleting directly is not effective
            if False:
                DirectoryControl.destroy_directory(args.destroy)
            else:
                print(f"Manually delete: {args.destroy}")
                #instead, open the browser location for the user to delete
                self.do_open(f"-b projects")
        else:
            self.do_help("project")

    def do_p(self,line):
        " Abbreviation for project" 
        self.do_project(line)
    def do_projects(self,line):
        " Alis for project" 
        self.do_project(line)
    

    def do_ls(self,args):
        print(os.getcwd())
        print("\nDirectories:")
        for entry in os.listdir(os.getcwd()):
            if os.path.isdir(entry):
                print(f"\t{entry}")
        print("\nFiles:")
        for entry in os.listdir(os.getcwd()):
            if os.path.isfile(entry):
                print(f"\t{entry}")

    def do_cd(self,args):
        os.chdir(args)
        print(os.getcwd())
        

    template_cmd2_parser = cmd2.Cmd2ArgumentParser()
    template_cmd2_parser.add_argument('-n','--new',help='create new project directory')
    template_cmd2_parser.add_argument('-o','--open',help='access existing project directory')
    template_cmd2_parser.add_argument('--destroy',help='destroy existing project directory')
    template_cmd2_parser.add_argument('-t','--tree',help='print tree using library: null')
    @cmd2.with_argparser(template_cmd2_parser)
    def do_template_cmd2(self,args):
        if args.tree is not None:
            print(f"os.getcwd() =  {os.getcwd()}")
            self.do_tree(None)
        if args.destroy is not None:
            DirectoryControl.destroy_directory(args.destroy)
        else:
            self.do_help("template_cmd2")

    """ an alternative ecample
    defaults = config_utils.load_defaults('config.toml')    
    parser = argparse.ArgumentParser(description="Trim an audio file.")
    parser.add_argument("-i", "--input_file", type=str, default=defaults['input_file'], help="Path to the input audio file")
    parser.add_argument("-o", "--output_file", type=str, default=defaults['output_file'], help="Path to the output audio file")
    parser.add_argument("-s", "--start_time", type=float, default=float(defaults['start_time']), help="Start time in seconds")
    parser.add_argument("-e", "--end_time", type=float, default=defaults['end_time'], help="End time in seconds")
    """
    spark_parser = cmd2.Cmd2ArgumentParser()
    spark_parser.add_argument('-a','--all',nargs = "?", default=False, const=True,help='')
    spark_parser.add_argument('-t','--time',nargs = "?", default=False, const=True,help='')
    spark_parser.add_argument('-d','--depth',nargs = "?", default=False, const=True,help='')
    spark_parser.add_argument('-he','--height',nargs = "?", default=False, const=True,help='')
    spark_parser.add_argument('-i','--index',help='')
    spark_parser.add_argument('-s','--scaled',help='')
    @cmd2.with_argparser(spark_parser)
    def do_spark(self,args):
        """
        Spark graph preview. Use time, height, depth, or other options.
        
        Examples:
            spark height -all
            spark index 1
        """

        #if line.startswith("time") and "-all" in line:
        if args.time is True:
            #and "-all" in line:
            print("Time values")
            self.sparkarray_direction(self.scene_object.vectorArray_time)
            #self.spark_dict_vector_key("time")

        #elif line.startswith("height") and "-all" in line:
        elif args.height is True:
            print("Height values")
            self.sparkarray_direction(self.scene_object.vectorArray_height)
            #self.spark_dict_vector_key("height")
        
        #elif line.startswith("depth") and "-all" in line:
        elif args.depth is True:
            print("Depth values")
            self.sparkarray_direction(self.scene_object.vectorArray_depth)
            #self.spark_dict_vector_key("depth")
        elif args.all is True:
            self.do_spark("--time")
            self.do_spark("--height")
            self.do_spark("--depth")

        #elif line.startswith("index"):
        elif args.index is not None:
            i = int(args.index)
            
            key_i = list(self.hierarchy_object.dict_curve_objects_all.keys())[i]
            #i = int(line.split("index")[1])
            print(self.scene_object.names[i])
            print(f"i = {i}")
            print("-----")
            print("Time values")
            print(f"Header: {self.scene_object.headers_time[i]}")
            
            vector = self.hierarchy_object.dict_curve_objects_all[key_i].dict_data_vectors_raw["time"]

            all = [x-min(vector) for x in vector]
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)
            
            print("-----")
            print("Height values")
            print(f"Header: {self.scene_object.headers_height[i]}")
            vector = self.hierarchy_object.dict_curve_objects_all[key_i].dict_data_vectors_raw["height"]
            all = [x-min(vector) for x in vector]
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)

            print("-----")
            print("Depth values")
            print(f"Header: {self.scene_object.headers_depth[i]}")
            print(self.scene_object.headers_depth[i])
            vector = self.hierarchy_object.dict_curve_objects_all[key_i].dict_data_vectors_raw["depth"]
            all = [x-min(vector) for x in vector]
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)
            print("-----")

            """
            print("Depth values")
            vector = self.scene_object.vectorArray_depth[i]
            all = [x-min(vector) for x in vector]
            for line in sparklines(all,num_lines=1):
                print(line)
            """

        elif args.scaled is not None:
            print(f"args.scaled = {args.scaled}")
            i = int(args.scaled)
            print(self.scene_object.names[i])
            print(f"i = {i}")
            print("-----")
            print("Scaled Height values")
            key = list(self.hierarchy_object.dict_curve_objects_all)[i]
            curve_object = self.hierarchy_object.dict_curve_objects_all[key]
            vector = curve_object.dict_data_vectors_scaled["height"]
            #vector = self.scene_object.vectorArray_height[i]
            all = [x-min(vector) for x in vector]
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)
        else:
            self.do_help("spark")

    def sparkarray_direction(self,array):
        for i,vector in enumerate(array):
            print(self.scene_object.names[i])
            all = [x-min(vector) for x in vector]
            print(f"n = {i}")       
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)
    
    def spark_dict_vector_key(self,vector_key):
        for i,key in enumerate(self.hierarchy_object.dict_curve_objects_all):
            vector = self.hierarchy_object.dict_curve_objects_all[key].dict_data_vectors_raw[vector_key]
            print(self.scene_object.names[i])
            all = [x-min(vector) for x in vector]
            print(f"n = {i}")       
            print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}, min: {min(vector)}, max: {max(vector)}")
            for line in sparklines(all,num_lines=1):
                print(line)

    def sparkvector_direction(self,vector):
        i = int(line.split("-index")[1])
        print(self.scene_object.names[i])
        all = [x-min(vector) for x in vector]
        print(f"i = {i}")
        print(f"initial: {vector[0]}, last: {vector[-1]}, len: {len(vector)}")
        for line in sparklines(all,num_lines=1):
            print(line)

    def do_query(self,line):
        #Conversational characterization of data.
        hint_string = 'At any time you may see the default sample setting by typing [default].\nAlso, type quit to quit. This word, quit, cannot be a group name.\n   '
        print(f"{hint_string}")
        self.dict_query = self.characterization_mapping(self.characterization_query())


    def characterization_query(self):
        dict_query = dict()
        dict_query["data_file_single_or_multiple"] = str(input("Is your data in [one] single file or in [multiple] files? :: "))
        dict_query["points_or_curves_or_meshes"] = str(input("Would you characterize each data source as a [point], a [curve], or a [mesh]? :: "))
        dict_query["source_multiplicity_per_file"] = str(input(f"Is there [one] {dict_query['points_or_curves_or_meshes']} or [multiple] in each imported data file? :: "))
        dict_query["import_data_filetype"] = str(input("What filetype is/are your imported data file(s)? [FBX,CSV,XLSX,XLS]:: "))
        print("To choose an export style, please edit configuration JSON file or make a new one, and point to it with the config_entry.json file in your project. You can edit it with this command: open --config, open --entry. For guidance, use open --guide. ")
        return dict_query   
    
    def characterization_mapping(characterization_query):
        #relate raw responses to useful configuration values
        dict_query = characterization_query
        return dict_query
    
    def no_args(args):

        #major error 19 January 2025 - blockage - drop
        # There has to be a better way to say "if you only typed the command with no arguments"
        bool_are_there_args = args.cmd2_statement.__dict__['_Cmd2AttributeWrapper__attribute'].args 
        print(f"bool_are_there_args = {bool_are_there_args}")
        return "" == bool_are_there_args
    
    tree_parser = cmd2.Cmd2ArgumentParser()
    tree_parser.add_argument('-d','--dir', help='See the tree for a particularly directary.')
    @cmd2.with_argparser(tree_parser)
    def do_tree(self,args):
        "Tree"
        if args.dir is not None:
            fm.tree(args.dir)
        else:
            print(f"os.path.abspath(__file__) = {os.path.abspath(__file__)}")
            fm.tree(os.path.dirname(os.path.abspath(__file__)))

    def do_clear(self,line):
        
        if src.environment.windows():
            os.system('cls')
        else:
            os.system('clear')

    def do_htree(self,line):
        "Hierarchy tree, text."
        self.hierarchy_object.print_hierarchy_tree()
        #self.hierarchy_object.print_hierarchy_by_lineage()

    def do_hhtree(self,line):
        "Hierarchy tree, fancy."
        #self.hierarchy_object.print_hierarchy_tree()
        self.hierarchy_object.print_hierarchy_by_lineage()
    
    def do_stree(self,line):
        "Sibling tree."
        self.hierarchy_object.print_hierarchy_tree_sibling()
    def do_sstree(self,line):
        "Sibling tree, fancy."
        self.hierarchy_object.print_hierarchy_previous_siblings_by_lineage()
    def do_cctree(self,line):
        "Cousin tree."
        #self.hierarchy_object.print_hierarchy_tree_cousins()
        self.hierarchy_object.print_hierarchy_cousins_by_lineage()

    def do_dorsl(self,line):
        self.hierarchy_object.print_hierarchy_data_origins_relative_to_supergroup_by_lineage()

    def do_psl(self,line):
        self.hierarchy_object.print_hierarchy_place_in_supergroup_by_lineage()

    topo_parser = cmd2.Cmd2ArgumentParser()
    #topo_parser.add_argument('-t','--topo',nargs = "?", default=False, const=True, help='See topgraphy string, to test terminal capacity.')
    topo_parser.add_argument('-v','--vector', help='Example: topo -v [0,10,1,9,2,8,3,7,4,6,5,5,5,6,7,8,9,10,8,6,4,2,0,10,0,10]') 
    @cmd2.with_argparser(topo_parser)
    def do_topo(self,args):
        "Example: topo -v [0,10,1,9,2,8,3,7,4,6,5,5,5,6,7,8,9,10,8,6,4,2,0,10,0,10]"
        #if args.topo is True:
        #    print(self.topography)
        if args.vector is not None:
            for line in sparklines(eval(args.vector),num_lines=1):
                print(line)
            print("-----")
        else:
            print(self.topography)

    def do_assign(self, args):
        """Assign a variable dynamically."""
        try:
            key, value = args.split('=')
            self.vars[key.strip()] = value.strip()
            self.poutput(f"Variable '{key.strip()}' assigned to '{value.strip()}'")
        except ValueError:
            self.poutput("Usage: assign key=value")

    def do_show(self, _):
        """Show all variables."""
        for key, value in self.vars.items():
            self.poutput(f"{key} = {value}")


    def do_functions(self, args):
        """List all functions and methods of an imported module."""
        module_name = args.strip()
        module = self.modules.get(module_name)
        if module:
            functions = [attr for attr in dir(module) if callable(getattr(module, attr))]
            self.poutput(f"Functions and methods in '{module_name}': {functions}")
        else:
            self.poutput(f"Module '{module_name}' is not imported")

    def do_call(self, args):
        """Call a method from an imported library."""
        try:
            parts = args.split()
            module_name = parts[0]
            method_name = parts[1]
            method_args = []

            for arg in parts[2:]:
                if arg.startswith("self."):
                    method_args.append(getattr(self, arg[5:]))
                else:
                    method_args.append(eval(arg))

            module = self.modules.get(module_name)
            if module:
                method = getattr(module, method_name, None)
                if method:
                    result = method(*method_args)
                    self.poutput(f"Result: {result}")
                else:
                    self.poutput(f"Method '{method_name}' not found in module '{module_name}'")
            else:
                self.poutput(f"Module '{module_name}' is not imported")
        except ValueError:
            self.poutput("Usage: call <module_name> <method_name> [args...]")
        except Exception as e:
            self.poutput(f"An error occurred: {e}")

    def do_call2(self, args):
        """Call a method from an imported library using the notation module_name.method_name(args...)."""
        try:
            parts = args.split('(')
            method_path = parts[0]
            method_args_str = parts[1].rstrip(')')

            module_name, method_name = method_path.split('.')
            module = self.modules.get(module_name)

            if module:
                method = getattr(module, method_name, None)
                if method:
                    method_args = [eval(arg.strip()) for arg in method_args_str.split(',')]
                    result = method(*method_args)
                    self.poutput(f"Result: {result}")
                else:
                    self.poutput(f"Method '{method_name}' not found in module '{module_name}'")
            else:
                self.poutput(f"Module '{module_name}' is not imported")
        except ValueError:
            self.poutput("Usage: call <module_name>.<method_name>(args...)")
        except Exception as e:
            self.poutput(f"An error occurred: {e}")

    def do_eval(self, args):
        """Evaluate an expression using stored variables."""
        try:
            expr = self._substitute_vars(args)
            result = self._safe_eval(expr, self.context)
            self.poutput(f"{args} = {result}")
        except Exception as e:
            self.poutput(f"Error evaluating expression: {str(e)}")

    def _substitute_vars(self, expression):
        """Substitute variables in the expression with their values."""
        for key, value in self.vars.items():
            expression = expression.replace(key, value)
        return expression

    def _safe_eval(self, expression, context):
        """Safely evaluate an expression using ast and operator modules."""
        # Define allowed operators
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
            ast.USub: operator.neg,
        }

        def _eval(node, context):
            if isinstance(node, ast.Constant):  # <number>
                return node.n
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                return allowed_operators[type(node.op)](_eval(node.left, context), _eval(node.right, context))
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
                return allowed_operators[type(node.op)](_eval(node.operand, context))
            elif isinstance(node, ast.Name):  # <variable>
                return context[node.id]
            elif isinstance(node, ast.Attribute):  # <object.attribute>
                value = _eval(node.value, context)
                return getattr(value, node.attr)
            elif isinstance(node, ast.Call):  # <function call>
                func = _eval(node.func, context)
                args = [_eval(arg, context) for arg in node.args]
                return func(*args)
            elif isinstance(node, ast.Subscript):  # <variable>[<index>]
                value = _eval(node.value, context)
                if isinstance(node.slice, ast.Index):
                    index = _eval(node.slice.value, context)
                else:
                    index = _eval(node.slice, context)
                return value[index]
            else:
                raise TypeError(node)

        node = ast.parse(expression, mode='eval').body
        return _eval(node, context)


    batch_parser = cmd2.Cmd2ArgumentParser()
    batch_parser.add_argument('-f','--filepath', help='Path to the text file containing commands')
    @cmd2.with_argparser(batch_parser)
    def do_batch(self, args):
        """Run commands from a specified text file."""
        if args.filepath is not None:
            try:
                with open(args.filepath, 'r') as file:
                    for line in file:
                        command = line.strip()
                        if command:
                            print ("batch$> "+line)
                            self.onecmd(command)
            except Exception as e:
                self.perror(f"Error: {e}")

    def do_1(self,line):
        "make scene"
        self.make_scene(None)
    def do_2(self,line):
        "make config"
        self.makeconfig(None)
    def do_3(self,line):
        "skipinterface"
        self.do_skipinterface(None)
    def do_4(self,line):
        "import data, or, make data"
        self.import_data(None)
    def do_5(self,line):
        "make pointcloud, or, build_pointcoud"
        self.build_pointcloud(None)
    def do_6(self,line):
        "export or make export"
        self.do_export("fbx")


class DissertationCLI(PalovianCLI):
    pyfiglet_title =  """
     ____  _                   _        _   _             ____  ____
    |  _ \(_)___ ___  ___ _ __| |_ __ _| |_(_) ___  _ __ |___ \| ___|
    | | | | / __/ __|/ _ \ '__| __/ _` | __| |/ _ \| '_ \  __) |___ \\
    | |_| | \__ \__ \  __/ |  | || (_| | |_| | (_) | | | |/ __/ ___) |
    |____/|_|___/___/\___|_|   \__\__,_|\__|_|\___/|_| |_|_____|____/

    """
    prompt = '>> '
    intro = pyfiglet_title + \
    '''
    Welcome to the Dissertation25 Shell! 
    Type "help" or "h" to see available commands. 
    Type "instructions" or "i" to see a description of workflow.
    Type "gui" or "g" to launch the Graphical User Interface.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def do_task1(self,line=None):
        print("Task 1, start")
        import projects.task1.scripts.correctch2tables_figs_Cv_pguLtY3235 as file
        for key, values in file.items():
            print(key)
        if False:
            print("Task 1, complete")

def start_shell():
    app = DissertationCLI()
    app.onecmd_plus_hooks("test")
    #Directories.initilize_program_dir()
    app.initialize_scene_object()
    Directories.initialize_startup_project()
    app.cmdloop()

if __name__=='__main__':
    start_shell()
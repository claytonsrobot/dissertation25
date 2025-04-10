# __main__.py
from shell import shell
from pprint import pprint as pprint
def cli_entry():
    try:
        # Launch main
        shell.start_shell()
        #shell.shell.main()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = cli_entry()
    print(f"app = {app}")
    #print(f"app.__doc__ = {app.__doc__}")
    pprint(app.__doc__)
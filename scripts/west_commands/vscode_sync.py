'''vscode_sync.py

VScode snippets and extension synchronisation'''

from textwrap import dedent            
from west.commands import WestCommand 
from west import log                   
import os
import shutil
import git 

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class Vscode_sync(WestCommand):

    def __init__(self):
        super().__init__(
            'vscode_sync',
            'sync vscode snipets and extensions',
            dedent('''
            VScode snippets and extension synchronisation
            '''))

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        parser.add_argument('-o', '--optional', help='an optional argument')

        return parser         

    def do_run(self, args, unknown_args):
        # Pull latest git 
        g = git.cmd.Git(PROJECT_ROOT)

        # Check if running on Windows or Linux
        if(os.name == "posix"):
            VSCODE_SNIPETS_PATH = "~/.config/Code/User" # Linux
        elif (os.name == "nt"):
            VSCODE_SNIPETS_PATH = r'C:\Users\Chris\AppData\Roaming\Code\User\snippets' # Windows
        else:
            log.wrn("Unknonw operating system")

        log.inf("Syncing snippets ...", colorize=True)
        shutil.copy("templates/.vscode/BL_global.code-snippets", os.path.join(VSCODE_SNIPETS_PATH, "bl_global.code_snippets"))
        
        log.inf("Syncing extensions ...", colorize=True)
        with open('templates/.vscode/extensions.txt') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                os.system(f"code --install-extension {line.strip()} --force") # --force to install newer version
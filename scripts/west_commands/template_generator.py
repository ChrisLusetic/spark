'''template_generator.py

Initializes and generates templates  '''

from textwrap import dedent            
from west.commands import WestCommand 
from west import log                   
import os
import shutil
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class TemplatesInit(WestCommand):

    def __init__(self):
        super().__init__(
            'project-init',
            'Initializes and generates templates',
            dedent('''
            Initializes project
            '''))

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        parser.add_argument('-p', type=Path, required = False)

        return parser         

    def do_run(self, args, unknown_args):
        log.inf("Testing 1...", colorize=True)
        
class TemplatesGenerate(WestCommand):

    def __init__(self):
        super().__init__(
            'generate',
            'Initializes and generates templates',
            dedent('''
            Initializes and generates templates
            '''))

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        parser.add_argument('-p', type=Path, required = False)

        return parser         

    def do_run(self, args, unknown_args):
        log.inf("Testing 2...", colorize=True)
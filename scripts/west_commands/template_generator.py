'''template_generator.py

Initializes and generates templates  '''

from textwrap import dedent            
from west.commands import WestCommand 
from west import log                   
import os
import shutil
from pathlib import Path

import yaml
from yaml.loader import SafeLoader

CWD = os.getcwd()

class templateObj:
    def __init__(self, src_path, dst_path):
        self.src_path = src_path
        self.dst_path = dst_path

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

        name = "templates.yml"

        if(args.p):
            project_path = os.path.abspath(args.p)

        else:
            print("Using default path")
            project_path = CWD
        

        src = os.path.join(CWD, name)
        dst = os.path.join(project_path, name)
    
        if not os.path.exists(project_path):
            os.makedirs(project_path)

        print("Copying from:", src," to:", dst)
        shutil.copy(src,dst)
        
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
        list_of_jobs = []
        name = "templates.yml"

        if(args.p):
            project_path = os.path.abspath(args.p)
            
        else:
            print("Using default path")
            project_path = CWD
        
        src = os.path.join(project_path, name)
        print("PATH is: ", src)

        if not os.path.exists(src):
            print("No templates.yml at the location. Did you run blizard init?")
            
        else:
            with open(src) as f:
                yml_data = yaml.load(f, Loader=SafeLoader)
                print(yml_data)
            # Go through templates
            for template_item in yml_data:
                
                list_of_items = yml_data[template_item]["list"]
                for item in list_of_items:

                    # Add to list of jobs if marked "import = true"
                    if(item["import"] == True):
                        list_of_jobs.append(templateObj(item["src_path"], item["dst_path"]))

            # Generate templates from list
            for i in list_of_jobs:
                destination = os.path.join(project_path, i.dst_path)
                print("Copying: From: ",i.src_path, " To: ", destination)

                # # Create folders of they dont exist (.vscode, tools, scripts)
                head = os.path.split(destination)
                if not os.path.exists(head[0]):
                    os.makedirs(head[0])

                # Copy templates in folders
                shutil.copy(i.src_path, destination)
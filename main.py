import os
import argparse
from pathlib import Path
import shutil
import sys
import git 

import yaml
from yaml.loader import SafeLoader


CWD = os.getcwd()
TEMPLATES_YML_PATH = 'templates.yml'

class templateObj:
    def __init__(self, src_path, dst_path):
        self.src_path = src_path
        self.dst_path = dst_path


parser = argparse.ArgumentParser()

parser.add_argument('cmd', type=str)
parser.add_argument('-p', type=Path, required = False)
parser.add_argument('-n', type=str, required = False)

args = parser.parse_args()

# Usefull coomands `os.walk`

if (args.cmd == "test"):

    print("CWD: ",  CWD)
    print(args.p)

# Auto-search something like zehyr west. IE, "Not a blizard directory. initiazlie it it?
# Run blanalyzer

# if (args.cmd == "init"):

#     # project_path = "./TEST/.blizard/project_info.blzd"
#     # if not os.path.exists(os.path.dirname(project_path)):
#     #     os.makedirs(os.path.dirname(project_path))

#     # my_file = open(project_path, 'w', encoding='utf-8')

#     # print("# Generating project.blzd")
#     # my_file.write("# Bytelab project init list of options\n\n")

#     # with open(TEMPLATES_YML_PATH) as f:
#     #     yml_data = yaml.load(f, Loader=SafeLoader)

#     #     # Go through templates
#     #     for template_item in yml_data:
#     #         my_file.writelines(["\n", template_item, ":\n"])
#     #         list_of_items = yml_data[template_item]["list"]
#     #         for item in list_of_items:
#     #             my_file.writelines(["    ",item["name"], "\n"])

#     # my_file.close()
if (args.cmd == "init"):
    
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

if (args.cmd == "t"):
    name = "templates.yml"

    if(args.p):
        project_path = os.path.abspath(args.p)

    else:
        print("Using default path")
        project_path = CWD
    
    src = os.path.join(CWD, name)
    dst = os.path.join(project_path, name)

    with open(src) as f:
        yml_data = yaml.load(f, Loader=SafeLoader)
        print(yml_data)




if (args.cmd == "generate_templates"):

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

# TODO:
# add cronjob to autofetch and sync
# add all other templates
# enable/disable autosync
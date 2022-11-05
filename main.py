import os
import argparse
import shutil
import sys
import git 

import yaml
from yaml.loader import SafeLoader


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class templateObj:
    def __init__(self, src_path, dst_path):
        self.src_path = src_path
        self.dst_path = dst_path


# Defines
tmp_path = "tmp/"
west_template_path = "templates/west.yml"
west_name = "west.yml"

workspace_sufix = "_workspace/"
project_name_token = "<name>"

parser = argparse.ArgumentParser()

parser.add_argument('cmd', type=str)
parser.add_argument('-p', type=str, required = False)
parser.add_argument('-n', type=str, required = False)

args = parser.parse_args()

# Commands
if (args.cmd == "generate"):
    if not args.p or not args.n:
        print("Missing path and/or name arguments")
        sys.exit()

    print("Generating new project")

    # Create temp folder

    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)

    os.mkdir(tmp_path)

    # Create workspace folder
    workspace_name = args.n + workspace_sufix
    os.mkdir(tmp_path+ workspace_name)

    # Create project folder
    dst_path = tmp_path +  workspace_name + args.n
    os.mkdir(dst_path)

    # Copy west
    shutil.copy(west_template_path, dst_path)

    # Edit west project name
    with open(os.path.join(dst_path, west_name), 'r') as file :
        filedata = file.read()
    
    filedata = filedata.replace(project_name_token, args.n)

    with open(os.path.join(dst_path, west_name), 'w') as file:
        file.write(filedata)
    
    # Append west modules

    # Copy west file to project
    shutil.copytree(dst_path, os.path.join(args.p, workspace_name, args.n), symlinks=False, ignore=None, ignore_dangling_symlinks=False)

    shutil.rmtree(tmp_path)

if (args.cmd == "test2"):
    print ("\033[92m TEST")

if (args.cmd == "generate_templates"):

    project_path = "./TEST/"
    list_of_jobs = []

    with open('templates.yml') as f:
        data = yaml.load(f, Loader=SafeLoader)
    
    for template in data:
        
        list = data[template]["list"]
        for item in list:
            if(item["import"] == True):
                list_of_jobs.append(templateObj(item["src_path"], item["dst_path"]))


    # Generate templates
    for i in list_of_jobs:
        print("Copying: From: ",i.src_path, " To: ", os.path.join(project_path, i.dst_path))
        shutil.copy(i.src_path, os.path.join(project_path, i.dst_path))

if (args.cmd == "sync_vscode"):
    # Pull latest git 
    g = git.cmd.Git(PROJECT_ROOT)
    # print(g.pull())

    # Check if running on Windows or Linux
    if(os.name == "posix"):
        VSCODE_SNIPETS_PATH = "~/.config/Code/User" # Linux
    elif (os.name == "nt"):
        VSCODE_SNIPETS_PATH = r'C:\Users\Chris\AppData\Roaming\Code\User\snippets' # Windows
    else:
        print("Unknonw operating system")

    # Copy snippets
    shutil.copy("templates/.vscode/BL_global.code-snippets", os.path.join(VSCODE_SNIPETS_PATH, "bl_global.code_snippets"))
    
    # Install vscode extensions
    with open('templates/.vscode/extensions.txt') as f:
        while True:
            line = f.readline()
            if not line:
                break
            os.system(f"code --install-extension {line.strip()} --force") # --force to install newer version

# TODO:
# add wizard
# check if file already exists, if yes, override
# check if folder exists, if not create
# change path to be current, or user can specify
# add option to just add specifics stuff: spark generate_specific clang-zephyr

# add cronjob to autofetch and sync
# add all other templates
# enable/disable autosync
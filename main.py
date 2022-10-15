import os
import argparse
import pathlib
import shutil
import sys
# Defines
tmp_path = "tmp/"
west_template_path = "templates/west.yml"
west_name = "west.yml"

workspace_sufix = "_workspace/"
project_name_token = "<name>"


parser = argparse.ArgumentParser()

# os.system('west -v')

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

    # # Copy west
    shutil.copy(west_template_path, dst_path)

    # Edit west
    with open(os.path.join(dst_path, west_name), 'r') as file :
        filedata = file.read()
    
    filedata = filedata.replace(project_name_token, args.n)

    with open(os.path.join(dst_path, west_name), 'w') as file:
        file.write(filedata)
    
    shutil.copytree(dst_path, os.path.join(args.p, workspace_name, args.n), symlinks=False, ignore=None, ignore_dangling_symlinks=False)

    shutil.rmtree(tmp_path)

if (args.cmd == "init"):
    os.system('west init -l ' + str(args.p))
    print('west init -l ' + str(args.p))

    
if (args.cmd == "update"):
    os.system('west update')

if (args.cmd == "test"):
    print (os.path.abspath(__file__))

if (args.cmd == "generate_vscode"):

    if not args.p or not args.n:
        print("Missing path and/or name arguments")
        sys.exit()

    workspace_name = args.n + workspace_sufix

    shutil.copytree(os.path.join("templates/.vscode"), os.path.join(args.p, workspace_name, args.n, ".vscode"), symlinks=False, ignore=None, ignore_dangling_symlinks=False)

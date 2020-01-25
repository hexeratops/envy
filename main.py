import venv 
import os
import sqlite3
import pathlib
import json
import shutil

from configparser import ConfigParser
from pprint import pprint



def activate(path):
    #TBD: Windows support
    os.system("source " + os.path.join(path, "bin", "activate") + ";/bin/bash")

def load_cfg():
    folder_path = os.path.expanduser("~/.config/envy")
    cfg_file = os.path.expanduser("~/.config/envy/envs")

    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    if not os.path.isfile(cfg_file):
        with open(cfg_file, 'w') as fd:
            fd.write('{"environments": [], "backups": []}')

    if os.path.getsize(cfg_file) > 0:
        with open(cfg_file, 'r') as fd:
            return json.load(fd)
    return None

def save(entries):
    cfg_file = os.path.expanduser("~/.config/envy/envs")
    with open(cfg_file, 'w') as fd:
        json.dump(entries, fd)
    
def create_env(entries, new_path):
    name = input("Name: ")
    dir_loc = input("Folder path: ")
    dir_loc = os.path.abspath(os.path.expanduser(dir_loc))

    if entries is not None:
        for env in entries['environments']:
            if env['name'] == name:
                print("Cannot use a duplicate name. Please choose another.")
                return
            elif env['path'] == dir_loc:
                print("Cannot add multiple entries to the same environment.")
                return

    if os.path.isdir(dir_loc) and new_path:
        print("Directory already exists; cannot create a new environment here.")
        return
    elif not os.path.isdir(dir_loc) and not new_path:
        print("Directory does not exist; please choose another folder location")
        return

    if new_path:
        venv.create(dir_loc)
    entries['environments'].append({'id': 0, 'name': name, 'path': dir_loc})
    save(entries)

def delete_env(entries):
    if entries is None:
        return

    get_info(entries)
    name = input("Name: ")

    for i in range(0, len(entries['environments'])):
        if entries['environments'][i]['name'] == name:
            env_del = input("Delete the environment as well? (y/n): ")

            if env_del == 'y' or env_del == 'Y':
                shutil.rmtree(entries['environments'][i]['path'])
            del entries['environments'][i]
            
            save(entries)
            input("Successfully removed environment.")
            return
    print("Failed to find requested environment.")

def activate_env(entries):
    if entries is None:
        return

    get_info(entries)
    name = input("Name: ")

    for env in entries['environments']:
        if env['name'] == name:
            activate(env['path'])
            exit(0)

    input("Failed to find specified environment")

def get_info(entries):
    if entries is None:
        return

    print("\nINSTALLED ENVIRONMENTS")
    for env in entries['environments']:
        cfg = os.path.join(env['path'], 'pyvenv.cfg')
        py_ver = "?.?.?"

        if os.path.isfile(cfg):
            pyvenv = ConfigParser()
            with open(cfg) as fd:
                tmp = "[root]\n" + fd.read().strip()
                pyvenv.read_string(tmp)
                py_ver = pyvenv["root"]["version"]

        print(env['name'] + "\tpython " + py_ver + "\t" + env['path'])

def print_menu():
    print("")
    print("1) Activate environment")
    print("2) Create new environment")
    print("3) Add existing environment")
    print("4) Remove environment")
    print("5) List environments")
    print("")
    print("6) Backup environment*")
    print("7) Restore environment*")
    print("8) Delete backups*")
    print("9) Quit")
    print("")

def main():
    while True:
        entries = load_cfg()
        print_menu()
        opt = input("> ")
        if opt == "1":
            activate_env(entries)
        elif opt == "2":
            create_env(entries, True)
        elif opt == "3":
            create_env(entries, False)
        elif opt == "4":
            delete_env(entries)
        elif opt == "5":
            get_info(entries)
        elif opt == "9":
            break

if __name__ == "__main__":
    main()

import os
import random
import shutil
import subprocess
import sys

from movie_maker import create_movie_from_user_input
from scene_maker import create_scenes

dir_filename = "input.txt"
file_types = (".jpg", ".png")
files = {}
paths = []
fav_dirs = []
batch_move = False

windows = False
linux_image_viewer = "chafa"


def main():
    print("\n\t\t-- SLIDE MOVIE MAKER --")
    get_dirs()
    get_info()
    main_menu()


def get_files(file_dir, overwrite=False):
    if len(files[file_dir]
           ) == 0 or overwrite:  # scan dir if not already scanned
        files[file_dir] = [
            file for file in os.listdir(file_dir) if file.endswith(file_types)
        ]
    return files[file_dir]


def get_paths():
    """ returns a list of paths to the files contained in the input_dirs"""
    if paths:
        return paths
    scene_files = []
    for input_dir, input_files in files.items():
        for input_file in input_files:
            scene_files.append(os.path.join(input_dir, input_file))
    return scene_files


def get_input(prompt="-> "):
    selection = input(prompt)
    if selection.isdigit() == False:
        return get_input("Not a valid selection\n-> ")
    return int(selection)


def get_info():
    for d, f in files.items():  # scan all dirs
        f = get_files(d, True)
    print("\nInput Directories:")
    for i, file_dir in enumerate(list(files.keys())):
        print(f"\t{i+1}) {len(get_files(file_dir))} files in {file_dir}")
    print("\nScene Directories:")
    for i, file_dir in enumerate(fav_dirs):
        print(f"\t{i+1}) {len(os.listdir(file_dir))} files in {file_dir}")


def get_dirs():
    for source_dir, _, _ in os.walk("./scenes/"):
        fav_dirs.append(source_dir)

    with open(dir_filename, "r") as file:
        dir_names = [
            line.rstrip() for line in file.readlines()
            if not line.startswith("#")
        ]
        for i in range(0, len(dir_names)):
            if dir_names[i] != "":
                files[dir_names[i]] = []
            else:
                break


def main_menu():
    if len(files) == 0:
        print("No input files found")
        sys.exit()

    print("\n\bMain Menu:")
    menu = [
        "Create Scenes",
        "Create Movie",
        "Get Info",
        "Quit",
    ]
    for i, item in enumerate(menu):
        print("%d) %s" % (i + 1, item))

    match get_input():
        case 1:
            create_scenes(get_paths())
        case 2:
            create_movie_from_user_input()
        case 3:
            get_info()
        case 4:
            sys.exit()
        case _:
            main_menu()

    main_menu()


if __name__ == "__main__":
    main()

import os, sys
from functools import reduce
import pymovie

def main():
    target_dir = 'default'
    if len(sys.argv) > 1:
        target_dir = sys.argv[1] 
    print(combine_dir(target_dir))

def add_paths(paths, target_dir) -> list[str]:
    for path in os.listdir(target_dir):
        paths.append(f'{target_dir}/{path}')
    return paths

def combine_dir(target_dir):
    paths = add_paths([], target_dir)
    return reduce(merge, paths)

def merge(a, b):
    return a + b

if __name__ == "__main__":
    main()

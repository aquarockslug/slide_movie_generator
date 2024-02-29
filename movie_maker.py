import os, sys
from functools import reduce
# import pymovie

def main():
    source_dir = 'default'
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]

    print(merge_videos([source_dir]))

def get_paths(paths, target_dir) -> list[str]:
    for path in os.listdir(target_dir):
        paths.append(f'{target_dir}/{path}')
    return paths

def merge_videos(source_dirs):
    paths = []
    for source_dir in source_dirs:
        paths = get_paths(paths, source_dir)
    return reduce(merge, paths)

def merge(a, b):
    return a + b

if __name__ == "__main__":
    main()

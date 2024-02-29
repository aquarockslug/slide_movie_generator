import os, sys
from functools import reduce
# import pymovie

def main():
    source_dir = 'default'
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    
    print(merge_videos(source_dir))

def get_path(source_dir):
    for path in os.listdir(source_dir):
        yield f'{source_dir}/{path}'

def merge_videos(source_dir):
    return reduce(merge, get_path(source_dir))

def merge(a, b):
    return a + b

if __name__ == "__main__":
    main()

import os, sys
from functools import reduce

# import pymovie


def main():
    source_dir = "default"
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]

    video = map(merge_dir, [source_dir])

    print(list(video))


def merge_dir(source_dir):
    def get_paths(source_dir):
        for path in os.listdir(source_dir):
            yield f"{source_dir}/{path}"

    def merge(a, b):
        return a + b

    return reduce(merge, get_paths(source_dir))


if __name__ == "__main__":
    main()

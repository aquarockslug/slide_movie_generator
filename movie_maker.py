import os, sys
from functools import reduce

from moviepy.editor import ImageClip, concatenate_videoclips


def main():
    source_dir = "default"
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]

    video = merge_dirs([source_dir])
    video.write_videofile("output/default.mp4", fps=12)


def merge_dirs(source_dirs):
    """ merge multiple directories """
    merged_dirs = map(merge_dir, source_dirs)
    return reduce(merge, merged_dirs)


def merge_dir(source_dir):
    """ merge all of the videos in the given directory """

    def get_paths(source_dir):
        for path in os.listdir(source_dir):
            yield f"{source_dir}/{path}"

    return reduce(merge, get_paths(source_dir))


def merge(a, b):
    if isinstance(a, str):
        a = ImageClip(a).set_duration(2)
    if isinstance(b, str):
        b = ImageClip(b).set_duration(2)
    return concatenate_videoclips([a, b], method="compose")


if __name__ == "__main__":
    main()

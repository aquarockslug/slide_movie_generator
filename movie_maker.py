import os
import sys
from functools import reduce

from moviepy.editor import *


def main():
    source_dirs = ["source/default", "source/test"]
    if len(sys.argv) > 1:
        source_dirs = sys.argv[1:]

    text_files = ["text.txt"]

    save_video(source_dirs, text_files, "output/default.mp4")


def save_video(source_dirs, text_files, output_name):

    def confirm_save_video(source_dirs, text_files, output):
        print("\nText Files:")
        for index, text_file in enumerate(text_files):
            print(f"{index + 1}) {text_file}")
        print("\nSource Directories:")
        for index, source_dir in enumerate(source_dirs):
            print(f"{index + 1}) {source_dir}")
        return input(f'\ncreate file "{output}"? (y/n): ').lower() == 'y'

    if confirm_save_video(source_dirs, text_files, output_name):
        output = create_video(source_dirs, text_files)
        output.write_videofile(output_name, fps=6)


def create_video(source_dirs, text_files):
    """merge multiple directories"""

    def text_clip():
        for line in lines(text_files):
            yield TextClip(line, fontsize=75, color='black').set_pos('center')

    text_clip_gen = text_clip()

    def add_line_from_files(video):
        return CompositeVideoClip(
            [video, next(text_clip_gen).set_duration(video.duration)])

    return reduce(merge, map(add_line_from_files, map(merge_dir, source_dirs)))


def lines(text_files):
    """returns a generator that yields a line from the text_files"""

    def get_lines(text_file):

        lines_in_this_file = []
        with open(text_file, encoding='utf-8') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                lines_in_this_file.append(line)

        yield from lines_in_this_file

    for file in text_files:
        yield from get_lines(file)


def merge_dir(source_dir):
    """merge all of the videos in the given directory"""

    def get_paths(source_dir):
        for path in os.listdir(source_dir):
            yield f"{source_dir}/{path}"

    return reduce(merge, get_paths(source_dir))


def merge(a, b):
    """concatenate a and b"""
    if isinstance(a, str):
        a = ImageClip(a).set_duration(1)
    if isinstance(b, str):
        b = ImageClip(b).set_duration(1)
    return concatenate_videoclips([a, b], method="compose")


if __name__ == "__main__":
    main()

import os
import sys
from functools import reduce

from moviepy.editor import *


def main():
    text_files = ["text.txt"]
    output_name = 'output/default.mp4'
    source_dirs = ["source/default", "source/test"]
    if len(sys.argv) > 1:
        source_dirs = sys.argv[1:]

    def display_list(title, data_list):
        print("\n", title)
        for index, data in enumerate(data_list):
            print(f"{index + 1}) {data}")

    def confirm_save_video(source_dirs, text_files, output):
        display_list('Text Files:', text_files)
        display_list('Source Directories:', source_dirs)
        return input(f'\ncreate file "{output}"? (y/n): ').lower() == 'y'

    def text_clips():
        """returns a generator that yields TextClips"""
        for line in lines(text_files):
            yield TextClip(line, fontsize=75, color='black').set_pos('center')

    if confirm_save_video(source_dirs, text_files, output_name):
        output = create_video(source_dirs, text_clips())
        output.write_videofile(output_name, fps=6)


def create_video(source_dirs, text_clip_gen):
    """create video from the source_dirs merged with TextClips from the text_clip_gen"""

    def merge(a, b):
        if isinstance(a, str):
            a = ImageClip(a).set_duration(1)
        if isinstance(b, str):
            b = ImageClip(b).set_duration(1)
        return concatenate_videoclips([a, b], method="compose")

    def merge_dir(source_dir):
        """merge all of the videos in the given directory"""

        def get_paths(source_dir):
            for path in os.listdir(source_dir):
                yield f"{source_dir}/{path}"

        return reduce(merge, get_paths(source_dir))

    def add_line_from_text(video):
        return CompositeVideoClip(
            [video, next(text_clip_gen).set_duration(video.duration)])

    return reduce(merge, map(add_line_from_text, map(merge_dir, source_dirs)))


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


if __name__ == "__main__":
    main()

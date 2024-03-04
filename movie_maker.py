import os, sys
from functools import reduce

from moviepy.editor import ImageClip, concatenate_videoclips


def main():
    source_dirs = ["default"]
    if len(sys.argv) > 1:
        source_dir = sys.argv[1:]

    # get_text_clips()
    create_video(source_dirs, "output/default.mp4")


def get_text_clips():
    for file in get_paths("text"):
        print(list(get_text(file)))


def get_text(text_file):
    def get_lines_from_file(filename):
        lines = []
        with open(filename) as file:
            while True:
                line = file.readline()
                if not line:
                    break
                lines.append(line)
        return lines

    for line in get_lines_from_file(text_file):
        yield line


def create_video(source_dirs, output_name):
    def confirm_create_video(source_dirs, output):
        print(list(get_text("text/text.txt")))
        for index, source_dir in enumerate(source_dirs):
            print(f"{index}) {source_dir}")
        response = input(f'create file "{output}"? (y/n): ').lower()
        return True if response == "y" else False

    if confirm_create_video(source_dirs, output_name):
        merge_dirs(source_dirs).write_videofile(output_name, fps=12)


def merge_dirs(source_dirs):
    """merge multiple directories"""
    merged_dirs = map(merge_dir, source_dirs)
    return reduce(merge, merged_dirs)


def get_paths(source_dir):
    for path in os.listdir(source_dir):
        yield f"{source_dir}/{path}"


def merge_dir(source_dir):
    """merge all of the videos in the given directory"""
    return reduce(merge, get_paths(source_dir))


def merge(a, b):
    if isinstance(a, str):
        a = ImageClip(a).with_duration(2)
    if isinstance(b, str):
        b = ImageClip(b).with_duration(2)
    return concatenate_videoclips([a, b], method="compose")


if __name__ == "__main__":
    main()

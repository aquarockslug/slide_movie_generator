import os
import sys
from dataclasses import dataclass
from functools import reduce
from moviepy.editor import *


@dataclass
class MovieData:
    """contains all the data needed to create a movie"""
    source_dirs = []
    text_files = ['text.txt']
    output_name = 'output/default.mp4'
    beat_interval = 0.92


def create_movie_from_args():
    """create a movie using movie_data()"""
    create_movie_from_data(get_movie_data_from_args())


def create_movie_from_data(movie_data):
    """create a movie with the data from the Movie dataclass"""

    def confirm_movie_data(movie_data):
        """prompt user to confirm that the movie data is correct"""

        def display_list(title, data_list):
            print("\n", title)
            for index, data in enumerate(data_list):
                print(f"{index + 1}) {data}")

        display_list('Text Files:', movie_data.text_files)
        display_list('Source Directories:', movie_data.source_dirs)

        return input(f'\ncreate file "{movie_data.output_name}"? (y/n): '
                     ).lower() == 'y'

    def text_clips():
        """returns a generator that yields TextClips"""
        for line in lines(movie_data.text_files):
            yield TextClip(line, fontsize=75, color='black').set_pos('center')

    if confirm_movie_data(movie_data):
        output = create_movie(movie_data.source_dirs, movie_data.beat_interval,
                              text_clips())
        output.write_videofile(movie_data.output_name, fps=6)


def get_movie_data_from_args():
    """creates default movie data then modifies it with sys.argv"""
    movie_data = MovieData()

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            movie_data.source_dirs.append('source/' + arg)
    else:
        movie_data.source_dirs = ['source/default']

    return movie_data


def create_movie(source_dirs, beat_interval, text_clip_gen):
    """create movie from the source_dirs merged with TextClips generated from the text_clip_gen"""

    def merge(a, b):
        if isinstance(a, str):
            a = ImageClip(a).set_duration(beat_interval)
        if isinstance(b, str):
            b = ImageClip(b).set_duration(beat_interval)
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

    # merge dir, add text, merge
    return reduce(merge, map(add_line_from_text, map(merge_dir, source_dirs)))


def lines(text_files):
    """returns a generator that yields a line from the text_files"""

    def lines_in(text_file):
        lines_in_this_file = []
        with open(text_file, encoding='utf-8') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                lines_in_this_file.append(line)

        yield from lines_in_this_file

    for text_file in text_files:
        yield from lines_in(text_file)


if __name__ == "__main__":
    create_movie_from_args()

import os
import sys
from dataclasses import dataclass
from create_movie import create_movie
from moviepy.editor import (
    CompositeVideoClip,
    ImageClip,
    TextClip,
    concatenate_videoclips,
)
from moviepy.video.fx.all import crop
from create_movie import create_movie


@dataclass
class MovieData:
    """contains all the data needed to create a movie"""

    source_dirs = []
    text_files = ["text.txt"]
    output_name = "output/default.mp4"
    image_interval = 1
    has_countdown = False


def create_movie_from_user_input():
    """create a movie using movie_data()"""
    create_movie_from_data(get_movie_data_from_input())


def get_movie_data_from_input():
    """creates default movie data then modifies it with user input"""
    movie_data = MovieData()

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            movie_data.source_dirs.append("source/" + arg)
    else:
        for source_dir, _, _ in os.walk("source/"):
            movie_data.source_dirs.append(source_dir)
        movie_data.source_dirs.pop(0)

    if input("Add Countdown? (y/n): ").lower() == "y":
        movie_data.has_countdown = True

    return movie_data


def create_movie_from_data(movie_data):
    """create a movie with the data from the Movie dataclass"""

    def confirm_movie_data(movie_data):
        """prompt user to confirm that the movie data is correct"""

        def display_list(title, data_list):
            print("\n", title)
            for index, data in enumerate(data_list):
                print(f"{index + 1}) {data}")

        print("\n--- MOVIE SETTINGS ---")
        display_list("Text Files:", movie_data.text_files)
        display_list("Source Directories:", movie_data.source_dirs)

        print("\nEffects: ")
        if movie_data.has_countdown:
            print("Countdown")

        return (input(f'\ncreate file "{movie_data.output_name}"? (y/n): ').
                lower() == "y")

    def text_clips():
        """returns a generator that yields TextClips"""
        for line in lines(movie_data.text_files):
            yield TextClip(
                line,
                method="caption",
                font="Unicorns-Are-Awesome",
                size=[1080, 1080],
                color="pink2",
            ).set_pos("center")

    if confirm_movie_data(movie_data):
        new_movie = create_movie(movie_data, text_clips())
        crop(new_movie(),
                     width=1080).write_videofile(movie_data.output_name, fps=1)


def lines(text_files):
    """returns a generator that yields a line from the text_files"""

    def lines_in(text_file):
        lines_in_this_file = []
        with open(text_file, encoding="utf-8") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                lines_in_this_file.append(line)

        yield from lines_in_this_file

    for text_file in text_files:
        yield from lines_in(text_file)


if __name__ == "__main__":
    create_movie_from_user_input()

import os
from functools import reduce
from moviepy.editor import (CompositeVideoClip, ImageClip, TextClip,
                            concatenate_videoclips)


def create_movie(movie_data, text_clip_gen):
    """create movie using MovieData and TextClips generated from the text_clip_gen"""

    def merge(a, b):
        return concatenate_videoclips([a, b], method="compose")

    def get_paths(source_dir):
        for path in reversed(sorted(os.listdir(source_dir))):
            yield f"{source_dir}/{path}"

    def create_image_clip(path):
        return ImageClip(path).set_duration(
            movie_data.image_interval).resize(height=1080)

    def create_countdown_video(source_dir):
        """add numbers to images in source_dir and merges them"""

        def countdown():
            yield from reversed(range(1, 9))

        number_gen = countdown()

        def add_number(video):
            next_number = next(number_gen)
            if next_number:
                number_clip = ImageClip(
                    f'blank_countdown/{next_number}.png').set_duration(
                        video.duration).resize(height=1080)
                return CompositeVideoClip([video, number_clip])
            # dont change anything if there isn't a number
            return video

        return reduce(
            merge,
            map(add_number, map(create_image_clip, get_paths(source_dir))))

    def create_normal_video(source_dir):
        """merges images in source_dir"""
        return reduce(merge, map(create_image_clip, get_paths(source_dir)))

    def add_line_from_text(video):
        return CompositeVideoClip(
            [video, next(text_clip_gen).set_duration(video.duration)])

    # create a sequence of mapping and reducing to execute based on input
    if movie_data.has_countdown:

        def movie():
            return reduce(
                merge,
                map(add_line_from_text,
                    map(create_countdown_video, movie_data.source_dirs)))
    else:

        def movie():
            return reduce(
                merge,
                map(add_line_from_text,
                    map(create_normal_video, movie_data.source_dirs)))

    return movie

from difflib import SequenceMatcher
from functools import reduce
from math import dist
from random import shuffle

import scene_hasher


def get_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def find_matches(target_hash, hash_paths, threshold=0.2):
    """ yields hash_paths of images similar to target_hash """
    for image_hash in hash_paths:
        simularity = get_similarity(image_hash[0], target_hash)
        if image_hash[0] == target_hash:
            print("Exact match:", image_hash[1])
            continue
        if simularity > threshold:
            print(simularity * 100, "match:", image_hash[1])
            yield image_hash


def choose_targets(all_points, target_count=10):
    """ splits the points into target and non-target """
    shuffle(all_points)
    return all_points[:target_count], all_points[target_count:]


def convert_to_points(hash_paths):
    """ convert hashes into coordinates """
    return [(calculate_point(image_hash), path)
            for image_hash, path in hash_paths]


def calculate_point(image_hash):
    """ create points from image_hash (x, y)  """

    def base16(factor):
        return int(factor, base=16)

    def get_modulo(factor):
        return base16(factor) % 16

    def get_average(factor):
        return reduce(lambda a, b: a + b,
                      map(lambda char: int(char, base=16), factor),
                      0) / len(factor)

    placement_func = [get_average, get_modulo, base16][2]
    return (placement_func(image_hash[:len(image_hash) // 2]),
            placement_func(image_hash[len(image_hash) // 2:]))


def create_scenes(paths):
    """ move images from input path to scene directory """

    hash_paths = list(zip(scene_hasher.hash(paths), paths))
    if not hash_paths:
        print("hashing error")
        return

    point_paths = convert_to_points(hash_paths)
    targets, points = choose_targets(point_paths)

    clusters = []
    dist_sum = 0
    for point in points:
        distances = [
            dist(targets[i][0], point[0]) for i in range(0, len(targets))
        ]
        min_distance = min(distances)
        dist_sum += min_distance
        # clusters: path -> target
        clusters.append((targets[distances.index(min_distance)][1], point[1]))

    def display_clusters():
        for target in targets:
            print("\n" + str(target[1]))
            for image in clusters:
                if image[0] == target[1]:
                    print("   ", image[1])
        print("\nGroup spread: " + str(round(dist_sum)))

    display_clusters()

import os
import shutil
import string
from difflib import SequenceMatcher
from functools import reduce
from math import dist
from random import choice, shuffle

import scene_hasher


def create_scenes(paths, average_images_per_scene=5):
    print("Calculating image hashes...")
    hash_paths = list(zip(scene_hasher.hash(paths), paths))
    cluster_count = round(len(paths) / average_images_per_scene)
    cluster_count = cluster_count if cluster_count <= 25 else 25
    generate(hash_paths, cluster_count)


def generate(hash_paths, cluster_count):
    generated_clusters, spread_values = [], []
    for _ in range(0, 1000):
        clusters, spread_value = create_clusters(hash_paths, cluster_count)
        generated_clusters.append(clusters)
        spread_values.append(spread_value)

    best_spread = min(spread_values)
    best_index = spread_values.index(best_spread)

    print("Amount of clusters: ", cluster_count)
    print("Average spread: ", sum(spread_values) / len(spread_values))
    print("Best spread: ", str(round(best_spread)))

    if input("Create scenes? (y/n) ").lower() == "y":
        copy_images(generated_clusters[best_index])
    else:
        generate(hash_paths, cluster_count)

    print("Copying files...")


def choose_targets(all_points, target_count):
    """ splits the points into target and non-target """
    shuffle(all_points)
    return all_points[:target_count]


def convert_to_points(hash_paths):
    """ convert hashes into coordinates """
    return [(calculate_point(image_hash), path)
            for image_hash, path in hash_paths]


def calculate_point(image_hash):
    """ create points from image_hash (x, y)  """

    def base16(factor):
        return int(factor, base=16)

    def modulo(factor):
        return base16(factor) % 16

    def average(factor):
        return reduce(lambda a, b: a + b,
                      map(lambda char: int(char, base=16), factor),
                      0) / len(factor)

    def similarity(a):
        return SequenceMatcher(None, a, "1111111111111111").ratio() * 16

    placement_func = [average, similarity, modulo, base16]
    return (placement_func[0](image_hash), placement_func[1](image_hash))


def create_clusters(hash_paths, cluster_count):
    """ returns a list of (image_path, cluster_index) """

    point_paths = convert_to_points(hash_paths)
    targets = choose_targets(point_paths, cluster_count)

    clusters = []
    dist_sum = 0
    for point_path in point_paths:
        point = point_path[0]
        distances = [
            dist(targets[i][0], point) for i in range(0, cluster_count)
        ]
        min_distance = min(distances)
        dist_sum += min_distance
        clusters.append((point_path[1], distances.index(min_distance)))

    return [clusters, dist_sum]


def copy_images(clusters):
    dest_image_path = None
    target_scene_names = list(string.ascii_lowercase)
    for image_path, target_index in clusters:
        target_scene_name = target_scene_names[target_index]
        dest_image_path = new_scene_image(image_path, target_scene_name)
        # print(f"Copied {image_path} to {target_scene_name}")
    return dest_image_path


def new_scene_image(file_path, scene_name):
    scene_dir = os.path.join("scenes", scene_name)
    image_name = "".join(
        [choice(list(string.ascii_lowercase)) for i in range(0, 6)])
    if not os.path.exists(scene_dir):
        os.makedirs(scene_dir)

    dest_image_path = os.path.join("scenes", scene_name, image_name)

    shutil.copyfile(file_path, dest_image_path)
    return dest_image_path

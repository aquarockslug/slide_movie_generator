#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import sys

import numpy as np
from PIL import Image

import imagehash

hashfuncs = [
    ("ahash", imagehash.average_hash),
    ("phash", imagehash.phash),
    ("dhash", imagehash.dhash),
    ("whash-haar", imagehash.whash),
    ("whash-db4", lambda img: imagehash.whash(img, mode="db4")),
    ("colorhash", imagehash.colorhash),
]


def alpharemover(image):
    if image.mode != "RGBA":
        return image
    canvas = Image.new("RGBA", image.size, (255, 255, 255, 255))
    canvas.paste(image, mask=image)
    return canvas.convert("RGB")


def image_loader(hashfunc, hash_size=8):

    def function(path):
        image = alpharemover(Image.open(path))
        return hashfunc(image)

    return function


def with_ztransform_preprocess(hashfunc, hash_size=8):

    def function(path):
        image = alpharemover(Image.open(path))
        image = image.convert("L").resize((hash_size, hash_size),
                                          Image.ANTIALIAS)
        data = image.getdata()
        quantiles = np.arange(100)
        quantiles_values = np.percentile(data, quantiles)
        zdata = (np.interp(data, quantiles_values, quantiles) / 100 *
                 255).astype(np.uint8)
        image.putdata(zdata)
        return hashfunc(image)

    return function


def hashes(files=sys.argv[1:]):
    if isinstance(files, str):
        files = [files]
    hashfuncopeners = [(name, image_loader(func)) for name, func in hashfuncs]
    hashfuncopeners += [(name + "-z", with_ztransform_preprocess(func))
                        for name, func in hashfuncs if name != "colorhash"]
    output_hashes = []
    for path in files:
        output_hashes = [
            str(hashfuncopener(path))
            for name, hashfuncopener in hashfuncopeners
        ]
    return output_hashes


def hash(paths, hash_type=1):
    if isinstance(paths, list):
        return [
            str(image_loader(hashfuncs[hash_type][1])(path)) for path in paths
        ]
    return str(image_loader(hashfuncs[hash_type][1])(paths))


if __name__ == "__main__":
    print("\n", hashes())

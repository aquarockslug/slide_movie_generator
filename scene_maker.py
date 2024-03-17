import scene_hasher

# hashes: dict = file --> lambda: hash(file)
 
# scene creator manual and automatic
# move movie_data into main 

def create_scenes(files):
    print(files)
    hashes = [scene_hasher.hash(file) for file in files]
    print(hashes[1])

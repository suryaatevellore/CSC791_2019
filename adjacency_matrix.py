from pathlib import Path

data_folder = Path("/home/RND-TOOL/rnd_lab/")

FILENAME = 'connectivity_map.txt'
FILEPATH = data_folder / FILENAME

connections = {}
with open(FILEPATH, "r+"):


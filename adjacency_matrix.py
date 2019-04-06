from pathlib import Path


def create_connections(FILEPATH):

connections = {}
with open(FILEPATH, "r+"):


def main():
    data_folder = Path("/home/RND-TOOL/rnd_lab/")
    FILENAME = 'connectivity_map.txt'
    FILEPATH = data_folder / FILENAME
    create_connections(FILEPATH)


if __name__=='__main__':
    main()


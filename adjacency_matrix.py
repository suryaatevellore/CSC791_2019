from pathlib import Path


def create_connections(FILEPATH):
    connections = {}
    with open(FILEPATH, "r+") as file:
        for line in file:
            args = line.strip().split()
            if len(args)>5:
                # arguments in the form of (destination, local port, dest port)
                if args[0] in connections.keys():
                    connections[args[0]].append((args[4], args[1], args[5]))
                else:
                    connections[args[0]] = []

    return connections

def create_neighbors():
    data_folder = Path("/home/RND-TOOL/rnd_lab/")
    FILENAME = 'connectivity_map.txt'
    FILEPATH = data_folder / FILENAME
    connections = create_connections(FILEPATH)


if __name__=='__main__':
    create_neighbors()


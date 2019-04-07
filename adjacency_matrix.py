from pathlib import Path
0, 1, 2, 3, 4, 5, 6
['S3', 'eth71', '(192.168.15.1/24)', '---', 'L3', 'eth31', '(192.168.15.2/24)']


def create_connections(FILEPATH):
    connections = {}
    with open(FILEPATH, "r+") as file:
        for line in file:
            args = line.strip().split()
            if len(args) > 5:
                # arguments in the form of (destination, localip, local port, destip, dest port)
                if args[0] in connections.keys():
                    connections[args[0]].append((args[4], args[2], args[1], args[6], args[5]))
                else:
                    connections[args[0]] = []

    return connections


def create_neighbors():
    data_folder = Path("/home/RND-TOOL/rnd_lab/")
    FILENAME = 'connectivity_map.txt'
    FILEPATH = data_folder / FILENAME
    connections = create_connections(FILEPATH)

    return connections


def filter_by(connections, key, device):
    """
        returns the attributes as per specified key
    """
    result = []
    if key=='IP':
        if device[0]=='S':
            for source, attrs in connections.items():
                if source[0]=='S':
                        result.append(attrs[0][1][1:(len(attrs)-1)])
        elif device[0]=='L':
             for source, attrs in connections.items():
                if source[0]=='L':
                    result.append(attrs[0][1][1:(len(attrs)-1)])

    return result


if __name__=='__main__':
    create_neighbors()



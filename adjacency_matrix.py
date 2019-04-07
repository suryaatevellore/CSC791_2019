from pathlib import Path
# 0, 1, 2, 3, 4, 5, 6
# ['S3', 'eth71', '(192.168.15.1/24)', '---', 'L3', 'eth31', '(192.168.15.2/24)']

# source, localport, localip, --, dst, dstport, dstip
# 0         1           2       3  4     5       6

def create_connections(FILEPATH):
    connections = {}
    with open(FILEPATH, "r+") as file:
        for line in file:
            args = line.strip().split()
            if len(args) > 5:
                # initialise for spines
                if args[0] in connections.keys():
                    connections[args[0]].append((args[4], args[2], args[1], args[6], args[5]))
                else:
                    connections[args[0]] = []
                    connections[args[0]].append((args[4], args[2], args[1], args[6], args[5]))

                if args[4] in connections.keys():
                    connections[args[4]].append((args[0], args[6], args[5], args[2], args[1]))
                else:
                    connections[args[4]] = []
                    connections[args[4]].append((args[0], args[6], args[5], args[2], args[1]))

    #print("=======================connections with ip =================")
    #print(filter_by(connections['L1'], 'IP', 'L1'))
    #print("====================connections===================")
    #print(connections['L1'])
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
            for attrs in connections:
                if attrs[0][0]=='L':
                        _temp = attrs[1]
                        result.append(_temp[1:(len(_temp)-1)])
        elif device[0]=='L':
             for attrs in connections:
                print(f"{attrs[0][0]}, {attrs[1]}")
                if attrs[0][0]=='S':
                     _temp = attrs[1]
                     result.append(_temp[1:(len(_temp)-1)])

    return result


if __name__=='__main__':
    create_neighbors()



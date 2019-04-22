from pathlib import Path


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

    # print("=======================connections with ip =================")
    # print(filter_by(connections['L1'], 'IP', 'L1'))
    # print("====================connections===================")
    # print(connections['RR1'])
    return connections


def create_neighbors():
    data_folder = Path("/home/RND-TOOL/rnd_lab/")
    FILENAME = 'connectivity_map.txt'
    FILEPATH = data_folder / FILENAME
    connections = create_connections(FILEPATH)

    return connections


def filter_by(connections, key, device):
    """
        returns list, the attributes as per specified key
    """
    print(f"{connections} recieved for {device}")
    result = []
    if key == 'IP':
        if 'RR' in device:
            for attrs in connections:
                if attrs[0][0] in ['L', 'S']:
                    _temp = attrs[1]
                    result.append(_temp[1:(len(_temp) - 1)])
        elif device[0] == 'S':
            for attrs in connections:
                # spines can connect to only RR and leaves
                if attrs[0][0] == 'L' or 'RR' in attrs[0]:
                        _temp = attrs[1]
                        result.append(_temp[1:(len(_temp) - 1)])
        elif device[0] == 'L':
            for attrs in connections:
                # leaves connect to only spine and RR
                if attrs[0][0] == 'S' or 'RR' in attrs[0]:
                    _temp = attrs[1]
                    result.append(_temp[1:(len(_temp) - 1)])

    return result


def get_host_mapping(connections, hosts):
    # hostname, localport, bridge_id
    ports = {}
    print(f"Recieved {hosts} connectivity")
    for host in hosts:
        for connection in connections:
            print(f"Testing {connection[0]} aganst {host} ")
            if connection[0] == host:
                ip = ''.join(connection[1])
                ip = ip[1:-1]
                print(ip)
                ports[connection[2]] = ip

    return ports


def match_pattern_matrix(pattern):
    data_folder = Path("/home/RND-TOOL/rnd_lab/scripts/")
    FILENAME = 'connectivitymat.txt'
    FILEPATH = data_folder / FILENAME
    _temp = set()
    with open(FILEPATH) as file:
        data = file.readline().strip()  # first line of adjacency matrix
        data = data.split()             # currently split by spaces
        for entry in data:
            if pattern in entry:
                _temp.add(entry)

    if _temp:
        print(_temp)
        return list(_temp)
    else:
        return None


if __name__ == '__main__':
    create_neighbors()

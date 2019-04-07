from pathlib import Path
# 0, 1, 2, 3, 4, 5, 6
# ['S3', 'eth71', '(192.168.15.1/24)', '---', 'L3', 'eth31', '(192.168.15.2/24)']

# source, localport, localip, --, dst, dstport, dstip
# 0         1           2       3  4     5       6


# dst, localip, localport, dstip, dstport

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


def host_mapping(connections, bridges_list=None, number_of_tenants=1):
    # hostname, localport, bridge_id
    hosts_ports = []
    index = 0
    number_of_bridges = len(bridges_list)
    for entry in connections:
        if entry[0][0] == 'H':
            hosts_ports.append((entry[0], entry[2], bridges_list[index]))
            index += 1
            if index == (number_of_bridges):
                index = 0

    return hosts_ports


def match_pattern_matrix(pattern):
    data_folder = Path("/home/RND-TOOL/rnd_lab/scripts/")
    FILENAME = 'connectivitymat.txt'
    FILEPATH = data_folder / FILENAME
    _temp = set()
    with open(FILEPATH) as file:
        data = file.readlines()
        for item in data:
            # handles that readlines would give back full lines
            item = item.split()
            for entry in item:
                if pattern in entry:
                    _temp.add(entry)

    if _temp:
        return list(_temp)
    else:
        return None


if __name__ == '__main__':
    create_neighbors()

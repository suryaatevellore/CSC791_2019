import sys
from common_functions import get_docker_ips
from adjacency_matrix import match_pattern_matrix


def handle_device(pattern):
    if 'spine' in pattern:
        result = match_pattern_matrix('S')
    elif 'lea' in pattern:
        result = match_pattern_matrix('L')
    elif 'RR' in pattern:
        result = match_pattern_matrix('RR')

    return result


def get_RR_IPs(RR):
    RR_ip = get_docker_ips(RR)
    return RR_ip


def tenant_leaf_mapping():
    data_folder = Path("/home/RND-TOOL/rnd_lab/scripts/")
    FILENAME = 'tenant.txt'
    FILEPATH = data_folder / FILENAME
    with open(FILEPATH, "r+") as file:
        data = file.read()
        data = data.strip.split(",")
        for info in data:
            results.append(info[1:len(info)-1])

    print(results)

    return results



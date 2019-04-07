import sys
from common_functions import get_docker_ips
from adjacency_matrix import match_pattern_matrix


def handle_RR():
    RR_list = match_pattern_matrix('RR')

    if RR_list:
        return RR_list
    else:
        return None


def get_RR_IPs(RR):
    RR_ip = get_docker_ips(RR)
    return RR_ip

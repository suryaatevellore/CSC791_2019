import sys
import subprocess
from common_functions import get_docker_ips


def handle_RR(device_list, index):
    RR_choice = input("Do you need RR's in your topology(y/n): ")
    recommended_RR = len(device_list) // 2
    if RR_choice == 'y' or RR_choice == 'Y':
        number_of_RRs = int(input(f"How many RRs do you want in your topology(recommended is {recommended_RR}) ?: "))
        return ['RR' + str(i) for i in range(1, number_of_RRs)]
    elif RR_choice == 'n' or RR_choice == 'N':
        return None
    else:
        print("Incorrect choice")
        sys.exit(1)


def get_RR_IPs(RR):
    RR_ip = get_docker_ips(RR)
    return RR_ip

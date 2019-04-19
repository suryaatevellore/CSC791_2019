from ssh_config import config_via_ssh
from docker_cmd_config import common_terminal_config
from common_functions import create_loopbacks, get_docker_ips
from helper_functions import handle_RR, get_RR_IPs


def main():
    spines = ['S' + str(i) for i in range(1, 5)]
    leaves = ['L' + str(i) for i in range(1, 7)]
    index = 1

    devices_list = spines + leaves
    device_loopbacks, index = create_loopbacks(devices_list, index)
    RR = handle_RR()
    device_ip = get_docker_ips(devices_list)
    common_terminal_config(devices_list, device_loopbacks)
    if RR:
        RR_loopbacks, index = create_loopbacks(RR, index)
        common_terminal_config(RR, RR_loopbacks)
        RR_IP = get_RR_IPs(RR)
        combined_loopbacks = {**RR_loopbacks, **device_loopbacks}
        # configure ospf and bgp on spines and leaves
        config_via_ssh(device_ip, combined_loopbacks, True, True, True)
        RR_IP = get_RR_IPs(RR)
        # configure ospf for RRs
        config_via_ssh(RR_IP, combined_loopbacks, False, True, False)
        # configure BGP for RRs
        config_via_ssh(RR_IP, combined_loopbacks, False, False, True)
    else:
        config_via_ssh(device_ip, device_loopbacks, False, True, True)


if __name__ == "__main__":
    main()

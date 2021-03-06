import sys
from ssh_config import config_via_ssh
from common_functions import create_loopbacks, get_docker_ips, handle_device, get_RR_IPs, tenant_leaf_mapping


def main():
    spines = handle_device('spine')
    if not spines:
        print("Unable to extract spine information from adjacency matrix. Device names should start with S")
        sys.exit(1)

    leaves = handle_device('leaves')
    if not leaves:
         print("Unable to extract spine information from adjacency matrix. Device names should start with L")
         sys.exit(1)

    # Maintain the order in device list
    spines = sorted(spines)
    leaves = sorted(leaves)
    index = 1 # global counter for loopback indexes
    devices_list = spines + leaves
    device_loopbacks, index = create_loopbacks(devices_list, index)
    # If RRs are not specified in the adjacency matrix, a random spine is chosen as the RR
    RR = handle_device('RR')
    device_ip = get_docker_ips(devices_list)
    # common_terminal_config(devices_list, device_loopbacks)
    if RR:
        RR_loopbacks, index = create_loopbacks(RR, index)
        # common_terminal_config(RR, RR_loopbacks)
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

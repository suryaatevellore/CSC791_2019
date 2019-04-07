import os
import subprocess
from adjacency_matrix import create_neighbors, host_mapping
import time


def common_terminal_config(device_list, Loopbacks=None, device_ip=None):
    print("Received list and loopbacks {device_list} {Loopbacks}")
    for device in device_list:
        print(f"Configuring loopbacks on {device}")
        os.system(f"sudo docker exec -d {device} bash -c 'apt-get install bridge-utils -y'")
        os.system(f"sudo docker exec -d {device} bash -c 'ip addr add {Loopbacks[device]}/32 dev lo'")
        time.sleep(0.5)

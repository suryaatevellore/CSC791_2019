import os
import subprocess
from adjacency_matrix import create_neighbors


bridge_config = """
'brctl addbr t1',
'brctl addbr t2',
'ip link set up dev t1',
'ip link set up dev t2',
'brctl stp t1 off',
'brctl stp t2 off',
'brctl addif t1 tun1',
'brctl addif t2 tun2',
'ip link set up dev tun1',
'ip link set up dev tun2'
"""


def common_terminal_config(device_list, Loopbacks=None, device_ip=None):
    global bridge_config
    bridge_config = bridge_config.split(',')
    for device in device_list:
        print(f"Configuring loopbacks on {device}")
        os.system(f"sudo docker exec -d {device} bash -c 'apt-get install bridge-utils -y'")
        os.system(f"sudo docker exec -d {device} bash -c 'ip addr add {Loopbacks[device]}/32 dev lo'")
        for line in bridge_config:
            if device[0]=='L':
                print("Configuring bridges and tunnels on {device}")
                os.system(f"sudo docker exec -d {device} bash -c 'ip link add tun1 type vxlan id 100 dstport 4789 local {Loopbacks[device]} nolearning'")
                os.system(f"sudo docker exec -d {device} bash -c 'ip link add tun2 type vxlan id 200 dstport 4789 local {Loopbacks[device]} nolearning'")
                completed = subprocess.run(f"sudo docker exec -d {device} /bin/bash -c {line.strip()}", shell=True, stdout=subprocess.PIPE)
                # add host interfaces to bridges
                # if host number is odd, add to bridge1
                # if host number is even, add to bridge2
                connections = create_neighbors()
                hosts = host_mapping(connections[device])
                for entry in hosts:
                    completed = subprocess.run(f"sudo docker exec -d {device} 'brctl addif {entry[2]} {entry[1]}", shell=True, stdout=subprocess.PIPE)
                    print(completed.stdout.decode('utf-8').strip())


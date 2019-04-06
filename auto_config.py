import paramiko
import subprocess
import os
from ssh_config import config_via_ssh

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


def create_loopbacks(device_list):
    Loopbacks = {}
    for index, element in enumerate(device_list):
        Loopbacks[element] = (str(index+1)+'.')*3 + str(index+1)

    return Loopbacks


def get_docker_ips(device_list):
    #All leaves docker ips
    device_ip = {}
    for device in device_list:
        completed = subprocess.run("sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + device, shell=True, stdout=subprocess.PIPE)
        leaves_ip[device] = completed.stdout.decode('utf-8').strip()

    return device_ip


def common_terminal_config(device_list, Loopbacks=None, device_ip=None):
    bridge_config = bridge_config.split(',')
    for device in device_list:
        os.system("apt-get install bridge-utils -y")
        os.system(f"sudo docker exec -d {device} bash -c 'ip addr add {Loopbacks[device]}/32 dev lo'")
        os.system(f"ip link add tun1 type vxlan id 100 dstport 4789 local {Loopbacks[device]} nolearning")
        os.system(f"ip link add tun1 type vxlan id 200 dstport 4789 local {Loopbackleaf]} nolearning")
        for line in bridge_config:
            os.system(f"sudo docker exec -d {device} bash -c {line}")


def main():
    spines = ['S' + str(i) for i in range(1, 5)]
    leaves = ['L' + str(i) for i in range(1, 7)]
    hosts = ['H' + str(i) for i in range(1, 12)]

    all_devices = spines + leaves + hosts
    all_devices_index = {element:index for element, index in enumerate(all_devices)}
    devices_list = spines + leaves
    device_loopbacks = create_loopbacks(devices_list)
    device_ip = get_docker_ips(devices_list)
    common_terminal_config(devices_list, device_loopbacks)


if __name__=="__main__":
    main()

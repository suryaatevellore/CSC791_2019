import paramiko
import subprocess
import os
from ssh_config import config_via_ssh
from docker_cmd_config import common_terminal_config


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
        device_ip[device] = completed.stdout.decode('utf-8').strip()

    return device_ip


def main():
    spines = ['S' + str(i) for i in range(1, 5)]
    leaves = ['L' + str(i) for i in range(1, 7)]
    hosts = ['H' + str(i) for i in range(1, 12)]

    all_devices = spines + leaves + hosts
    all_devices_index = {element:index for element, index in enumerate(all_devices)}
    devices_list = spines + leaves
    device_loopbacks = create_loopbacks(devices_list)
    device_ip = get_docker_ips(devices_list)
    #common_terminal_config(devices_list, device_loopbacks)
    config_via_ssh(device_ip, device_loopbacks)


if __name__=="__main__":
    main()

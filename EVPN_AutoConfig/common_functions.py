import subprocess
import time
import re
import sys
from pathlib import Path
from adjacency_matrix import match_pattern_matrix, getPATH
from collections import OrderedDict



def create_loopbacks(device_list, index):
    Loopbacks = OrderedDict()
    for element in device_list:
        Loopbacks[element] = ((str(index) + '.') * 3) + str(index)
        index += 1

    print(f"Loopbacks created {Loopbacks}")
    return Loopbacks, index


def get_docker_ips(device_list):
    # All leaves docker ips
    device_ip = {}
    for device in device_list:
        completed = subprocess.run("sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + device, shell=True, stdout=subprocess.PIPE)
        device_ip[device] = completed.stdout.decode('utf-8').strip()

    return device_ip


def displayLine():
    print("="*30)


def check_prompt(initial_prompt):
    router_prompt = initial_prompt.decode('utf-8')
    searchObj = re.search( r'Welcome to Ubuntu', router_prompt, re.M|re.I)
    if searchObj:
        # 1 is server prompt
        print('Welcome to ubuntu found')
        return 1
    else:
        # 0 is router prompt
        return 0


def set_prompt(client, initial_prompt, prompt_type):
    _local_prompt = check_prompt(initial_prompt)
    if(prompt_type == 'router'):
        if(_local_prompt == 1):
            # prompt is server
            client.send('\rvtysh\r')
            time.sleep(0.5)
            output = client.recv(1000)
            print(output)
        else:
            return

    elif(prompt_type == 'server'):
        if(_local_prompt == 0):
            # prompt is router
            client.send('\rend\r')
            time.sleep(0.5)
            client.send("exit\r")
            output = client.recv(1000)
        else:
            return


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
    mapping = {}
    DIRECTORY_PATH = getPATH()
    data_folder = Path(DIRECTORY_PATH + "scripts/")
    FILENAME = 'tenant.txt'
    FILEPATH = data_folder / FILENAME
    # leaf_regex = r"{([A-Za-z\d]+-[A-Za-z]\d{1,4})?}"
    leaf_regex = r"{(Leaf\d-L\d{1,2})?}"
    tenant_regex = r"[a-zA-Z\d]+-[A-Za-z]\d{.*?}"
    with open(FILEPATH, "r+") as file:
        for line in file:
            # print(line.strip())
            #leaf = re.findall(leaf_regex, line)
            m = re.match(leaf_regex, line)
            leaf = m.group(1)
            # print(leaf)
            if not leaf:
                print("Either leaf names are not specified, or their formatting is incorrect")
                sys.exit(1)
            l_name, l_id = leaf.strip().split("-")
            mapping[l_id] = {}
            tenants = re.findall(tenant_regex, line)
            # print(tenants)
            if not tenants:
                print("Either tenant names are not specified, or their formatting is incorrect")
                sys.exit(1)
            for tenant in tenants:
                tenant = tenant[tenant.index("-")+1:]
                t_id, remaining = tenant.split("{")
                remaining = remaining[:-1]           # gets rid of the last }
                hosts = remaining.split(",")
                mapping[l_id][t_id] = hosts

    return mapping



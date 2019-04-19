import subprocess
import time
import re


def create_loopbacks(device_list, index):
    Loopbacks = {}
    for element in device_list:
        Loopbacks[element] = ((str(index) + '.') * 3) + str(index)
        index += 1

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
    print(f"Checking for prompt {initial_prompt}")
    router_prompt = initial_prompt.decode('utf-8')
    searchObj = re.search( r'Welcome to Ubuntu', router_prompt, re.M|re.I)
    if searchObj:
        # 1 is server prompt
        print("Welcome to Ubuntu found")
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
            print(f"prompt {output}")
        else:
            return

    elif(prompt_type == 'server'):
        if(_local_prompt == 0):
            # prompt is router
            client.send('\rend\r')
            time.sleep(0.5)
            client.send("exit\r")
            output = client.recv(1000)
            print(f"prompt {output}")
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
    results = []
    data_folder = Path("/home/RND-TOOL/rnd_lab/scripts/")
    FILENAME = 'tenant.txt'
    FILEPATH = data_folder / FILENAME
    regex = ur"(.*),\s(.*}),\s(.*})"
    line = "President [P] Barack Obama [/P] met Microsoft founder [P] Bill Gates [/P], yesterday."
    person = re.findall(pattern, line)
    with open(FILEPATH, "r+") as file:
        data = file.read()
        data = re.findall(pattern, data)
    print(data)


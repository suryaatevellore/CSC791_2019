import subprocess
import time

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


def prompt_check(client):
    client.send("\r")
    time.sleep(0.5)
    output = client.recv(1000)
    print(f"Checking for prompt {output}")
    router_prompt = output.decode('utf-8')
    if 'root@' in router_prompt:
        return 'server'
    
    return 'router'

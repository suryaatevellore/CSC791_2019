import paramiko
import subprocess
spines = ['S'+str(i) for i in range(1, 5)]
leaves = ['L'+str(i) for i in range(1, 7)]
hosts = ['H'+str(i) for i in range(1, 12)]

all_devices = spines + leaves + hosts
all_devices_index = {element:index for element, index in enumerate(all_devices)}

#Loopbacks
Loopbacks = {}
for index, element in enumerate(leaves):
    Loopbacks[element] = (str(index+1)+'.')*3 + str(index+1)

#All leaves docker ips
leaves_ip = {}
for leaf in leaves:
    completed = subprocess.run("sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + leaf, shell=True, stdout=subprocess.PIPE)
    leaves_ip[leaf] = completed.stdout.decode('utf-8').strip()

# Now ssh
loopback_config = [
  f'ip route add {Loopbacks[leaf]}/32 dev lo'
]

for leaf, ip in leaves_ip.items():
    ssh = paramiko.SSHClient()
    ssh.connect(ip, username=root, password=root)
    for cmd_to_execute in loopback_config:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
        print(ssh_stdout)

import time
import paramiko
from routing_functions import configure_bgp, configure_ospf

def config_via_ssh(device_list, loopbacks=None, username='root', password='root'):

    for device, ip in device_list.items():
        print("Creating ssh connection")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        print(f"Interactive SSH session established to {device}")
        client = ssh.invoke_shell()
        # configure BGP
        configure_bgp(client, loopbacks)

        #configure ospf

        ospf_ips = filter_by(connections, 'IP', device)
        configure_ospf(client, ospf_ips, loopbacks[device])




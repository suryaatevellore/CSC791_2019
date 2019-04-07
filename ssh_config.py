import time
import paramiko
from routing_functions import configure_bgp, configure_ospf
from adjacency_matrix import filter_by, create_neighbors


def config_via_ssh(device_list, loopbacks=None, username='root', password='root'):
        
    print(f"Current device list")
    for device, ip in device_list.items():
        print("Creating ssh connection")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        print(f"Interactive SSH session established to {device}")
        client = ssh.invoke_shell()

        #configure ospf
        connections = create_neighbors()
        print(f"started ospf configuration for {device}")
        ospf_ips = filter_by(connections[device], 'IP', device)
        configure_ospf(client, ospf_ips, loopbacks[device])
        print(f"Finished ospf configuration for {device}")

        # configure BGP
        loopback_bgp = {}
        if device[0] == 'S':
            for router, loopback in loopbacks.items():
                if(router[0]=='L'):
                    loopback_bgp[router] = loopback
            
        elif device[0] == 'L':
            for router, loopback in loopbacks.items():
                if(router[0]=='S'):
                    loopback_bgp[router] = loopback
        configure_bgp(client, loopback_bgp, device)

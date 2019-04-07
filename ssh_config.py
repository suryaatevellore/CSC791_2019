import time
import paramiko
from routing_functions import configure_bgp, configure_ospf, configure_bridges
from adjacency_matrix import filter_by
from adjacency_matrix import create_neighbors

bridge_config = [
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
]


def config_via_ssh(device_list, loopbacks=None, username='root', password='root'):
    global bridge_config

    for device, ip in device_list.items():
        print("Creating ssh connection")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        print(f"Interactive SSH session established to {device}")
        client = ssh.invoke_shell()
        connections = create_neighbors()

        # configure_bridges
        if device[0] == 'L':
            print(f"Configure bridge on {device}")
            configure_bridges(client, bridge_config, connections[device], loopbacks[device], device)
        elif device[0] == 'S':
            print("No need for bridges or tunnels on spines")


        #configure ospf

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

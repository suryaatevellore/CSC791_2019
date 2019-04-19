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


def config_via_ssh(device_list, loopbacks, RR_flag=False, ospf_flag=False, bgp_flag=False, username='root', password='root'):
    """
        device_list: dictionary as device:IP
        loopbacks  : dictionary as device:LoopbackIP
        RR_flag    : State wheather RRs are present or not
        username   : SSH username
        password   : SSH password
    """
    global bridge_config
    for device, ip in device_list.items():
        print("Creating ssh connection")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        print(f"Interactive SSH session established to {device}")
        client = ssh.invoke_shell()
        connections = create_neighbors()
        # ==========================================================
        # configure_bridges only for leaves
        # ==========================================================
        if device[0] == 'L':
            print(f"Configure bridge on {device}")
            configure_bridges(client, bridge_config, connections[device], loopbacks[device], device)
        else:
            print("No need for bridges or tunnels on spines/RRs")

        # ==========================================================
        # configure ospf for all devices
        # ==========================================================
        if ospf_flag:
            print(f"started ospf configuration for {device}")
            ospf_ips = filter_by(connections[device], 'IP', device)
            print(f"Connected IPs for {device} are {ospf_ips}")
            configure_ospf(client, ospf_ips, loopbacks[device], device)
            print(f"Finished ospf configuration for {device}")

        # ==========================================================
        # configure BGP
        # if RR_flag is set, then RRs are present in the topology
        # ==========================================================
        if bgp_flag:
            if(RR_flag):
                # loopbacks contains loopbacks of RRs
                loopback_bgp = {}
                for router, loopback in loopbacks.items():
                    if 'RR' in router:
                        loopback_bgp[router] = loopback
            else:
                # No RRs present, each leaf peers with each spine only and vice versa
                loopback_bgp = {}
                if 'RR' in device:
                    for router, loopback in loopbacks.items():
                        if(router[0] in ['L', 'S']):
                            loopback_bgp[router] = loopback
                elif device[0] == 'S':
                    for router, loopback in loopbacks.items():
                        if(router[0]=='L'):
                            loopback_bgp[router] = loopback

                elif device[0] == 'L':
                    for router, loopback in loopbacks.items():
                        if(router[0]=='S'):
                            loopback_bgp[router] = loopback
            print(f"For {device}, neighbors are {loopback_bgp}")
            configure_bgp(client, loopback_bgp, device)

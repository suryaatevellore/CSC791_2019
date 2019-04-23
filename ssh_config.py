import time
import paramiko
from routing_functions import configure_bgp, configure_ospf, configure_loopbacks, configure_overlay,install_bridge_utils, get_vxlan_id, get_tenants, configure_bridges
from adjacency_matrix import filter_by
from adjacency_matrix import create_neighbors
from common_functions import displayLine, set_prompt, tenant_leaf_mapping


def config_via_ssh(device_list, loopbacks, RR_flag=False, ospf_flag=False, bgp_flag=False, username='root', password='root'):
    """
        device_list: dictionary as device:IP
        loopbacks  : dictionary as device:LoopbackIP
        RR_flag    : State wheather RRs are present or not
        username   : SSH username
        password   : SSH password
    """
    t2l_mapping = tenant_leaf_mapping()
    connections = create_neighbors()
    for device, ip in device_list.items():
        print("=================================")
        print(f"Starting configuration for {device}")
        print("=================================")
        print("Creating ssh connection")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        print(f"Interactive SSH session established to {device}")
        client = ssh.invoke_shell()
        time.sleep(0.5)
        initial_prompt = client.recv(1000)
        time.sleep(0.5)
        tenants = get_tenants(t2l_mapping)
        vx_id = get_vxlan_id(tenants)
        # ==========================================================
        # configure_loopbacks on device
        # ==========================================================
        configure_loopbacks(client, device, loopbacks[device])
        # ==========================================================
        # configure_bridges only for leaves
        # install bridge_utils too
        # ==========================================================
        if device[0] == 'L':
            # Will need to configure tunnels and bridges according to
            # the tenant mapping
            set_prompt(client, initial_prompt, 'server')
            time.sleep(3)
            if device in t2l_mapping.keys():
                install_bridge_utils(device)
                print("Installed bridge-utils on device")
                print(f"Configuring overlay on {device}")
                configure_overlay(client, t2l_mapping[device], vx_id, loopbacks[device], device, connections[device])
        else:
            print("No need for bridges or tunnels on spines/RRs")

        # ==========================================================
        # configure ospf for all devices
        # ==========================================================
        if ospf_flag:
            set_prompt(client, initial_prompt, 'router')
            print(f"started ospf configuration for {device}")
            ospf_ips = filter_by(connections[device], 'IP', device)
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
                # No RRs present, each leaf peers all other devices, but
                loopback_bgp = {}
                if 'RR' in device:
                    for router, loopback in loopbacks.items():
                        if(router[0] in ['L']):
                            loopback_bgp[router] = loopback
                elif device[0] == 'S':
                    for router, loopback in loopbacks.items():
                        if(router[0]=='L'):
                            loopback_bgp[router] = loopback

                elif device[0] == 'L':
                    for router, loopback in loopbacks.items():
                        if(router[0] in ['S', 'L']):
                            loopback_bgp[router] = loopback
            set_prompt(client, initial_prompt, 'router')
            configure_bgp(client, loopback_bgp, device)

        print("Closing SSH connection")
        client.close()


# def create_ssh_object():
#     try:



#     except socket.gaierror:

#     return client

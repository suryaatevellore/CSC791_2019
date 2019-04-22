import time
import os
from adjacency_matrix import get_host_mapping
from common_functions import displayLine, set_prompt


def configure_bgp(client, loopbacks, device):
    '''
        client    : Paramiko SSH shell object
        loopbacks : dictionary as BGPneighbor:loopbacks
        device    : device for which BGP is being configured
    '''
    print(f"started bgp configuration for {device}")
    client.send("configure t\r")
    time.sleep(0.5)
    client.send("router bgp 100\r")
    time.sleep(0.5)
    for item, loopback in loopbacks.items():
        if item != device:
            client.send(f"neighbor {loopback} remote-as 100\r")
            time.sleep(0.5)
            client.send(f"neighbor {loopback} update-source lo\r")
            time.sleep(0.5)
    client.send("address-family l2vpn evpn\r")
    time.sleep(0.5)
    for item, loopback in loopbacks.items():
        if item != device:
            client.send(f"neighbor {loopback} activate\r")
            time.sleep(0.5)
    client.send('advertise-all-vni\r')
    time.sleep(0.5)


def configure_ospf(client, neighbor_IP, loopback, device):
    """
        Configure OSPF on the devices

    """
    client.send("configure t\r")
    time.sleep(0.5)
    client.send("router ospf\r")
    for ip_mask in neighbor_IP:
        client.send(f"network {ip_mask} area 0\r")
        time.sleep(0.5)
        client.send(f"network {loopback}/32 area 0\r")
        time.sleep(0.5)
        client.send("passive-interface lo\r")
        time.sleep(0.5)
    client.send("end")
    time.sleep(0.5)


def configure_overlay(client, t2l_mapping, vx_id, loopback, device, connections):
    """
        client: Paramiko object for device
        t2l_mapping : Tenant and hosts attached to device
        vx_id : Global tenant to VXLAN ID mapping
        loopback : loopback of device
        device : device name
        connections : What is this device connected to and how ?
    """

    # Steps
    # configure the bridge
    # bring the bridge interface up
    # configure the tunnel
    # bring the tunnel interface up
    # add the tunnel interface to the bridge
    # configure the host ports
    # remove ip from the host ports

    bridge_names = {tenant:'BR'+str(index+1) for index,tenant in enumerate(t2l_mapping.keys())}
    for t_name, hosts in t2l_mapping.items():
        tunnel_name = get_tunnel_name(bridge_names[t_name])
        host_mapping = get_host_mapping(connections, hosts)
        client.send('\r\r')
        time.sleep(0.5)
        client.send(f"brctl addbr {bridge_names[t_name]}\r")
        time.sleep(0.5)
        client.send(f"ip link set up dev {bridge_names[t_name]}\r")
        time.sleep(0.5)
        client.send(f"brctl stp {bridge_names[t_name]} off\r")
        time.sleep(0.5)
        client.send(f"ip link add {tunnel_name} type vxlan id {vx_id[t_name]} dstport 4789 local {loopback} nolearning\r")
        time.sleep(0.5)
        client.send(f"ip link set {tunnel_name} up\r")
        time.sleep(0.5)
        client.send(f"brctl addif {bridge_names[t_name]} {tunnel_name}\r")
        time.sleep(0.5)
        for switch_port, switch_ip in host_mapping.items():
            client.send(f"brctl addif {bridge_names[t_name]} {switch_port}\r ")
            time.sleep(0.5)
            client.send(f"ip addr del {switch_ip} dev {switch_port}\r")
            time.sleep(0.5)
        output = client.recv(1000)
        print(f"Bridges configuration {output}")


def get_vxlan_id(tenants, index=10):
    return {value: index+key for key, value in enumerate(tenants)}


def get_tunnel_name(bridge):
    return 'tun' + bridge[-1]


def get_tenants(t2l_mapping):
    tenant_set = set()
    for leaf, tenant_info in t2l_mapping.items():
        for t_name in tenant_info.keys():
            tenant_set.add(t_name)

    return tenant_set


def install_bridge_utils(device):
    os.system(f"sudo docker exec -d {device} bash -c 'apt-get install bridge-utils -y'")


def configure_loopbacks(client, device, loopback):
    print(f"Configure {loopback} as {device} loopback")
    client.send(f"ip addr add {loopback}/32 dev lo\r")
    time.sleep(0.5)

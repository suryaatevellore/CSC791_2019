import time
from adjacency_matrix import host_mapping
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


ip link add t1ns1 type vxlan id 100 dstport 4789 local 1.1.1.1


def configure_overlay(client, t2l_mapping, vx_id, loopback, device):
    # Bridges names are equal to

    # Steps
    # Find bridge names. has to be one per tenant
    # set bridge interfaces up
    # attach hosts to bridges
    # configure tunnels and attach to bridges

    # get all the tenants in this device
    bridges = t2l_mapping.keys()
    host_mapping(connections, bridges)
    for t_name, hosts in t2l_mapping.items():



    for bridge in bridges:
        client.send(f"brctl addbr {bridge}\r")
        time.sleep(0.5)
        client.send(f"ip link set up dev {bridge}\r")
        time.sleep(0.5)
        client.send(f"brctl stp {bridge} off\r")
        time.sleep(0.5)
        output = client.recv(1000)
        print(f"Bridges configuration {output}")

    """hosts = host_mapping(connections, bridges_list)
    print(f"Host directory {hosts}")
    for entry in hosts:
        client.send(f"brctl addif {entry[2]} {entry[1]}\r")
        time.sleep(0.5)
        output = client.recv(1000)
        print(output)
        print("Configuring client interfaces on bridges")
    """

def get_vxlan_id(tenants, index=10):
    return {(value:index+key)for key, value in enumerate(tenants)}

def get_tunnels(bridges):
    return ['tun'+str(index) for index in range(len(bridges))]

def configure_tunnels(client, tenant_mapping, loopback, device):
    # each leaf will have different configuration

def get_tenants(t2l_mapping):
    tenant_set = set()
    for leaf, tenant_info in t2l_mapping.items():
        for t_name in tenant_info.keys():
            tenant_set.add(t_name)

    return tenant_set

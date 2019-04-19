import time
from adjacency_matrix import host_mapping
from common_functions import displayLine, prompt_check


def configure_bgp(client, loopbacks, device):
    '''
        client    : Paramiko SSH shell object
        loopbacks : dictionary as BGPneighbor:loopbacks
        device    : device for which BGP is being configured
    '''
    set_prompt(client, 'router')
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
    client.send('\rend\r')
    time.sleep(0.5)
    client.send("exit\r")
    time.sleep(5)
    output = client.recv(1000)
    print(output)
    print(f"Finished bgp configuration for {device}")


def configure_ospf(client, neighbor_IP, loopback, device):
    """
        Configure OSPF on the devices

    """
    set_prompt(client, 'router')
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
    client.send("exit\r")
    time.sleep(5)
    output = client.recv(1000)
    print(output)

def configure_bridges(client, bridge_config, connections, loopback, device):
    print("Configuring tunnels first")
    client.send("\r")
    time.sleep(0.5)
    client.send(f"ip link add tun1 type vxlan id 100 dstport 4789 local {loopback} nolearning\r")
    time.sleep(0.5)
    output = client.recv(1000)
    print(f"First tunnel config {output}")
    client.send(f"ip link add tun2 type vxlan id 200 dstport 4789 local {loopback} nolearning\r")
    time.sleep(0.5)
    for line in bridge_config:
        print(f"Command being sent {line}")
        client.send(f"{line}\r")
        time.sleep(0.5)
        output = client.recv(1000);
        print(f"Bridge config: {output}")

    bridges_list = ['t1', 't2']
    hosts = host_mapping(connections, bridges_list)
    print(f"Host directory {hosts}")
    for entry in hosts:
        displayLine()
        print(f"Configuring {entry}, bridge {entry[2]}, interface {entry[1]} on {device}\r")
        displayLine()
        client.send(f"brctl addif {entry[2]} {entry[1]}\r")
        time.sleep(0.5)
        output = client.recv(1000)
        print(output)
        print("Configuring client interfaces on bridges")

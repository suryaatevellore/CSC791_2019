import time

def configure_bgp(client, loopbacks):
    client.send("vtysh\r")
    time.sleep(.5)
    client.send("configure t\r")
    time.sleep(0.5)
    client.send("router bgp 100\r")
    time.sleep(0.5)
    for item, loopback in loopbacks.items():
        if item!=device:
            client.send(f"neighbor {loopback} remote-as 100\r")
            time.sleep(0.5)
            client.send(f"neighbor {loopback} update-source lo\r")
            time.sleep(0.5)
    client.send("address-family l2vpn evpn\r")
    time.sleep(0.5)
    for item, loopback in loopbacks.items():
        if item!=device:
            client.send(f"neighbor {loopback} activate\r")
            time.sleep(0.5)
    client.send('advertise-all-vni\r')
    time.sleep(0.5)
    client.send('end\r')
    time.sleep(0.5)
    output = client.recv(1000)
    print(output)


def configure_ospf(client, neighbor_IP, loopback):
    client.send("vtysh\r")
    time.sleep(.5)
    client.send("configure t\r")
    time.sleep(0.5)
    client.send("router ospf\r")
    for ip_mask in neighbor_IP:
        client.send(f"network {ip_mask} area 0")
        time.sleep(0.5)
        client.send(f"network {loopback} area 0")
        time.sleep(0.5)
        client.send("passive-interface lo")
        time.sleep(0.5)
    client.send("end")
    time.sleep(0.5)
    output = client.recv(1000)
    print(output)





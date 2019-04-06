import time
import paramiko


def config_via_ssh(device_list, loopbacks=None, username='root', password='root'):

    for device, ip in device_list.items():
        print("Creating ssh connection")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        print(f"Interactive SSH session established to {device}")
        client = ssh.invoke_shell()
        # check if we are on the root of the correct system
        output = client.recv(1000)
        time.sleep(0.5)
        client.send("vtysh\r")
        time.sleep(.5)
        client.send("configure t\r")
        client.send("router bgp 100")
        for item, loopback in loopbacks.items():
            if item!=device:
                client.send(f"neighbor {loopback} remote-as 100")
                time.sleep(0.5)
                client.send(f"neighbor {loopback} update-source lo")
                time.sleep(0.5)
        client.send("address-family l2vpn evpn")
        time.sleep(0.5)
        for item, loopback in loopbacks.items():
            if item!=device:
                client.send(f"neighbor {loopback} activate")
                time.sleep(0.5)
        client.send('advertise-all-vni')

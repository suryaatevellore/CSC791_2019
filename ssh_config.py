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

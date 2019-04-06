import time
import paramiko


def config_via_ssh(device_list, username='root', password='root'):

    for device in device_list:
        print("Creating ssh connection")
        ssh = paramiko.SSHClient()
        ssh.connect(device, username=username, password=password)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Interactive SSH session established to {device}")
        client = ssh.invoke_shell()
        # check if we are on the root of the correct system
        output = client.recv(1000)
        print(output)
        if((f'root@{device}') in output):
            print("In the wrong device")
            break

        client.send("vtysh")
        time.sleep(.5)
        output = client.recv(1000)
        print(output)

import paramiko
import time

import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

class SSHConnection:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel = None

    def connect(self):
        self.client.connect(self.server, username=self.username, password=self.password)
        self.client.get_transport().set_keepalive(60)
        self.channel = self.client.invoke_shell()
        time.sleep(1)
        self.channel.recv(4096)  # clear initial output

    def send_command(self, command, sleep_time=1):
        self.channel.send(f'{command}\n'.encode())
        time.sleep(sleep_time)
        data = self.channel.recv(4096).decode()
        return data

    def close(self):
        self.client.close()

if __name__ == "__main__":
    ssh = SSHConnection("192.168.124.125", "pi", "pi")
    ssh.connect()
    print(ssh.send_command("ls"))
    ssh.send_command("mkdir aaa")
    ssh.send_command("ls -la")
    print(ssh.send_command("ls"))
    ssh.close()

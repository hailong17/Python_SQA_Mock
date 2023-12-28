import  connectSSH

sshRaspi = connectSSH.TelnetHostUtil
hostIp = "192.168.1.1."
hostPort = 23
appPath = "local/path/"
hostName = "ubuntu"
hostPasswd = "1"

if __name__ == "__main__":
    print('Delete device.tbl and config.def file ')
    sshRaspi.open_host_connection(hostIp, hostPort)
    sshRaspi.host_login(hostName, hostPasswd)
    sshRaspi.host_send('cd {}'.format(appPath), 2)
    sshRaspi.host_send('sudo rm device.tbl', 1)
    sshRaspi.host_send('sudo rm config.def', 1)
    result = sshRaspi.host_send('ls', 1)
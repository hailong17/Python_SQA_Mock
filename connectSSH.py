
import logging
import queue
import re
import threading
import time
from abc import abstractmethod
from typing import Any, Callable, Optional, Union, List, Pattern

class OTCIError(Exception):
    """Base class for OTCI Errors."""
    pass

class CommandError(OTCIError):
    """OTCI failed to execute a command."""

    def __init__(self, cmd: str, output: List[str]):
        self.__output = output
        super(CommandError, self).__init__("Command error while executing %r:\n%s\n" % (cmd, '\n'.join(output)))

    def error(self) -> str:
        return self.__output[-1]

class OtbrSshCommandRunner():

    def __init__(self, host, port, username, password, sudo=None, prefix = True):
        import paramiko

        self.__host     = host
        self.__port     = port
        self.__sudo     = sudo
        self.__username = username
        self.__password = password
        self.__prefix   = prefix
        self.__ssh      = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.__line_read_callback = None
        self.__maxByte = 327675

        print("\r\nConnect to host {} port {}".format(host, port))
        try:
            print("username:", username)
            print("password:", password)
            self.__ssh.connect(host,
                               port=port,
                               username=username,
                               password=password,
                               allow_agent=False,
                               look_for_keys=False)
        except paramiko.ssh_exception.AuthenticationException:
            if not password:
                self.__ssh.get_transport().auth_none(username)
            else:
                raise
        self.channel = self.__ssh.invoke_shell()
        self.channel.settimeout(10)

    def __repr__(self):
        return f'{self.__host}:{self.__port}'

    def execute_command(self, cmd: str, timeout: float) -> List[str]:

        if not self.__prefix:
            sh_cmd = f'{cmd}'
        else:
            sh_cmd = f'ot-ctl -- {cmd}'
        if self.__sudo:
            sh_cmd = 'sudo ' + sh_cmd
        print("\r\nsh_cmd: {}".format(sh_cmd))
        cmd_in, cmd_out, cmd_err = self.__ssh.exec_command(sh_cmd, timeout=int(timeout), bufsize=1024)
        err = cmd_err.read().decode('utf-8')
        if err:
            raise CommandError(cmd, [err])

        output = [l.rstrip('\r\n') for l in cmd_out.readlines()]

        if self.__line_read_callback is not None:
            for line in output:
                self.__line_read_callback(line)

        if cmd in ('reset', 'factoryreset'):
            self.wait(3)

        return output

    def send_cmd(self, cmd: str, timeout: float):
        try:
            recv_data = ''
            cmd_out   = ''
            print("\r\ncmd: {}".format(cmd))
            self.channel.send(cmd + "\n")
            time.sleep(timeout-1)
            recv_data =  self.channel.recv(self.__maxByte).decode('utf-8')
            cmd_out  += str(recv_data)
            print("cmd_out", cmd_out)
        except:
            print('Socket disconnected.')
            return ''

    def send_cmd_expect(self, cmd: str, expectStr: str, timeout: float, breakTime: float):
        print("\r\n[{}]cmd: {}".format(round(time.time(),2),cmd))
        recv_data   = ''
        cmd_out     = ''
        result      = False
        self.channel.send(cmd + "\n")
        startTime   = time.time()
        elapsedTime = 0
        while(timeout > time.time() - startTime):
            time.sleep(1)
            if self.channel.recv_ready():
                recv_data = self.channel.recv(self.__maxByte).decode('utf-8')
                cmd_out  += str(recv_data)
                if expectStr in recv_data:
                    # wait cmd finish
                    if breakTime:
                        time.sleep(breakTime)
                        # when there's no data coming in,
                        # recv will wait until the timeout set by setttimeout which is 10s now.
                        # So use recv_ready() as the condition to rx data to avoid waiting 10s more.
                        if self.channel.recv_ready():
                            try:
                                recv_data = self.channel.recv(self.__maxByte).decode('utf-8')
                                cmd_out  += str(recv_data)
                            except:
                                pass
                    result = True
                    break
        elapsedTime = time.time() - startTime
        # print("[{}] Cmd finish".format(round(time.time(),2)))
        return result, str(cmd_out), elapsedTime

    def recv(self, timeout: float):
        data_out    = ''
        startTime   = time.time()
        elapsedTime = 0
        while(timeout > elapsedTime):
            time.sleep(0.5)
            if self.channel.recv_ready():
                recv_data = self.channel.recv(self.__maxByte).decode('utf-8')
                data_out += str(recv_data)
            elapsedTime   = time.time() - startTime
        print("elapsedTime: ", elapsedTime)
        return str(data_out)

    def recv_expect(self, expectStr: str, timeout: float):
        result = False
        startTime = time.time()
        elapsedTime = 0
        recv_data = ''
        while(timeout > elapsedTime):
            time.sleep(0.5)
            if self.channel.recv_ready():
                data = self.channel.recv(self.__maxByte).decode('utf-8')
                recv_data += str(data)
                if expectStr in recv_data:
                    result = True
                    break
            elapsedTime = time.time() - startTime
        return result, str(recv_data), elapsedTime

    def close(self):
        self.__ssh.close()

    def wait(self, duration: float) -> List[str]:
        time.sleep(duration)
        return []

    def set_line_read_callback(self, callback: Optional[Callable[[str], Any]]):
        self.__line_read_callback = callback

    def reopen_connect(self):
        import paramiko
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.__ssh.connect(self.__host,
                               port=self.__port,
                               username=self.__username,
                               password=self.__password,
                               allow_agent=False,
                               look_for_keys=False)
        except paramiko.ssh_exception.AuthenticationException:
            if not self.__password:
                self.__ssh.get_transport().auth_none(self.__username)
            else:
                raise
        self.channel = self.__ssh.invoke_shell()
        self.channel.settimeout(10)

if __name__ == "__main__":
    host        = "192.168.124.125"
    port        = 22
    username    = "pi"
    password    = "pi"
    cmd_handler = OtbrSshCommandRunner(host, port, username, password) # ssh pi@192.168.124.125
    cmd_handler.send_cmd(cmd="ls -la", timeout=5)
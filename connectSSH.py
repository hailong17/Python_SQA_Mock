import telnetlib
class TelnetHostUtil(telnetlib.Telnet):
    def __init__(self, logService=None):
        telnetlib.Telnet.__init__(self)
        # Disable telnetlib debug printing.
        self.set_debuglevel(0)
        self._logService = logService
        self._hostName = None
        hostPort = None
        self._hostPasswd = None
        self._hostLoginName = None

    def update_host_info(self, hostName, hostPort, hostPasswd=None, hostLoginName=None):
        self._hostName = hostName
        hostPort = hostPort
        if hostPasswd and hostLoginName:
            self._hostPasswd = hostPasswd
            self._hostLoginName = hostLoginName

    # @brief: open a telnet connection to a host processor.
    def open_host_connection(self, hostName=None, hostPort=None, timeout=None, hide=None):
        if hostName and hostPort:
            self._hostName = hostName
            hostPort = hostPort
        self.open(self._hostName, hostPort, timeout)
        if not self.sock:
            raise ValueError('Host connection open failed!')
        else:
            self.log('Host connection open succeeded!', hide)

    # @brief: log in the Linux system with specified name + passwd.
    def host_login(self, hostLoginName, hostPasswd):
        try:
            self._hostLoginName = hostLoginName
            self._hostPasswd = hostPasswd
            '''
            # First, enter the login name when "raspberrypi login:"
            # Second, enter the password when "Password:"
            # Last, verify login using "hostLoginName@raspberrypi"
            '''
            self.read_until("raspberrypi login:", 5)
            self.write(hostLoginName + "\n")
            self.read_until("Password:", 5)
            self.write(hostPasswd + "\n")
            self.read_until(self._hostLoginName + "@", 5)
            self.log('Host [' + self._hostLoginName + '] login succeeded!')
            return 'success'
        except EOFError:
            self.log('Socket disconnected.')
            return 'conn_failure'

    # @brief: send commands to the host application with expected results.
    #         Returns 'success' if match is found, otherwise return original
    #         printouts.
    def host_send_expect(self, cmd, expectStr, timeout=None, hide=None):
        try:
            self.log("Sending cmd [" + cmd + "]...", hide)
            self.write(cmd + "\r\n")
            buf = self.read_until(expectStr, timeout)
            if expectStr in buf:
                return 'success'
            else:
                msg = "Expected string [" + \
                      expectStr + \
                      "] not found. Original prints:"
                # self.log(buf)
                return msg + "\n" + buf
        except EOFError:
            self.log('Socket disconnected.')
            return 'conn_failure'

    # @brief: send commands to the host application and return results. No
    #         check on the expected pattern.
    def host_send(self, cmd, timeout=None, hide=None):
        #try:
        self.log("Sending cmd [" + cmd + "]...", hide)
        self.write(cmd + "\r\n")
        print("BUG Before:")
        buf = self.read_until('Nonsense', timeout)
        print("BUG After:", buf)
        return buf
        #except EOFError, IOError:
        #    self.log('Socket disconnected.')
        #    return ''


import paramiko

class RemoteDeployer:
    
    def __init__(self, ip, username, password=None):
        self.ip = ip
        self.username = username
        self.password = password
        self.ssh = None
        
    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.connect(self.ip, username=self.username, password=self.password)
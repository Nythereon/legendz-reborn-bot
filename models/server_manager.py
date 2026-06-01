class ServerManager:
    def __init__(self):
        self.servers = {}

    def server_count(self):
        return len(self.servers)
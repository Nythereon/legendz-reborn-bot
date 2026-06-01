class ServerObject:
    def __init__(
            self,
            identifier,
            server_name,
            game_type,
            ip,
            port,
    ):

        self.identifier = identifier
        self.server_name = server_name
        self.game_type = game_type
        self.ip = ip
        self.port = port

        self.game_name = None
        self.egg = None
        self.nest = None

        self.public_ip = None
        self.query_port = None
        self.rcon = None

        self.current_state = "unknown"
        self.player_count = 0
        self.max_players = 0
        self.uptime = 0

        self.version = None
        self.motd = None
        self.map = None
        self.error = None

    def to_dict(self):
        return self.__dict__

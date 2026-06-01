class PlayerManager:
    def __init__(self):
        self.members = []
        self.online_members = {}
        self.activity_count = {}

    @property
    def total_count(self):
        return len(self.members)

    @property
    def online_count(self):
        return len(self.online_members)


    def clear_total_members(self):
        self.members = []

    def clear_online_members(self):
        self.online_members = {}
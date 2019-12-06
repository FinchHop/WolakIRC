class members:
    def __init__(self, nickname=None,conn=None):
        self.nickname = nickname
        self.conn = conn

    def set_nickname(self, nick):
        self.nickname = nick

    def set_connection(self, conn):
        self.conn = conn
        
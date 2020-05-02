class Score(object):
    def __init__(self, host):
        self.host = host
        self.total = 0

    def add(self, points):
        self.total += points

    def remove(self, points):
        self.total -= points

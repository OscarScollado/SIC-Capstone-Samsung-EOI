from datetime import timedelta
from random import choice

class Event:
    def __init__(self, name, now):
        days = choice(range(0, 50 + 1, 10)) # 0 - 50 days
        minutes = choice(range(0, 180 + 1, 30)) # 0 - 3 hours

        self.name = name
        self.now = now
        self.date = self.now + timedelta(days=days, minutes=minutes)
        self.starts_now = self.now == self.date

    def __str__(self):
        return f'{self.name}: {self.date.strftime("%d/%m/%y %H:%M:%S")}'
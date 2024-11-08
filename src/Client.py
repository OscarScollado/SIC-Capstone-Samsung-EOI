from Agent import Agent

class Client(Agent):
    """An agent able to interact with the stadium."""

    def __init__(self, name):
        super().__init__(name)
        self.stadium = None # here goes a Stadium object
        self.tickets = [] # here goes a list of Event objects
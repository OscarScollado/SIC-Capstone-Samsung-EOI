from Client import Client
from Agent import Agent
from Event import Event
from random import choice, choices, randint

class Stadium(Agent):
    """An agent capable of holding events."""

    def __init__(self, name, now):
        super().__init__(name)
        self.events = {} # {event.name: Event}
        self.now = now
        self.location= choice(('North coast', 'East coast', 'West coast', 'South coast'))
        self.size = (randint(100, 120), randint(65, 75))
        self.color = choices(('Green', 'Blue', 'Red', 'Black', 'White'), k=randint(1, 2))
        self.issues = []
        self.cheers = []

    def __str__(self):
        return (
                f'Stadium {self.name}:' +
                f'\n- Location: {self.location}.' +
                f'\n- Size: {self.size[0]}x{self.size[1]} meters.' +
                f'\n- Color: {' and '.join(self.color)}.'
        )

    def add_event(self, event_name):
        """Adds a new event to the stadium."""
        self.events[event_name] = Event(event_name, self.now)

    def remove_event(self, event_name):
        """Deletes an event from the stadium."""
        del self.events[event_name]

    def filter_events(self, which):
        """Returns a filtered subset of the stadium's events."""
        if which == 'current':
            return filter(lambda e: e.starts_now, self.events.values())
        elif which == 'future':
            return filter(lambda e: not e.starts_now, self.events.values())
        else: # client's events
            return filter(lambda e: e in which.tickets, self.events.values())

    def show_events(self, which_events):
        """Shows a list of the stadium's events."""
        events = tuple(self.filter_events(which_events))
        subject = ''
        if isinstance(which_events, Client):
            subject += which_events.name
        else:
            subject += which_events.capitalize()

        print(f'{subject} events hosted in {self.name}:')
        if len(events) == 0:
            print('(none)')
        for event in events:
            print(f'- {event.name}')
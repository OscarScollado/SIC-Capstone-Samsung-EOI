#!/usr/bin/env python
# coding: utf-8

# # SIC Capstone project

# #### Clients & Stadiums

# ## Class hierarchy

# ### Agent

# In[193]:


class Agent:
    """Base class for all agents."""

    def __init__(self, name):
        self.name = name


# ### Client

# In[195]:


class Client(Agent):
    """An agent able to interact with the stadium."""

    def __init__(self, name):
        super().__init__(name)
        self.stadium = None # here goes a Stadium object
        self.tickets = [] # here goes a list of Event objects


# ### Event

# In[197]:


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


# ### Stadium

# In[199]:


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


# ### AgentManager

# In[201]:


from datetime import datetime

class AgentManager:
    """Util class for managing the agents."""

    agents = {}
    now = datetime.now() # The time has to be fixed and recycled

    def add_agent(self, agent_type, agent_name):
        """Adds a new agent to the system."""
        if agent_type == 'stadium':
            self.agents[agent_name] = Stadium(agent_name, AgentManager.now)
            return True
        if agent_type == 'client':
            self.agents[agent_name] = Client(agent_name)
            return True
        return False

    def retrieve_all_agents_of_type(self, agent_type):
        """Returns a list of agents of the specified type"""
        which_type = None
        if agent_type == 'stadium':
            which_type = Stadium
        elif agent_type == 'client':
            which_type = Client
        else:
            return []
        selected_agents = []
        for agent in self.agents.values():
            if isinstance(agent, which_type):
                selected_agents.append(agent)
        return selected_agents


# ### Simulation

# In[203]:


class Simulation:
    """Main class. Manages the simulation."""
    command_args = {
        'stadium': {
            'add': ('<stadium_name>',),
            'add_event': ('<stadium_name>', '<event_name>'),
            'show_events': ('<stadium_name>',),
            'show_attendance': ('<stadium_name>', '<event_name>'),
            'remove_event': ('<stadium_name>', '<event_name>'),
            'show_current_events': ('<stadium_name>',),
            'show_info': ('<stadium_name>',),
            'show_clients': ('<stadium_name>',)
        },
        'client': {
            'add': ('<client_name>',),
            'buy_ticket': ('<client_name>', '<stadium_name>', '<event_name>'),
            'cancel_ticket': ('<client_name>', '<stadium_name>', '<event_name>'),
            'enter': ('<client_name>', '<stadium_name>'),
            'leave': ('<client_name>', '<stadium_name>'),
            'request_refund': ('<client_name>', '<stadium_name>', '<event_name>'),
            'check_wait_time': ('<client_name>', '<stadium_name>'),
            'view_ticket_status': ('<client_name>', '<stadium_name>', '<event_name>'),
            'cheer_for_team': ('<client_name>', '<stadium_name>', '<team_name>'),
            'check_event_schedule': ('<client_name>', '<stadium_name>'),
            'report_issue': ('<client_name>', '<stadium_name>', '<issue_description>'),
            'show_all_clients': ()
        }
    }

    def __init__(self):
        self.agent_manager = self.am = AgentManager()

    def valid_stadium(self, name, silent=False):
        """Checks whether a specific Stadium exists."""
        if name not in self.am.agents:
            if not silent:
                print(f'Error: Stadium {name} not found.')
            return False
        if not isinstance(self.am.agents[name], Stadium):
            if not silent:
                print(f'Error: {name} not found as a Stadium.')
            return False
        return True

    def valid_client(self, name, silent=False):
        """Checks whether a specific Client exists."""
        if name not in self.am.agents:
            if not silent:
                print(f'Error: Client {name} not found.')
            return False
        if not isinstance(self.am.agents[name], Client):
            if not silent:
                print(f'Error: {name} not found as a Client.')
            return False
        return True

    def valid_event(self, stadium_name, event_name, silent=False):
        """Checks whether a specific Event exists in s Stadium."""
        if event_name in self.am.agents[stadium_name].events:
            return True
        if not silent:
            print(f'Error: Event {event_name} not found in Stadium {stadium_name}.')
        return False

    def show_error_invalid(self, agent, action):
        """Shows the "invalid command" error message."""
        usage_args = ' '.join(self.command_args[agent][action])
        print(f'Error: Invalid command format for "{action}". Usage: "{agent} {action} {usage_args}".')

    def show_error_unknown(self):
        """Shows the "unknown command" error message."""
        print('Unknown command. Type "?" for a list of commands.')

    def show_commands(self):
        """Shows all available commands."""
        print(
            '\nAvailable commands:' +
            '\n- stadium add <stadium_name>: Add a new stadium to the system.' +
            '\n- client add <client_name>: Add a client to the system.' +
            '\n- stadium add_event <stadium_name> <event_name>: Add a new event (e.g. football match) to the stadium.' +
            '\n- client buy_ticket <client_name> <stadium_name> <event_name>: Buy a ticket for an event at the stadium.' +
            '\n- client cancel_ticket <client_name> <stadium_name> <event_name>: Cancel a ticket for an event at the stadium.' +
            '\n- stadium show_events <stadium_name>: Show the list of upcoming events at the stadium.' +
            '\n- client enter <client_name> <stadium_name>: Allow a client to enter the stadium, provided they have a ticket.' +
            '\n- client leave <client_name> <stadium_name>: Allow a client to leave the stadium.' +
            '\n- stadium show_attendance <stadium_name> <event_name>: Show the list of customers attending a specific event at the stadium.' +
            '\n- client request_refund <client_name> <stadium_name> <event_name>: Request a refund for a purchased ticket.' +
            '\n- stadium remove_event <stadium_name> <event_name>: Remove an event from the stadium, provided there are no customers inside.' +
            '\n- client check_wait_time <client_name> <stadium_name>: Check the wait time to enter the stadium.' +
            '\n- stadium show_current_events <stadium_name>: Show current events taking place at the stadium.' +
            '\n- stadium show_info <stadium_name>: Show information about the stadium (e.g. location, capacity).' +
            '\n- client view_ticket_status <client_name> <stadium_name> <event_name>: Check the status of a ticket for an event.' +
            '\n- client cheer_for_team <client_name> <stadium_name> <team_name>: Indicate that a client is cheering for a specific team during a game.' +
            '\n- stadium show_clients <stadium_name>: Show the list of clients that are currently in the stadium.' +
            '\n- client check_event_schedule <client_name> <stadium_name>: Check the schedule of events at the stadium.' +
            '\n- client report_issue <client_name> <stadium_name> <issue_description>: Report a problem or concern while at the stadium.' +
            '\n- client show_all_clients: Show the list of all clients in the system' +
            '\n- q: Exit the simulation.'
        )

    def process_command(self, command):
        """Parses and executes the user's command."""
        parts = command.split()

        if not parts:
            return
        if parts[0] == '?':
            self.show_commands()
            return
        if len(parts) < 2:
            self.show_error_unknown()
            return

        agent, action, *args = parts

        try:
            if len(self.command_args[agent][action]) != len(args):
                self.show_error_invalid(agent, action)
                return
        except KeyError:
            self.show_error_unknown()
            return

        # enough to assume the command is in the correct format, provided the command name is valid
        if agent == 'stadium':
            if action == 'add':
                stadium_name, = args
                if self.valid_stadium(stadium_name, silent=True):
                    print(f'Error: Stadium {stadium_name} already exists.')
                    return
                if self.am.add_agent('stadium', stadium_name):
                    print(f'Stadium {stadium_name} successfully added to the system.')
                else:
                    print(f'Error: Couldn\'t add Stadium {stadium_name} to the system.')

            elif action == 'add_event':
                stadium_name, event_name = args
                if not self.valid_stadium(stadium_name):
                    return
                if self.valid_event(stadium_name, event_name, silent=True):
                    print(f'Error: Event {event_name} already exists.')
                    return
                stadium = self.am.agents[stadium_name]
                stadium.add_event(event_name)
                print(f'Event {event_name} successfully added to Stadium {stadium_name}.')

            elif action == 'show_events': # doesn't absorb excess args
                stadium_name, = args
                if not self.valid_stadium(stadium_name):
                    return
                stadium = self.am.agents[stadium_name]
                stadium.show_events('future')

            elif action == 'show_attendance':
                stadium_name, event_name = args
                if not self.valid_stadium(stadium_name):
                    return
                if not self.valid_event(stadium_name, event_name):
                    return
                clients = self.am.retrieve_all_agents_of_type('client')
                stadium = self.am.agents[stadium_name]
                event = stadium.events[event_name]
                print(f'Attendees for the {event_name} Event in Stadium {stadium_name}:')
                someones_there = False
                for client in clients:
                    if event in client.tickets:
                        someones_there = True
                        print(f'- {client.name}')
                if not someones_there:
                    print('(none)')

            elif action == 'remove_event':
                stadium_name, event_name = args
                if not self.valid_stadium(stadium_name):
                    return
                if not self.valid_event(stadium_name, event_name):
                    return
                stadium = self.am.agents[stadium_name]
                event = stadium.events[event_name]
                stadium.remove_event(event_name)
                print(f'Event {event_name} successfully removed from Stadium {stadium_name}.')

            elif action == 'show_current_events':
                stadium_name, = args
                if not self.valid_stadium(stadium_name):
                    return
                stadium = self.am.agents[stadium_name]
                stadium.show_events('current')

            elif action == 'show_info':
                stadium_name, = args
                if not self.valid_stadium(stadium_name):
                    return
                stadium = self.am.agents[stadium_name]
                print(stadium)

            elif action == 'show_clients':
                stadium_name, = args
                if not self.valid_stadium(stadium_name):
                    return
                clients = self.am.retrieve_all_agents_of_type('client')
                stadium = self.am.agents[stadium_name]
                print(f'Clients in Stadium {stadium_name}:')
                someones_there = False
                for client in clients:
                    if client.stadium == stadium:
                        print(f'- {client.name}')
                        someones_there = True
                if not someones_there:
                    print('(none)')

            else:
                self.show_error_unknown()

        elif agent == 'client':
            if action == 'add':
                client_name, = args
                if self.valid_client(client_name, silent=True):
                    print(f'Error: Client {client_name} already exists.')
                    return
                if self.am.add_agent('client', client_name):
                    print(f'Client {client_name} successfully added to the system.')
                else:
                    print(f'Error: Couldn\'t add Client {client_name} to the system.')

            elif action == 'buy_ticket':
                client_name, stadium_name, event_name = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                if not self.valid_event(stadium_name, event_name):
                    return
                client = self.am.agents[client_name]
                stadium = self.am.agents[stadium_name]
                event = stadium.events[event_name]
                client.tickets.append(event)
                print(f'Client {client_name} has bought a ticket for Event {event_name}.')

            elif action == 'cancel_ticket':
                client_name, stadium_name, event_name = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                if not self.valid_event(stadium_name, event_name):
                    return
                client = self.am.agents[client_name]
                stadium = self.am.agents[stadium_name]
                event = stadium.events[event_name]
                if event in client.tickets:
                    client.tickets.remove(event)
                    print(f'Client {client_name} has bought a ticket for Event {event_name}.')
                else:
                    print(f'Error: {client_name} doesn\'t have a ticket for Event {event_name}.')

            elif action == 'enter':
                client_name, stadium_name = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                client = self.am.agents[client_name]
                if client.stadium is not None:
                    print(f'Error: Client {client_name} is already in another Stadium ({stadium_name}).')
                else:
                    stadium = self.am.agents[stadium_name]
                    if len(tuple(stadium.filter_events(client))) > 0:
                        client.stadium = stadium
                        print(f'Client {client_name} entered Stadium {stadium_name}')
                    else:
                        print(f'Error: Client {client_name} doesn\'t have a ticket to enter Stadium {stadium_name}.')

            elif action == 'leave':
                client_name, stadium_name = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                client = self.am.agents[client_name]
                stadium = self.am.agents[stadium_name]
                if client.stadium == stadium:
                    client.stadium = None
                    print(f'Client {client_name} left Stadium {stadium_name}.')
                else:
                    print(f'Error: Client {client_name} isn\'t in Stadium {stadium_name}.')

            elif action == 'request_refund':
                client_name, stadium_name, event_name = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                if not self.valid_event(stadium_name, event_name):
                    return
                client = self.am.agents[client_name]
                stadium = self.am.agents[stadium_name]
                event = stadium.events[event_name]
                client_events = tuple(stadium.filter_events(client))
                if event in client_events:
                    client.tickets.remove(event)
                    print(f'Client {client_name} has just refunded a ticket for Event {event_name} at Stadium {stadium_name}.')
                else:
                    print(f'Error: Client {client_name} doesn\'t have a ticket for Event {event_name} at Stadium {stadium_name}.')

            elif action == 'check_wait_time':
                client_name, stadium_name = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                client = self.am.agents[client_name]
                stadium = self.am.agents[stadium_name]
                print(f'Wait time for Client {client_name} to enter Stadium {stadium_name}:')
                client_events = tuple(stadium.filter_events(client))
                if len(client_events) == 0:
                    print(f'Error: Client {client_name} doesn\'t have any ticket related to Stadium {stadium_name}.')
                    return
                event_times = (event.date for event in client_events)
                min_wait_time = min(event_times)
                time_diff = min_wait_time - self.am.now
                notice = ""
                days, hours, minutes = time_diff.days, int(time_diff.seconds / 3600), int(time_diff.seconds % 60)
                if days != 0:
                    notice += f'{days} days'
                if hours != 0:
                    notice += f' {hours} hours'
                if minutes != 0:
                    notice += f' {minutes} minutes'
                notice += '.'
                print(notice.strip())

            elif action == 'view_ticket_status':
                client_name, stadium_name, event_name = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                if not self.valid_event(stadium_name, event_name):
                    return
                client = self.am.agents[client_name]
                stadium = self.am.agents[stadium_name]
                event = stadium.events[event_name]
                if event in client.tickets:
                    print(f'Client {client_name} has a ticket for Event {event_name}.')
                else:
                    print(f'Client {client_name} doesn\'t have a ticket for Event {event_name}.')

            elif action == 'cheer_for_team':
                client_name, stadium_name, team_name = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                client = self.am.agents[client_name]
                stadium = self.am.agents[stadium_name]
                if client.stadium == stadium:
                    stadium.cheers.append(team_name)
                    n_cheers = stadium.cheers.count(team_name)
                    stadium_plural = "" if len(stadium.cheers) == 1 else "s"
                    team_plural = "" if n_cheers == 1 else "s"
                    print(
                        f'Client {client_name} just cheered for team {team_name} at Stadium {stadium_name}!' +
                        f'\n{len(stadium.cheers)} cheer{stadium_plural} in this Stadium so far.' +
                        f'\n{team_name} has been cheered {n_cheers} time{team_plural} in this Stadium so far.'
                    )
                else:
                    print(f'Error: Client {client_name} isn\'t in Stadium {stadium_name}.')

            elif action == 'check_event_schedule':
                client_name, stadium_name = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                client = self.am.agents[client_name]
                stadium = self.am.agents[stadium_name]
                print(f'Schedule for Client {client_name}\'s events in Stadium {stadium_name}:')
                no_events = True
                for event in stadium.events.values():
                    if event in client.tickets:
                        no_events = False
                        print(f'- {event}')
                if no_events:
                    print('(none)')

            elif action == 'report_issue':
                client_name, stadium_name, issue_description = args
                if not self.valid_client(client_name):
                    return
                if not self.valid_stadium(stadium_name):
                    return
                client = self.am.agents[client_name]
                stadium = self.am.agents[stadium_name]
                if client.stadium == stadium:
                    stadium.issues.append(issue_description)
                    issue_plural = "" if len(stadium.issues) == 1 else "s"
                    print(
                            f'Client {client_name} just reported an issue with Stadium {stadium_name}!' +
                            f'\n{len(stadium.issues)} issue{issue_plural} in this Stadium so far: "{issue_description}"'
                    )
                else:
                    print(f'Error: Client {client_name} isn\'t in Stadium {stadium_name}')

            elif action == 'show_all_clients':
                # no args here
                clients = self.am.retrieve_all_agents_of_type('client')
                print(f'Clients:')
                if len(clients) == 0:
                    print(f'(none)')
                for client in clients:
                    print(f'- {client.name}')

            else:
                self.show_error_unknown()
        else:
            self.show_error_unknown()

    def command_loop(self):
        """Main loop. Manages any entered commands."""
        print('Starting city simulation... Type "q" to exit.')
        while True:
            command = input('> ')
            if command == 'q':
                break
            self.process_command(command)


# ### Main program

# In[205]:


if __name__ == "__main__":
    simulation = Simulation()
    simulation.command_loop()


from Client import Client
from Stadium import Stadium
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
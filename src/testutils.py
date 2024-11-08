import sys
from io import StringIO
import builtins

from Client import Client
from Stadium import Stadium

""" USE EXAMPLE:
if __name__ == "__main__":
    test_name = ("client", "add_client")
    #test_name = None
    if test_name:
        str_in = tests[test_name[0]][test_name[1]] + ("q",)
        print(str_in)
        ai = AutoInput(str_in)
        input = ai.input

    simulation = Simulation()

    if test_name == ("mixed", "enter_leave"):
        inject["mixed"]["enter_leave"](simulation)

    simulation.command_loop()
"""

# automatic input testing
class AutoInput:
    def __init__(self, inputs):
        self.inputs = inputs
        sys.stdin = StringIO("\n".join(inputs))
        self.inputs_iter = iter(inputs)

    def input(self, prompt): # -> EOFError: EOF when reading a line (I'm trying to read more than what I'm feeding it)
        print("\033[92m", end="") # green input
        value = builtins.input(prompt)
        print(next(self.inputs_iter))
        print("\033[93m", end="") # yellow output
        return value

""" Reminder:
stadium:
    (1) add:                 "<stadium_name>"
    (2) add_event:           "<stadium_name>" "<event_name>"
    (1) show_events:         "<stadium_name>"
    (2) show_attendance:     "<stadium_name>" "<event_name>"
    (2) remove_event:        "<stadium_name>" "<event_name>"
    (1) show_current_events: "<stadium_name>"
    (1) show_info:           "<stadium_name>"
    (1) show_clients:        "<stadium_name>"
client:
    (1) add:                  "<client_name>"
    (3) buy_ticket:           "<client_name>" "<stadium_name>" "<event_name>"
    (3) cancel_ticket:        "<client_name>" "<stadium_name>" "<event_name>"
    (2) enter:                "<client_name>" "<stadium_name>"
    (2) leave:                "<client_name>" "<stadium_name>"
    (3) request_refund:       "<client_name>" "<stadium_name>" "<event_name>"
    (2) check_wait_time:      "<client_name>" "<stadium_name>"
    (3) view_ticket_status:   "<client_name>" "<stadium_name>" "<event_name>"
    (3) cheer_for_team:       "<client_name>" "<stadium_name>" "<team_name>"
    (2) check_event_schedule: "<client_name>" "<stadium_name>"
    (3) report_issue:         "<client_name>" "<stadium_name>" "<issue_description>"
    (0) show_all_clients:     "null"
"""

tests = {
    "stadium": {
        "nothing_created_wrong_n_of_params": (
            "stadium add", # fail
            "stadium add Sa Sb", # fail
            "stadium add_event", # fail
            "stadium add_event Sa", # fail
            "stadium add_event Sa Ea Eb", # fail
            "stadium show_events", # fail
            "stadium show_events Sa Sb", # fail
            "stadium show_attendance", # fail
            "stadium show_attendance Sa", # fail
            "stadium show_attendance Sa Ea Eb", # fail
            "stadium remove_event", # fail
            "stadium remove_event Sa", # fail
            "stadium remove_event Sa Ea Eb", # fail
            "stadium show_current_events", # fail
            "stadium show_current_events Sa Sb", # fail
            "stadium show_info", # fail
            "stadium show_info Sa Sb", # fail
            "stadium show_clients", # fail
            "stadium show_clients Sa Sb" # fail
        ),
        "one_stadium_no_events": (
            "stadium add Sa", # success
            "stadium add_event Sa", # fail
            "stadium show_events Sb", # fail
            "stadium show_events Sa", # empty
            "stadium show_attendance Sa", # fail
            "stadium remove_event Sa", # fail
            "stadium show_current_events Sb", # fail
            "stadium show_current_events Sa", # empty
            "stadium show_info Sb", # fail
            "stadium show_info Sa", # success
            "stadium show_info Sa", # success
            "stadium show_clients Sb", # fail
            "stadium show_clients Sa", # empty
            "stadium show_clients Sa" # empty
        ),
        "one_stadium_one_event": (
            "stadium add Sa", # success
            "stadium add_event Sb Ea", # fail
            "stadium add_event Sb Ea Eb", # fail
            "stadium add_event Sa Ea", # success
            "stadium show_events Sb", # fail
            "stadium show_events Sa Sb", # fail
            "stadium show_events Sa", # success
            "stadium show_attendance Sb Ea", # fail
            "stadium show_attendance Sb Ea Eb", # fail
            "stadium show_attendance Sa Eb", # fail
            "stadium show_attendance Sa Eb Ec", # fail
            "stadium show_attendance Sa Ea", # success
            "stadium show_current_events Sb", # fail
            "stadium show_current_events Sa Sb", # fail
            "stadium show_current_events Sa", # success
            "stadium remove_event Sb Ea", # fail
            "stadium remove_event Sb Ea Eb", # fail
            "stadium remove_event Sa Eb Ec", # fail
            "stadium remove_event Sa Eb", # fail
            "stadium remove_event Sa Ea", # success
            "stadium show_events Sa", # empty
            "stadium show_attendance Sa Ea", # fail
            "stadium show_current_events Sa", # empty
            "stadium remove_event Sa Ea" # fail
        ),
        "multiple_stadiums_multiple_events": (
            "stadium add Sa", # success
            "stadium add Sa", # fail
            "stadium add_event Sa Ea", # success
            "stadium add_event Sa Ea", # fail
            "stadium add Sb", # success
            "stadium add Sb", # fail
            "stadium add_event Sb Eb", # success
            "stadium add_event Sb Eb", # fail
            "stadium remove_event Sb Ea Ec", # fail
            "stadium remove_event Sa Eb Ec", # fail
            "stadium remove_event Sa Ea Ec", # fail
            "stadium remove_event Sb Eb Ec", # fail
            "stadium show_attendance Sa Eb", # fail
            "stadium show_attendance Sb Ea", # fail
            "stadium show_attendance Sa Ea", # empty
            "stadium show_attendance Sb Eb", # empty
            "stadium remove_event Sa Eb", # fail
            "stadium remove_event Sb Ea", # fail
            "stadium remove_event Sa Ea", # success
            "stadium remove_event Sb Eb", # success
            "stadium show_events Sa", # empty
            "stadium show_events Sb" # empty
        )
    },
    "client": {
        "add_client": (
            "client add Ca", # success
        )
    },
    "mixed": {
        "enter_leave": (
            "client enter", # fail
            "client enter Sa", # fail
            "client enter Ca", # fail
            "client enter Sa Ca", # fail
            "client enter Ca Sa Sb", # fail
            "client enter Ca Sa", # success
            "client enter Ca Sa", # fail
            "client enter Cb Sa", # fail
            "stadium show_attendance Sa Ea", # success
            "stadium show_clients Sa", # success
            "client leave", # fail
            "client leave Sa", # fail
            "client leave Ca", # fail
            "client leave Sa Ca", # fail
            "client leave Ca Sa Sb", # fail
            "client leave Ca Sa", # success
            "client leave Ca Sa", # fail
            "client leave Cb Sa", # fail
            "stadium show_attendance Sa Ea", # success
            "stadium show_clients Sa" # empty
        )
    }
}

def mixed_enter_leave(s):
    s.am.agents = {
        "Sa": Stadium("Sa", s.am.now),
        "Ca": Client("Ca"),
        "Cb": Client("Cb")
    }
    stadium = s.am.agents["Sa"]
    stadium.add_event("Ea")
    event = stadium.events["Ea"]
    s.am.agents["Ca"].tickets.append(event)

inject = {
    "mixed": {
        "enter_leave":
            mixed_enter_leave
    }
}
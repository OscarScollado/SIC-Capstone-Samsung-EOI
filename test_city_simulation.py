import unittest
from io import StringIO
import sys
from CitySimulation import Simulation
import time

class TestCitySimulation(unittest.TestCase):
    test_number = 0
    def setUp(self):
        self.simulation = Simulation()

    def run_command_and_assert(self,command, expected_output):
        try:
            output = StringIO()
            sys.stdout = output
            self.simulation.process_command(command)
            sys.stdout = sys.__stdout__
            result_output = output.getvalue()
            TestCitySimulation.test_number +=1
            print(f'# {TestCitySimulation.test_number}\n>{command}\n{result_output.strip()}',end='')
            self.assertIn(expected_output, result_output)
            print(' "Test passsed!"')
        except AssertionError:
            print()
            print("="*40)
            print(' "Test not passsed!"') 
            print("="*40)
            print(f'AssertionError: Expected output\n"{expected_output}"\nnot found in actual output:\n"{result_output.strip()}"')
            follow=input("q: quit, press other key continue...")
            if follow=='q':
                sys.exit(1)


    def test_commands(self):
        print('testing ...')

        self.run_command_and_assert("stadium add Bernabeu", "Stadium Bernabeu successfully added to the system.")
        self.run_command_and_assert("client add Billy", "Client Billy successfully added to the system.")
        self.run_command_and_assert("stadium add_event Bernabeu Futbol", "Event Futbol successfully added to Stadium Bernabeu.")
        self.run_command_and_assert("client buy_ticket Billy Bernabeu Futbol", "Client Billy has bought a ticket for Event Futbol.")
        self.run_command_and_assert("client enter Billy Bernabeu", "Client Billy entered Stadium Bernabeu")
        self.run_command_and_assert("stadium show_events Bernabeu", "Future events hosted in Bernabeu:\n- Futbol")
        self.run_command_and_assert("client show_all_clients", "Clients:\n- Billy")
        self.run_command_and_assert("client view_ticket_status Billy Bernabeu Futbol", "Client Billy has a ticket for Event Futbol.")
        self.run_command_and_assert("stadium show_attendance Bernabeu Futbol", "Attendees for the Futbol Event in Stadium Bernabeu:\n- Billy")
        self.run_command_and_assert("stadium show_clients Bernabeu", "Clients in Stadium Bernabeu:\n- Billy")
        self.run_command_and_assert("stadium show_current_events Bernabeu", "Current events hosted in Bernabeu:\n(none)")
        self.run_command_and_assert("client check_event_schedule Billy Bernabeu", "Schedule for Client Billy's events in Stadium Bernabeu:\n- Futbol: ") # Event date is random
        self.run_command_and_assert("client check_wait_time Billy Bernabeu","Wait time for Client Billy to enter Stadium Bernabeu:") # Event date difference is random
        self.run_command_and_assert("client cheer_for_team Billy Bernabeu Raven","Client Billy just cheered for team Raven at Stadium Bernabeu!\n1 cheer in this Stadium so far.\nRaven has been cheered 1 time in this Stadium so far.")
        self.run_command_and_assert("client report_issue Billy Bernabeu Unamused","Client Billy just reported an issue with Stadium Bernabeu!\n1 issue in this Stadium so far: \"Unamused\"")
        self.run_command_and_assert("client request_refund Billy Bernabeu Futbol","Client Billy has just refunded a ticket for Event Futbol at Stadium Bernabeu.")
        self.run_command_and_assert("client cancel_ticket Billy Bernabeu Futbol", "Error: Billy doesn't have a ticket for Event Futbol.")
        self.run_command_and_assert("client leave Billy Bernabeu", "Client Billy left Stadium Bernabeu.")
        self.run_command_and_assert("stadium remove_event Bernabeu Futbol", "Event Futbol successfully removed from Stadium Bernabeu.")
        self.run_command_and_assert("stadium show_info Bernabeu","Stadium Bernabeu:\n- Location: ") # Stadium description is random


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCitySimulation)
    unittest.TextTestRunner(verbosity=2).run(suite)

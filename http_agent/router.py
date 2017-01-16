from http_agent.views import Greetings, Greeting, Do_Greet, Status


def configure_routes(shell, core):
    shell.add_route('/greetings', Greetings(shell, core))
    shell.add_route('/greetings/{greet_id}', Greeting(shell, core))
    shell.add_route('/actions/greet/{greet_id}', Do_Greet(shell, core))
    shell.add_route('/status', Status(shell, core))

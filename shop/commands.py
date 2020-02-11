class CommandsInvoker:
    def __init__(self):
        self._commands_list = []

    def store_command(self, command):
        self._commands_list.append(command)

    def execute_commands(self):
        for command in self._commands_list:
            command()
        self._clear_commands()

    def _clear_commands(self):
        self._commands_list = []

    def rollback_commands(self):
        self._clear_commands()

from pytest import raises
from commands import CommandsInvoker


def create_file(file_name):
    with open(file_name, 'w') as f:
        f.write('done')


class TestInvoker:

    def setup(self):
        self.ci = CommandsInvoker()

    def test_commit(self):
        self.ci.store_command(lambda: create_file('test_command_commit'))
        self.ci.execute_commands()
        with open('test_command_commit', 'r') as f:
            assert f.read() == 'done'

    def test_rollback(self):
        self.ci.store_command(lambda: create_file('test_command_rollback'))
        self.ci.rollback_commands()
        with raises(Exception):
            open('test_command_rollback', 'r')
        assert not self.ci._commands_list

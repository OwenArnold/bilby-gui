from ICommand import ICommand


class CommandBinding(object):

    def __init__(self, command, target):
        super(CommandBinding, self).__init__()

        if not isinstance(command, ICommand):
            raise ValueError("CommandBinding: the specified command is not of type \"ICommand\"")

        self._target = target
        self._target_slot = lambda: command.execute() if command.can_execute() else None
        self._target.clicked.connect(self._target_slot)

    def destroy(self):
        if self._target_slot:
            self._target.clicked.disconnect(self._target_slot)
            self._target_slot = None

from abc import ABC, abstractmethod
from .browser import RecordableBrowser

class Command(ABC):
    names: tuple[str, ...]

    def __init__(self, recorder: RecordableBrowser):
        self.recorder = recorder

    @abstractmethod
    def execute(self, argument: str | None = None):
        ...

class RecordCommand(Command):
    names = ("record", "r")

    def execute(self, argument=None):
        if argument:
            self.recorder.record_output = argument
        
        self.recorder.start_recording()
        print(f"Start recording {argument}")


class PlayCommand(Command):
    names = ("play", "pl")

    def execute(self, argument=None):
        self.recorder.is_playing = True
        print("Playing")


class PauseCommand(Command):
    names = ("pause", "p")

    def execute(self, argument=None):
        self.recorder.is_playing = False
        print("Paused")

class StopCommand(Command):
    names = ("stop", "s")

    def execute(self, argument = None):
        self.recorder.stop_recording()
        print("Stopped recording")

class ExecuteCommand(Command):
    names = ("execute", "e")

    def execute(self, argument = None):
        if argument:
            self.recorder.record_input = argument
        else:
            print('No argument. Using last input file', self.recorder.record_input)
        
        print('Executing events')
        self.recorder.execute_record()


class CommandProcessor:
    def __init__(self, commands: list[Command]):
        self.commands = {}

        for command in commands:
            for name in command.names:
                self.commands[name] = command

    def process(self, user_input: str):
        cmd, _, arg = user_input.partition(" ")
        cmd = cmd.lower()
        arg = arg.strip() or None

        if cmd in self.commands:
            self.commands[cmd].execute(arg)
        else:
            print(f"Unknown command: {cmd}")
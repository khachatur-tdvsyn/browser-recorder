from abc import ABC, abstractmethod
from .browser import RecordableBaseBrowser

class Command(ABC):
    names: tuple[str, ...]
    description: str
    usage: str

    def __init__(self, recorder: RecordableBaseBrowser):
        self.recorder = recorder

    @abstractmethod
    def execute(self, argument: str | None = None):
        ...

class RecordCommand(Command):
    names = ("record", "r")
    description = "Start recording user interactions in browser."
    usage = "record [output_file] | r [output_file]"

    def execute(self, argument=None):
        if argument:
            self.recorder.record_output = argument
        
        self.recorder.start_recording()
        print(f"Start recording {argument}")


class PlayCommand(Command):
    names = ("play", "pl")
    description = "Resume playing recorded interactions"
    usage = "play | pl"

    def execute(self, argument=None):
        self.recorder.is_playing = True
        print("Playing")


class PauseCommand(Command):
    names = ("pause", "p")
    description = "Pause recording or playback."
    usage = "pause | p"

    def execute(self, argument=None):
        self.recorder.is_playing = False
        print("Paused")

class StopCommand(Command):
    names = ("stop", "s")
    description = "Stop recording user interactions."
    usage ="stop | s"

    def execute(self, argument = None):
        self.recorder.stop_recording()
        print("Stopped recording")

class ExecuteCommand(Command):
    description = "Execute recorded interactions from a file."
    names = ("execute", "e")
    usage = "execute [input_file] | e [input_file]"

    def execute(self, argument = None):
        if argument:
            self.recorder.record_input = argument
        else:
            print('No argument. Using last input file', self.recorder.record_input)
        
        print('Executing events')
        self.recorder.execute_record()

class ExitCommand(Command):
    names = ("exit", "quit", "close")
    description = "Just to close the program."
    usage = "exit | quit | close"

    def execute(self, argument = None):
        exit()

class HelpCommand(Command):
    names = ("help", "h", "?")
    description = "Show all available commands and their usage"
    usage = "help"

    def __init__(self, recorder: RecordableBaseBrowser, command_processor=None):
        super().__init__(recorder)
        self.command_processor = command_processor

    def execute(self, argument=None):
        print("\nAvailable Commands:")
        print("-" * 60)
        commands_shown = set()
        
        if self.command_processor:
            for cmd_name in sorted(self.command_processor.commands.keys()):
                cmd = self.command_processor.commands[cmd_name]
                if cmd.names[0] == cmd_name:
                    commands_shown.add(cmd)
                    print(f"{cmd_name} - {cmd.description}\nUsage: {cmd.usage}\n")
        
        print("-" * 60)


class CommandProcessor:
    def __init__(self, commands: list[Command]):
        self.commands = {}

        for command in commands:
            for name in command.names:
                self.commands[name] = command
        
        # Set command_processor reference for HelpCommand if present
        for command in commands:
            if isinstance(command, HelpCommand):
                command.command_processor = self

    def process(self, user_input: str):
        cmd, _, arg = user_input.partition(" ")
        cmd = cmd.lower()
        arg = arg.strip() or None

        if cmd in self.commands:
            self.commands[cmd].execute(arg)
        else:
            print(f"Unknown command: {cmd}")
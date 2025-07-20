from abc import abstractmethod
from io import TextIOBase
from typing import TextIO, Callable

from ..lexer.main import Lexer
from ..token.main import Token
from ..utils.error import ErrorReporter
from ..utils.text import get_line_terminator


Stream = TextIO | TextIOBase
OutputCallable = Callable[[str],None]
InputCallable = Callable[[],str]


class BaseInterpreter:
    @abstractmethod
    def read_input(self) -> str:
        pass
    @abstractmethod
    def print_output(self, text: str):
        pass
    @abstractmethod
    def print_error(self, text: str):
        self.print_output(text)


class Interpreter(BaseInterpreter):
    def __init__(self, read_input: InputCallable, print_output: OutputCallable, print_error: OutputCallable):
        super().__init__()

        self.had_error = False
        self._read_input = read_input
        self._print_output = print_output
        self._print_error = print_error

        assert(self.read_input and self.print_output and self.print_error)

    def read_input(self) -> str:
        return self._read_input()

    def print_output(self, text: str):
        self._print_output(text)

    def print_error(self, text: str):
        self._print_error(text)

    def _execute(self, source: str):
        self.had_error = False

        try:
            tokens = self.parse_source(source)
            self.parse_tokens(tokens)

        except Exception as e:
            self.error(1, source, str(e), "")
            raise e

    def error(self, line_no: int, line: str, message: str, token: str):
        self.had_error = True
        message = ErrorReporter.format_error(line_no, line, message, token)
        self.print_error(message + get_line_terminator())

    def parse_source(self, source: str) -> list[Token]:
        scanner = Lexer(source)
        tokens = scanner.scan_tokens()
        return tokens

    def parse_tokens(self, tokens: list[Token]) -> None:
        text = ""
        for token in tokens:
            text = text + f"{token} "
        self.print_output(text)

    def execute_line(self, line: str):
        """
        Executes a single line of input using the interpreter.

        Args:
            line (str): The line of code to be executed.
        """

        self._execute(line)


    def execute_stream(self, stream: Stream):
        """
        Executes a stream of input lines using the interpreter.

        Args:
            stream (Stream): The input stream containing lines of code to be executed.
        """

        while 1:
            line = stream.readline()
            if len(line) == 0:
                break

            self.execute_line(line)

            if self.had_error:
                break


    def execute_file(self, filepath: str):
        with open(filepath, "r") as file:
            self.execute_stream(file)

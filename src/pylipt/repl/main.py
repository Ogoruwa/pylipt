from enum import StrEnum
from typing import TextIO
from textwrap import dedent
from sys import stdin, stderr, stdout

from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.input.defaults import create_input
from prompt_toolkit.output.defaults import create_output
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import StyleAndTextTuples, FormattedText

from .settings import get_settings
from ..interpreter.main import Stream, Interpreter
from ..utils.text import get_line_terminator


class PROMPT(StrEnum):
    LINE = ">>> "
    CONTINUE = "... "


class REPL:
    def __init__(self, stream_in: TextIO | None = None, stream_out: TextIO | None = None, stream_err: Stream | None = None):
        self.stdin = stream_in or stdin
        self.stdout = stream_out or stdout
        self.stderr = stream_err or stderr
        self._prompt_settings = {
            "enable_suspend": True,
            "complete_in_thread" : True,
            "prompt_continuation": self._generate_continuation_prompt
        }

        self._settings = get_settings()
        self._line_terminator = get_line_terminator()

        self._interpreter = Interpreter(self.read, self.print, self.print)
        self._session = PromptSession(input = create_input(self.stdin), output = create_output(self.stdout))

        self._intro = dedent("""
            Pylipt 0.1.0 (main, Jul 08 2025, 00:00:00) [Python 3.13.5]
        """)

    def _generate_line_prompt(self) -> FormattedText:
        prompt_text = [("class:line_terminator", self._line_terminator), ("class:prompt", PROMPT.LINE)]
        prompt_style = Style.from_dict({"prompt": "#884444"})
        prompt = FormattedText((prompt_text, prompt_style))

        return prompt

    def _generate_continuation_prompt(self, width: int, line_number: int, is_soft_wrap: bool) -> StyleAndTextTuples:
        prompt = [
            ("class:line_terminator", self._line_terminator),
            ("class:prompt", (' ' * (width - len(PROMPT.CONTINUE)) + PROMPT.CONTINUE))
        ]

        return prompt


    def read(self) -> str:
        prompt, prompt_style = self._generate_line_prompt()
        text = self._session.prompt(prompt, **self._prompt_settings, style = prompt_style)
        return text

    def execute(self, line: str):
        self._interpreter.execute_line(line)

    def print(self, text: str, flush: bool = False):
        print_formatted_text(text, end = "", flush = flush, output = self._session.output)

    def loop(self) -> bool:
        try:
            text = self.read()
            self.execute(text)
            self.print(get_line_terminator(), True)

        except KeyboardInterrupt:
            self.print("KeyboardInterrupt\n")

        except EOFError:
            return False

        return True

    def run(self):
        running = True
        self.print(self._intro)

        with patch_stdout():
            while running:
                running = self.loop()

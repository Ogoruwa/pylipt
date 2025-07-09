from io import StringIO
from argparse import ArgumentParser


def main(script: str, command: bool = False):
    if script:
        from .interpreter.main import Interpreter

        interpreter = Interpreter()

        if command:
            stream = StringIO(script)
            interpreter.execute_stream(stream)

        else:
            interpreter.execute_file(script)

    else:
        from .repl.main import REPL

        repl = REPL()
        repl.run()


if __name__ == "__main__":
    parser = ArgumentParser(description = "An interpreter for `pylipt`")

    source = parser.add_mutually_exclusive_group()
    source.add_argument("-c", "--cmd", default = None, help = "Run as a command")
    source.add_argument("script", nargs = "?", default = None, help = "The script to run")

    args = parser.parse_args()
    main(args.script or args.cmd, command = bool(args.cmd))

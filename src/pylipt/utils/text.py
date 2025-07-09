from .os import is_nix


def get_line_terminator() -> str:
    if is_nix():
        return "\n"
    else:
        return "\r\n"

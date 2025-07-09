from sys import platform


def is_windows():
    return platform == "win32"

def is_darwin():
    return platform == "darwin"

def is_linux():
    return platform == "linux"

def is_nix():
    return not (is_windows())


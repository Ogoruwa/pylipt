from enum import IntEnum

class IndentationType(IntEnum):
    SPACES = 1
    TABS = 2


class Settings:
    VERSION = 0.1
    INDENTATION_TYPE = IndentationType.SPACES
    INDENTATION_SIZE = 4


def get_settings() -> Settings:
    return Settings()
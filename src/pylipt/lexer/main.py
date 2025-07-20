from typing import Any

from pylipt.token.main import Token, TokenType
from pylipt.utils.text import get_line_terminator, get_whitespace
from .mapping import SINGLE_TOKEN_MAPPING, DOUBLE_TOKEN_PAIRS, DOUBLE_TOKEN_MAPPING


class Lexer:
    """ Provides methods to parse source code as tokens """
    def __init__(self, source: str) -> None:
        self._line = 1
        self._start = 0
        self._current = 0
        self._source = source
        self._tokens: list[Token] = []

    def is_finished(self) -> bool:
        """ Returns whether source has been completely parsed """
        return self._current >= len(self._source)

    def _next_character(self) -> str:
        """ Returns the next character in the source for parsing """
        character = self._source[self._current]
        self._current += 1
        return character

    def _add_next_token(self, token_type: TokenType, literal: Any):
        """ Adds current string as a token """
        string = self._source[self._start:self._current]
        token = Token(token_type, string, literal, self._line)
        self._tokens.append(token)

    def add_next_token(self, token_type: TokenType):
        """ Wrapper function for `_add_next_token`, for setting the literal """
        self._add_next_token(token_type, None)

    def match_next_character(self, expected: str) -> bool:
        """ If next character matches expected character, add token"""
        if self.is_finished():
            return False
        elif self._source[self._current] != expected:
            return False
        else:
            self._current += 1
            return True

    def peek_next_character(self):
        """ Get next character without advancing """
        if self.is_finished():
            return '\0'
        else:
            return self._source[self._current]

    def scan_token(self):
        """ Scans the current string for a valid token """
        character = self._next_character()

        if character == get_line_terminator():
            self._line += 1

        elif character in get_whitespace():
            pass

        elif character in SINGLE_TOKEN_MAPPING:
            single = True
            next_character = ''

            if character in DOUBLE_TOKEN_PAIRS:
                next_characters = DOUBLE_TOKEN_PAIRS[character]

                for next_character in next_characters:
                    if self.match_next_character(next_character):
                        single = False
                        break

            if single:
                token_type = SINGLE_TOKEN_MAPPING[character]
            else:
                token_type = DOUBLE_TOKEN_MAPPING[character + next_character]

            if token_type == TokenType.COMMENT:
                while not self.is_finished() and self.peek_next_character() != get_line_terminator():
                    self._next_character()
            else:
                self.add_next_token(token_type)

        else:
            # Invalid token encountered
            pass


    def scan_tokens(self) -> list[Token]:
        """ Parse source completely """
        while not self.is_finished():
            self._start = self._current
            self.scan_token()

        eof_token = Token(TokenType.EOF, "", None, self._line)
        self._tokens.append(eof_token)

        return self._tokens

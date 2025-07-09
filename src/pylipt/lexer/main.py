from typing import Any

from pylipt.token.main import Token, TokenType
from .mapping import SINGLE_TOKEN_MAPPING


class Lexer:
    def __init__(self, source: str) -> None:
        self._line = 1
        self._start = 0
        self._current = 0
        self._source = source
        self._tokens: list[Token] = []

    def is_finished(self) -> bool:
        return self._current >= len(self._source)


    def _next_character(self) -> str:
        character = self._source[self._current]
        self._current += 1
        return character


    def _add_next_token(self, token_type: TokenType, literal: Any):
        string = self._source[self._start:self._current]
        token = Token(token_type, string, literal, self._line)
        self._tokens.append(token)

    def add_next_token(self, token_type: TokenType):
        self._add_next_token(token_type, None)


    def scan_token(self):
        character = self._next_character()
        match character:
            case i if i in SINGLE_TOKEN_MAPPING:
                self.add_next_token(SINGLE_TOKEN_MAPPING[i])


    def scan_tokens(self) -> list[Token]:
        while not self.is_finished():
            self._start = self._current
            self.scan_token()

        eof_token = Token(TokenType.EOF, "", None, self._line)
        self._tokens.append(eof_token)
        # self.add_next_token(TokenType.EOF)
        return self._tokens

import unittest

from pylipt.token.main import Token, TokenType


class TokenTestCase(unittest.TestCase):
    def test_token_initialization(self):
        for token_type in set(TokenType):
            token = Token(token_type, "test", None, 1)
            self.assertEqual(token.token_type, token_type)
            self.assertEqual(token.lexeme, "test")
            self.assertEqual(token.literal, None)
            self.assertEqual(token.line, 1)


if __name__ == '__main__':
    unittest.main()

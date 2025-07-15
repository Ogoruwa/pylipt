import unittest

from pylipt.lexer.mapping import DOUBLE_TOKEN_MAPPING, DOUBLE_TOKEN_PAIRS


class TokenMappingTestCase(unittest.TestCase):
    def test_double_token_mapping(self):
        for single_token in set(DOUBLE_TOKEN_PAIRS):
            token_pairs = [ single_token + next_token for next_token in DOUBLE_TOKEN_PAIRS[single_token] ]

            for token_pair in token_pairs:
                self.assertIn(token_pair, DOUBLE_TOKEN_MAPPING, f"Double token {token_pair} was not assigned a token type")


if __name__ == '__main__':
    unittest.main()

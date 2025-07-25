import unittest

from pylipt.lexer.main import Lexer
from pylipt.token.main import TokenType, Token
from pylipt.utils.text import get_line_terminator
from pylipt.lexer.mapping import SINGLE_TOKEN_MAPPING, DOUBLE_TOKEN_MAPPING


def generate_nested_values(start_value: str, end_value: str, layers: int, depth: int) -> str:
    string = ""
    for layer in range(layers):
        string = string + start_value
        string = string + (start_value * depth) + (end_value * depth)
        string = string + end_value

    return string


class NestedFunctionTestCase(unittest.TestCase):
    def setUp(self):
        self.start_value = "a"
        self.end_value = "z"

    def generate_test(self, layers, depth, expected_format):
        result = generate_nested_values(self.start_value, self.end_value, layers, depth)
        expected = expected_format.format(self.start_value, self.end_value)
        self.assertEqual(result, expected)

    def test_even_flat_layers(self):
        self.generate_test(8, 0, "{0}{1}{0}{1}{0}{1}{0}{1}{0}{1}{0}{1}{0}{1}{0}{1}")

    def test_odd_flat_layers(self):
        self.generate_test(7, 0, "{0}{1}{0}{1}{0}{1}{0}{1}{0}{1}{0}{1}{0}{1}")

    def test_even_depth_layers(self):
        self.generate_test(3, 2, "{0}{0}{0}{1}{1}{1}{0}{0}{0}{1}{1}{1}{0}{0}{0}{1}{1}{1}")

    def test_odd_depth_layers(self):
        self.generate_test(2, 3, "{0}{0}{0}{0}{1}{1}{1}{1}{0}{0}{0}{0}{1}{1}{1}{1}")

    def test_single_flat_layer(self):
        self.generate_test(1, 0, "{0}{1}")

    def test_single_deep_layer(self):
        self.generate_test(1, 8, "{0}{0}{0}{0}{0}{0}{0}{0}{0}{1}{1}{1}{1}{1}{1}{1}{1}{1}")

    def test_no_layer(self):
        self.generate_test(0, 0, "")



class LexerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def generate_test(self, source: str, expected: list[Token], remove_eof_token: bool = True):
        lexer = Lexer(source)
        result = lexer.scan_tokens()

        if remove_eof_token:
            eof_token = result.pop()
            self.assertEqual(eof_token.token_type, TokenType.EOF, "Last token is not EOF token")

        self.assertEqual(result, expected)

    def test_parse_nested_brackets(self):
        depth = 8
        layers = 8
        expected = []

        line = generate_nested_values("[","]", layers, depth)

        for character in line:
            if character == "[":
                expected.append(Token(TokenType.LEFT_BRACKET, "[", None, 1))
            elif character == "]":
                expected.append(Token(TokenType.RIGHT_BRACKET, "]", None, 1))

        self.generate_test(line, expected)

    def test_parse_empty_source(self):
        self.generate_test("", [Token(TokenType.EOF, "", None, 1)], False)

    def test_parse_single_token(self):
        line = ""
        expected = []

        for lexeme, token_type in zip(SINGLE_TOKEN_MAPPING.keys(), SINGLE_TOKEN_MAPPING.values()):
            expected.append(Token(token_type, lexeme, None, 1))
            line = line + lexeme + " "

        self.generate_test(line, expected)

    def test_parse_double_token(self):
        line = ""
        expected = []

        for lexeme, token_type in zip(DOUBLE_TOKEN_MAPPING.keys(), DOUBLE_TOKEN_MAPPING.values()):
            # Test comments separately
            if token_type == TokenType.COMMENT:
                continue
            expected.append(Token(token_type, lexeme, None, 1))
            line = line + lexeme + " "

        self.generate_test(line, expected)

    def test_parse_whitespace(self):
        line = "( \n \t.\t <= ! )"
        expected = [
            Token(TokenType.LEFT_PAREN, '(', None, 1), Token(TokenType.DOT, '.', None, 2),
            Token(TokenType.LESS_EQUAL, '<=', None, 2), Token(TokenType.BANG, '!', None, 2),
            Token(TokenType.RIGHT_PAREN, ')', None, 2),
        ]
        self.generate_test(line, expected)

    def test_parse_single_line_comment(self):
        line = "//\tHello World- 0 () "
        expected = []
        self.generate_test(line, expected)

    def test_parse_inline_comments(self):
        line = f"() // Should not be parsed"
        expected = [
            Token(TokenType.LEFT_PAREN, '(', None, 1),
            Token(TokenType.RIGHT_PAREN, ')', None, 1),
        ]

        self.generate_test(line, expected)

    def test_parse_multiple_single_line_comments(self):
        line = f"// Hello World{get_line_terminator()}//testing ... +=!=/"
        expected = []
        self.generate_test(line, expected)

    def test_parse_multiple_lines(self):
        lines = f"(){get_line_terminator()}(){get_line_terminator()}()"
        expected = [
            Token(TokenType.LEFT_PAREN, '(', None, 1), Token(TokenType.RIGHT_PAREN, ')', None, 1),
            Token(TokenType.LEFT_PAREN, '(', None, 2), Token(TokenType.RIGHT_PAREN, ')', None, 2),
            Token(TokenType.LEFT_PAREN, '(', None, 3), Token(TokenType.RIGHT_PAREN, ')', None, 3)
        ]
        self.generate_test(lines, expected)


if __name__ == '__main__':
    unittest.main()

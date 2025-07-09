from pylipt.token.main import TokenType

SINGLE_TOKEN_MAPPING = {
    '(': TokenType.LEFT_PAREN,
    ')': TokenType.RIGHT_PAREN,
    '{': TokenType.LEFT_BRACE,
    '}': TokenType.RIGHT_BRACE,
    '[': TokenType.LEFT_BRACKET,
    ']': TokenType.RIGHT_BRACKET,
    ',': TokenType.COMMA,
    '.': TokenType.DOT,
    ';': TokenType.SEMICOLON,
    ':': TokenType.COLON,
    "'": TokenType.SINGLE_QUOTE,
    '"': TokenType.DOUBLE_QUOTE,

    '-': TokenType.MINUS,
    '+': TokenType.PLUS,
    '*': TokenType.STAR,
    '/': TokenType.SLASH,

    '!': TokenType.BANG,
    '=': TokenType.EQUAL,
    '>': TokenType.GREATER,
    '<': TokenType.LESS,
}


DOUBLE_TOKEN_MAPPING = {
    '!=': TokenType.BANG_EQUAL,
    '==': TokenType.EQUAL_EQUAL,
    '>': TokenType.GREATER_EQUAL,
    '<': TokenType.LESS_EQUAL,
}

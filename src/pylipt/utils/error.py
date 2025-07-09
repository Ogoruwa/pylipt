
class ErrorReporter:
    @classmethod
    def format_error(cls, line_no: int, line: str, message: str, token: str) -> str:
        return (
            f"Error: {message}\n"
            f"  {line_no} | {line}\n"
        )

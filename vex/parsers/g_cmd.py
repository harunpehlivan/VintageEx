from vex.parsers.parsing import RegexToken
from vex.parsers.parsing import Lexer
from vex.parsers.parsing import EOF


class GlobalLexer(Lexer):
    DELIMITER = RegexToken(r'[^a-zA-Z0-9 ]')
    WHITE_SPACE = ' \t'

    def __init__(self):
        self.delimiter = None

    def _match_white_space(self):
        while self.c != EOF and self.c in self.WHITE_SPACE:
            self.consume()

    def _match_pattern(self):
        buf = []
        while self.c not in [EOF, self.delimiter]:
            buf.append(self.c)
            if self.c == '\\':
                self.consume()
                if self.c in '\\':
                    # Don't store anything, we're escaping \.
                    self.consume()
                elif self.c == self.delimiter:
                    # Overwrite the \ we've just stored.
                    buf[-1] = self.delimiter
                    self.consume()

                if self.c == EOF:
                    break
            else:
                self.consume()

        return ''.join(buf)

    def _parse_long(self):
        self.delimiter = self.c
        self.consume()

        buf = [self._match_pattern()]
        self.consume()
        buf.append(self.string[self.cursor:])

        return buf

    def _do_parse(self):
        if self.c not in self.DELIMITER:
            raise SyntaxError("expected delimiter, got '%s'" % self.c)
        return self._parse_long()


def split(s):
    return GlobalLexer().parse(s)

import re

EOF = -1

class Lexer(object):
    def __init__(self):
        self.c = None # current character
        self.cursor = 0
        self.string = None

    def _reset(self):
        self.c = None
        self.cursor = 0
        self.string = None

    def consume(self):
        self.cursor += 1
        self.c = EOF if self.cursor >= len(self.string) else self.string[self.cursor]

    def _do_parse(self):
        pass

    def parse(self, string):
        if not isinstance(string, basestring):
            raise TypeError("Can only parse strings.")
        self._reset()
        self.string = string
        self.c = EOF if not string else string[0]
        return self._do_parse()


class RegexToken(object):
    def __init__(self, value):
        self.regex = re.compile(value)

    def __contains__(self, value):
        return self.__eq__(value)

    def __eq__(self, other):
        return bool(self.regex.match(other))

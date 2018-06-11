import re

from .tokenizer.tokens import *

class RegexMatcher(object):

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, document):
        out = []
        for token in document.body:
            if isinstance(token, Text):
                if re.match(self.pattern, token.value):
                    out.append(token)
            elif isinstance(token, Command):
                for arg in token.args:
                    out += self.match(arg)
            elif isinstance(token, Math):
                out += self.match(token.body)

        return out
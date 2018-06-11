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

class CommandMatcher(object):

    def __init__(self,name, args = []):
        self.name = name
        self.args = args

    def match(self, document):
        out = []
        for token in document.body:
            if isinstance(token, Command):
                if token.name == self.name:
                    all_args_match = True
                    for matcher, argument in zip(self.args, token.args):
                        if len(matcher.match(argument)) == 0:
                            all_args_match = False

                    if all_args_match:
                        out.append(token)
                
                for arg in token.args:
                    out += self.match(arg)

            elif isinstance(token, Math):
                out += self.match(token.body)
                
        return out
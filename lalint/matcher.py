import re
import abc

from .tokenizer.tokens import *

class Matcher(abc.ABC):

    def match(self, document):
        out = []
        for token in document.body:
            if self.token_matches(token):
                out.append(token)
            
            if isinstance(token, Command):
                for arg in token.args:
                    out += self.match(arg)
            elif isinstance(token, Math):
                out += self.match(token.body)

        return out

    @abc.abstractmethod
    def token_matches(self, token):
        """
        Returns true if the token should match this matcher.
        """
        pass

class RegexMatcher(Matcher):

    def __init__(self, pattern):
        self.pattern = pattern

    def token_matches(self, token):
        return isinstance(token,Text) and re.search(self.pattern, token.value)

class CommandMatcher(Matcher):

    def __init__(self,name, args = []):
        self.name = name
        self.args = args

    def token_matches(self, token):
        if isinstance(token, Command):
            if token.name == self.name:
                all_args_match = True
                for matcher, argument in zip(self.args, token.args):
                    if len(matcher.match(argument)) == 0:
                        all_args_match = False

                if all_args_match:
                    return True
                
        return False
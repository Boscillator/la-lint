import importlib
from .matcher import RegexMatcher

class LintException(Exception):
    
    def __init__(self, rule):
        self.rule = rule

class ExpectedException(LintException):

    def __repr__(self):
        return f"Document is invalide. Required rule {self.rule} did not match."

class DisallowedException(LintException):

    def __repr__(self):
        return f"Document is invalide. Disallowed rule {self.rule} matched."

class Rules(object):

    def __init__(self, required, disallowed):
        self.required = required
        self.disallowed = disallowed

    def test(self, document):
        for rule_name, matcher in self.required.items():
            result = matcher.match(document)
            print("require", result, rule_name)
            if len(result) == 0:
                raise ExpectedException(rule_name)
            
        for rule_name, matcher in self.disallowed.items():
            result = matcher.match(document)
            print("disallow", result)
            if len(result) != 0:
                raise DisallowedException(rule_name)

def load_rules(package_name):
    rules_package = importlib.import_module(package_name)
    required = rules_package.require or {}
    disallowed = rules_package.disallow or {}
    return Rules(required,disallowed)



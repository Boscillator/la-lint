import importlib
import inspect
from .matcher import RootMatcher
from .tokenizer.tokens import Document


class Rules(object):

    def __init__(self, package):
        #Get a list of things that subclass rule in the package
        items = [getattr(package,item) for item in dir(package)]
        classes = [item for item in items if inspect.isclass(item)]
        class_rules = [c() for c in classes if issubclass(c,Rule) and c != Rule]
        functional_rules = [r for r in items if isinstance(r,Rule)]
        self.rules = class_rules + functional_rules
        print(f"Rules.__init__({self.rules})")

    def test(self, document):
        """
        Test all the rules
        """
        for rule in self.rules:
            matches = rule.matcher.match(document)
            if isinstance(matches, Document):
                print("checking", rule, matches)
                rule.check(matches)
            else:
                for match in matches:
                    rule.check(match)

class Rule(object):

    matcher = RootMatcher()

    def __init__(self):
        self._body = None
        self.as_decorator = False

    def __call__(self, body):
        """
        If this is being used as a docorator, it will be called
        """
        self._body = body
        self.as_decorator = True
        return self

    def check(self, match):
        """
        Called to see of a match is ok by this rule. Is either overriden in subclass, or added by __call__ when used as decorator.
        Raises assertion errors if this does not match
        """
        print("check")
        self._body(match)

def load_rules(package_name):
    rules_package = importlib.import_module(package_name)
    return Rules(rules_package)

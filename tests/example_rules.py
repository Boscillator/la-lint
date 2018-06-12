from lalint import Rule, CommandMatcher

@Rule()
def dissallow_letter_a(document):
    print(document)
    assert 'a' not in document.text

@Rule()
def require_letter_b(document):
    assert 'b' in document.text

class FooMustHaveCArgument(Rule):
    matcher = CommandMatcher('foo')

    def check(self, match):
        assert match.args[0] == 'c'

    def suggest(self, match):
        return r"\foo{c}"
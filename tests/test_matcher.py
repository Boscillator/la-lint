from lalint.matcher import *
from lalint.tokenizer.tokens import *

def test_match_regex():
    document = Document([
        Text("Hello")
    ])

    matcher = RegexMatcher(".*")

    assert matcher.match(document) == [
        Text("Hello")
    ]

def test_match_text_regex_multi():
    document = Document([
        Text("Hello"),
        Text("Human"),
        Text("World")
    ])

    matcher = RegexMatcher("H.*")

    assert matcher.match(document) == [
        Text("Hello"),
        Text("Human")
    ]

def test_recursive_regex_match():
    document = Document([
        Command("bold", args=[Document([
            Text("Hello")
        ])]),
        Text("Human"),
        Text("World")
    ])

    matcher = RegexMatcher("H.*")

    assert matcher.match(document) == [
        Text("Hello"),
        Text("Human")
    ]

def test_recursive_regex_match_math():
    document = Document([
        Math(Document([
            Text("Hello")
        ])),
        Text("Human"),
        Text("World")
    ])

    matcher = RegexMatcher("H.*")

    assert matcher.match(document) == [
        Text("Hello"),
        Text("Human")
    ]
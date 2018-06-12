import re

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


def test_regex_matcher_pattern():
    document = Document([
        Text("Hello")
    ])

    pattern = re.compile('.*')
    matcher = RegexMatcher(pattern)

    assert matcher.match(document) == [
        Text("Hello")
    ]


def test_command_matcher():
    document = Document([
        Command('foo'),
        Command('bar')
    ])

    matcher = CommandMatcher('foo')

    assert matcher.match(document) == [
        Command('foo')
    ]


def test_command_matcher_with_args():
    document = Document([
        Command('foo', args=[
            Document([
                Text('a')
            ])
        ]),
        Command('foo', args=[
            Document([
                Text('b')
            ])
        ])
    ])

    matcher = CommandMatcher('foo', args=[
        RegexMatcher('a')
    ])

    assert matcher.match(document) == [
        Command('foo', args=[
            Document([
                Text('a')
            ])
        ])
    ]

def test_command_matcher_recursive():
    document = Document([
        Command("foo", args=[Document([
            Command("foo")
        ])]),
        Command("foo"),
        Command("bar")
    ])

    matcher = CommandMatcher('foo')

    assert matcher.match(document) == [
        Command("foo", args=[Document([
            Command("foo")
        ])]),
        Command('foo'),
        Command('foo')
    ]

def test_command_matcher_in_math():
    document = Document([
        Math(Document([
            Command('foo')
        ]))
    ])

    matcher = CommandMatcher('foo')

    assert matcher.match(document) == [
        Command('foo')
    ]

def test_regex_matcher_not_first():
    document = Document([
        Text('abc')
    ])

    matcher = RegexMatcher('b')

    assert matcher.match(document) == [
        Text('abc')
    ]

def test_root_matcher():
    document = Document([
        Text('foo')
    ])

    matcher = RootMatcher()

    assert matcher.match(document) == Document([
        Text('foo')
    ])
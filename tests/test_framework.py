import pytest

from lalint.framework import *
from lalint.tokenizer.tokens import *

@pytest.fixture
def example_rules():
    return load_rules('tests.example_rules')

def test_import():
    load_rules('tests.example_rules')

def test_execute_rules_pass(example_rules):
    document = Document([
        Text('boo')
    ])

    #Assert returns no exception
    example_rules.test(document)

def test_execute_rules_missing_required(example_rules):
    document = Document([
        Text('oo')
    ])

    with pytest.raises(AssertionError):
        example_rules.test(document)

def test_execute_rules_has_disallowed():
    print("test")
    example_rules = load_rules('tests.example_rules')
    document = Document([
        Text('abc')
    ])

    with pytest.raises(AssertionError):
        example_rules.test(document)

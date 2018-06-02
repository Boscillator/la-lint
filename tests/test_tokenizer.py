from lalint.tokenizer import *

def test_single_command():
    assert tokenize(r'\mycommand') == [Command('mycommand')]

def test_two_commands():
    assert tokenize(r'\mycommand\myothercommand') == [
        Command('mycommand'),
        Command('myothercommand')
        ]

def test_command_with_brace_arg():
    src = r'\test{a}'
    assert tokenize(src) == [
        Command(
            'test',
            brace_args = ['a']
        )
    ]

def test_many_brace_args():
    assert tokenize(r'\test{a}{b}') == [
        Command(
            'test',
            brace_args = ['a','b']
        )
    ]

def test_brace_args_with_white_space():
    assert tokenize(r'\test{a long argument}') == [
        Command(
            'test',
            brace_args = ['a long argument']
        )
    ]

def test_nested_brace_args():
    assert tokenize(r'\outer{\inner}') == [
        Command('outer', brace_args = [
            Command('inner')
        ])
    ]

def test_nested_brace_args_with_body():
    assert tokenize(r'\outer{text \inner}') == [
        Command('outer', brace_args = [
            'text ', Command('inner')
        ])
    ]

def test_nested_brace_args_with_body_2():
    assert tokenize(r'\outer{\inner text}') == [
        Command('outer', brace_args = [
            Command('inner'),'text'
        ])
    ]

def test_body_then_command():
    assert tokenize(r'body \command') == [
        'body ',
        Command('command')
    ]

def test_command_then_body():
    assert tokenize(r'\command body') == [
        Command('command'),
        'body'
    ]

def test_two_command_inside_command():
    assert tokenize(r'\outer{\innerone \innertwo}') == [
        Command('outer', brace_args = [
            Command('innerone'),
            Command('innertwo')
        ])
    ]
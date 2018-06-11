from lalint.tokenizer import tokenize
from lalint.tokenizer.tokens import *

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
            args=[['a']]
        )
    ]


def test_many_brace_args():
    assert tokenize(r'\test{a}{b}') == [
        Command(
            'test',
            args=[['a'], ['b']]
        )
    ]


def test_brace_args_with_white_space():
    assert tokenize(r'\test{a long argument}') == [
        Command(
            'test',
            args=[['a long argument']]
        )
    ]


def test_nested_brace_args():
    assert tokenize(r'\outer{\inner}') == [
        Command('outer', args=[
            [Command('inner')]
        ])
    ]


def test_nested_brace_args_with_body():
    assert tokenize(r'\outer{text \inner}') == [
        Command('outer', args=[
            ['text ', Command('inner')]
        ])
    ]


def test_nested_brace_args_with_body_2():
    assert tokenize(r'\outer{\inner text}') == [
        Command('outer', args=[
            [Command('inner'), 'text']
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
        Command('outer', args=[
            [Command('innerone'),
             Command('innertwo')]
        ])
    ]


def test_inner_body_and_two_commands():
    src = r"""
    \outer{
        \inner1{a}
        hello
        \inner2
    }
    """

    tokens = tokenize(src)
    print(tokens)
    assert tokens == [
        Command('outer', args=[
            [Command('inner1', args=[['a']]),
             'hello\n        ',
             Command('inner2')]
        ])
    ]


def test_command_with_number():
    assert tokenize(r"\hello1") == [
        Command('hello1')
    ]


def test_mulitline_brace_arg():
    src = r"""
    \outer{
        \inner
    }
    """
    assert tokenize(src) == [
        Command('outer', args=[
            [Command('inner')]
        ])
    ]


def test_multiple_brace_args():
    assert tokenize(r"\command{a}{b}") == [
        Command('command', args=[
            ['a'],
            ['b']
        ])
    ]


def test_multiple_brace_args_with_command():
    src = r"""
    \outer{a}{
        \inner
        some body text
    }
    """

    res = tokenize(src)
    assert res == [
        Command('outer', [
            ['a'],
            [
                Command('inner'),
                'some body text\n    '
            ]
        ])
    ]


def test_bracket_arg():
    assert tokenize(r"\command[value]") == [
        Command('command', args=[
            ['value']
        ])
    ]


def test_brace_and_bracket():
    assert tokenize(r"\command{a}[b]") == [
        Command('command', args=[
            ['a'],
            ['b']
        ])
    ]


def test_bracket_and_brace():
    assert tokenize(r"\command[a]{b}") == [
        Command('command', args=[
            ['a'],
            ['b']
        ])
    ]


def test_inline_math():
    assert tokenize(r"$1+1$") == [
        Math(["1+1"])
    ]


def test_inline_math_with_command():
    assert tokenize(r"$\frac{a}{b} + 1$") == [
        Math([
            Command('frac', args=[['a'], ['b']]),
            '+ 1'
        ])
    ]


def test_two_inline_maths():
    assert tokenize(r"$1$ and $2$") == [
        Math(['1']),
        'and ',
        Math(['2'])
    ]


def test_displayed_equation():
    assert tokenize(r"$$1$$") == [
        Math(['1'], inline=False)
    ]


def test_displayed_math_with_command():
    assert tokenize(r"$$\frac{a}{b} + 1$$") == [
        Math([
            Command('frac', args=[['a'], ['b']]),
            '+ 1'
        ], inline=False)
    ]


def test_inline_and_displayed_maths():
    assert tokenize(r"$1$ and $$2$$") == [
        Math(['1']),
        'and ',
        Math(['2'], inline=False)
    ]

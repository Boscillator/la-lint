import click
from .tokenizer import tokenize
from .framework import load_rules

@click.command()
@click.argument('rules', nargs=-1)
@click.argument('file', type=click.File('r'))
def lint(rules, file):
    src = file.read()
    document = tokenize(src)

    for rule in rules:
        load_rules(rule).test(document)
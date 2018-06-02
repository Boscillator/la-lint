from dataclasses import dataclass, field
from typing import List
from pyparsing import *

@dataclass
class Token:
    pass

@dataclass
class Command(Token):
    name:str
    brace_args:List[Token] = field(default_factory=list)
    braket_args:List[Token] = field(default_factory=list)

slash = Literal("\\")
lbrace = Literal("{")
rbrace = Literal("}")

document = Forward()

brace_arg = lbrace + document.setResultsName('body') + rbrace
brace_arg.setParseAction(lambda t: t.body)

arg_list = ZeroOrMore(brace_arg)

def handelCommand(t):
    brace_args = [arg for arg in t.args]

    return Command(
        name = t.name,
        brace_args = brace_args
    )

command = slash + Word(alphas).setResultsName('name') + Optional(arg_list).setResultsName('args')
command.setParseAction(handelCommand)

special_char = slash | lbrace | rbrace
word = ~special_char + Regex(r'[\s\S]')
text = Combine(OneOrMore(word))

document << Group(ZeroOrMore( command | text ))

def tokenize(source_str):
    res = document.parseString(source_str)
    return res.asList()[0]

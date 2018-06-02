from collections import namedtuple
from typing import List, Any
from pyparsing import *

Command = namedtuple('Command',['name','args'])
Command.__new__.__defaults__ = ([],)

InlineMath = namedtuple('InlineMath', ['body'])

slash = Literal("\\")
lbrace = Literal("{")
rbrace = Literal("}")

document = Forward()

brace_arg = lbrace + document.setResultsName('body') + rbrace
brace_arg.setParseAction(lambda t: t.body)

lbracket = Literal("[")
rbracket = Literal("]")
bracket_arg = lbracket + document.setResultsName('body') + rbracket
bracket_arg.setParseAction(lambda t: t.body)

argument = brace_arg | bracket_arg

arg_list = ZeroOrMore(Group(argument))
#arg_list.setParseAction(lambda t: print(t))

def handelCommand(t):

    cmd = Command(
        name = t.name,
        args = t.args.asList()
    )
    return cmd

command = slash + Word(alphanums).setResultsName('name') + Optional(arg_list).setResultsName('args')
command.setParseAction(handelCommand)

dollar = Literal("$")
inlineMath = dollar + document.setResultsName("body") + dollar
inlineMath.setParseAction(lambda t: InlineMath(t.body.asList()))

special_char = slash | lbrace | rbrace | lbracket | rbracket | dollar
word = ~special_char + Regex(r'[\s\S]')
text = Combine(OneOrMore(word))

document << Group(ZeroOrMore( command | text | inlineMath))

def tokenize(source_str):
    res = document.parseString(source_str)
    return res.asList()[0]

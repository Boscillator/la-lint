"""PyParsing Grammar decleration"""
from pyparsing import *
from .tokens import *

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

arg_list = ZeroOrMore(argument)
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
doubleDollar = Literal("$$")

inlineMath = ~doubleDollar + dollar + document.setResultsName("body") + dollar
inlineMath.setParseAction(lambda t: Math(t.body))

displayedMath = doubleDollar + document.setResultsName("body") + doubleDollar
displayedMath.setParseAction(lambda t :Math(t.body, inline=False))

special_char = slash | lbrace | rbrace | lbracket | rbracket | dollar 
word = ~special_char + Regex(r'[\s\S]')
text = Combine(OneOrMore(word))
text.setParseAction(lambda t: (Text(''.join(t.asList()))))

document << Group(ZeroOrMore( command | text | inlineMath | displayedMath )).setResultsName('body')
document.setParseAction(lambda t: Document(t.body.asList()))
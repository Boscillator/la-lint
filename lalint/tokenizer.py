from collections import namedtuple
from pyparsing import *

# Command = namedtuple('Command',['name','args'])
# Command.__new__.__defaults__ = ([],)

class Document(object):
    """Repersents a selection of LaTeX"""

    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return str(self.body)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.body == other.body
        elif type(other) == list:
            return self.body == other
        else:
            return False

class Text(object):
    """Plain text in LaTeX"""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

    def __eq__(self,other):
        if type(other) == type(self):
            return self.value == other.value
        else:
            return self.value == other

class Command(object):
    r"""
    A Latex Command (ie `\section`)

    Attributes
    ----------
    name : str
        The text that comes directly after the backslash
    args : List[Document], optional
        The list of args to the command. Each argument is a list of strings and Commands and Maths which represent the body of that command.
    """

    def __init__(self, name, args = []):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"<Command name='{self.name}' args='{self.args}'>"
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        return self.name == other.name and self.args == other.args

class Math(object):
    """
    Represents some math

    Attributes
    ----------
    body : Document
        The content inside the math
    inline : bool
        True if this is inline ($math$), False if this is displayed ($$math$$)
    """

    def __init__(self, body, inline = True):
        self.body = body
        self.inline = inline
    
    def __repr__(self):
        return f"<Math {'inline' if self.inline else ''} body='{self.body}'>"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.body == other.body and self.inline == other.inline

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

def tokenize(source_str):
    """
    Converts a latex document into a Document
    Parameters
    ----------
    source_str : str
        A string to convert into a document
    Returns
    -------
    Document
        A document representing source_str
    """
    res = document.parseString(source_str)
    return res.asList()[0]

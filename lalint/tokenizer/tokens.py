"""Token classes for the tokenizer"""

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
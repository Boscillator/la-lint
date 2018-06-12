import pytest
from lalint.tokenizer.tokens import *

def test_attach_parrents():

    hello = Text("Hello")
    world = Text("World")
    hello_doc = Document([hello, world])
    foo = Command("Foo", args=[hello_doc])

    document = Document([foo])

    document.attach_parents()

    assert hello.parent == hello_doc
    assert world.parent == hello_doc
    assert hello_doc.parent == foo
    assert foo.parent == document
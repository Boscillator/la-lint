from lalint.tokenizer.tokens import *

def test_text():
    document = Document([
        Text("foo"),
        Text("bar")
    ])

    assert document.text == "foobar"

def test_text_recursive():
    document = Document([
        Command("command", args=[
            Document([
                Text("foo")
            ])
        ]),
        Text("bar")
    ])

    assert document.text == "foobar"

def test_replace():
    text = Text('foo')
    document = Document([
        text
    ])

    document.replace(text, Text('bar'))

    assert document == Document([
        Text('bar')
    ])
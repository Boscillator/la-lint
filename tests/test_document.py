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
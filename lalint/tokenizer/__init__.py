from ._grammar import document

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

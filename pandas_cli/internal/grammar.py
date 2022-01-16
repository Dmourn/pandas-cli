import re

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.contrib.regular_languages.compiler import compile
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from prompt_toolkit.contrib.regular_languages.lexer import GrammarLexer
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.styles import Style

"""
This is not good but i dont want to delete it.
"""

verb_list = ['exit', 'quit', 'load', 'show', 'cols', 'order', 'search', 'reset', 'save', 'sort', 'multi']
def create_grammar():
    return compile(
        r"""
        (\s* (?P<verb1>[a-z]+) \s+ (?P<noun1>[a-zA-Z0-9.]+) \s*)
    """
    )

def create_lexer():
    example_style = Style.from_dict(
        {
            "verb": "#33aa33 bold",
            "noun": "#10a0f0 bold",
            "trailing-input": "bg:#662222 #ffffff",
        }
    )


    g = create_grammar()

    lexer = GrammarLexer(g, 
            lexers={
            "verb1": SimpleLexer("class:verb"),
            "noun1": SimpleLexer("class:noun"),
            },
        )

    completer = GrammarCompleter(g,
        {
        "verb1": WordCompleter(verb_list),
        },
    )
    return lexer,example_style, completer


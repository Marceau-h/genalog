# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# ---------------------------------------------------------

import re
from io import StringIO

END_OF_TOKEN = {" ", "\t", "\n"}
NON_ASCII_REPLACEMENT = "_"
spaces = re.compile(r"((\s)+)")

def remove_non_ascii(token, replacement=NON_ASCII_REPLACEMENT):
    """Remove non ascii characters in a token

    Arguments:
        token (str) : a word token
        replacement (str, optional) : a replace character for non-ASCII characters.
                                      Defaults to ``NON_ASCII_REPLACEMENT``.
    Returns:
        str -- a word token with non-ASCII characters removed
    """
    # Remove non-ASCII characters in the token
    ascii_token = str(token.encode("utf-8").decode("ascii", "ignore"))
    # If token becomes an empty string as a result
    if len(ascii_token) == 0 and len(token) != 0:
        ascii_token = replacement  # replace with a default character
    return ascii_token


def tokenize(s):
    """Tokenize string

    Arguments:
        s (str) : aligned string

    Returns:
        a list of tokens
    """
    # split alignment tokens by spaces, tabs and newline (and excluding them in the tokens)
    return s.split()


def tokenize_and_remember_linebreaks(s):
    """Tokenize string and remember the linebreaks

    Arguments:
        s (str) : aligned string

    Returns:
        a list of tokens and the dict of the indexes (in the tokens) where linebreaks are present
        with the number of linebreaks in the line as the value
    """
    # split alignment tokens by spaces, tabs and newline (and excluding them in the tokens)
    tokens = s.split()
    all_spaces = [space[0] for space in spaces.findall(s)]
    # linebreaks = [i for i, c in enumerate(all_spaces) if all(c == "\n" for c in c)]
    linebreaks = {
        i: sum(e == "\n" for e in c) for i, c in enumerate(all_spaces)
    }
    linebreaks = {
        k: v for k, v in linebreaks.items() if v > 0
    }
    return tokens, linebreaks


def join_tokens(tokens):
    """Join a list of tokens into a string

    Arguments:
        tokens (list) : a list of tokens

    Returns:
        a string with space-separated tokens
    """
    return " ".join(tokens)


def join_tokens_with_spacing(tokens, linebreaks):
    """Join a list of tokens inserting linebreaks at the specified indexes
    Intended to be used with the output of ``tokenize_and_remember_linebreaks``

    Arguments:
        tokens (list) : a list of tokens
        linebreaks (dict) : a dict of the indexes (in the tokens) where linebreaks are present
                            with the number of linebreaks in the line as the value

    Returns:
        a string with space-separated tokens and re inserted linebreaks
    """
    # join tokens with spaces
    # return "".join(t + "\n" if i in spacing else t + " " for i, t in enumerate(tokens))[:-1]
    s = StringIO()
    for i, t in enumerate(tokens):
        s.write(t)
        if i in linebreaks:
            s.write("\n" * linebreaks[i])
        else:
            s.write(" ")
    return s.getvalue().strip()


def _is_spacing(c):
    """ Determine if the character is ignorable """
    return True if c in END_OF_TOKEN else False


def split_sentences(text, delimiter="\n"):
    """ Split a text into sentences with a delimiter"""
    return re.sub(r"(( /?[.!?])+ )", rf"\1{delimiter}", text)


def is_sentence_separator(token):
    """ Returns true if the token is a sentence splitter """
    return re.match(r"^/?[.!?]$", token) is not None

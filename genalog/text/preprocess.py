# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# ---------------------------------------------------------

import re
from io import StringIO

END_OF_TOKEN = {" ", "\t", "\n"}
NON_ASCII_REPLACEMENT = "_"
spaces = re.compile(r"\s")


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

def tokenize_and_remember_spacing(s):
    """Tokenize string and remember the spacing

    Arguments:
        s (str) : aligned string

    Returns:
        a list of tokens and a the list of the trimmed spacing
    """
    # tokens = []
    # spacing = []
    # token = StringIO()
    # for c in s:
    #     if _is_spacing(c):
    #         if token:
    #             tokens.append(token.getvalue())
    #             token = StringIO()
    #         spacing.append(c)
    #     else:
    #         token.write(c)
    # if token:
    #     tokens.append(token.getvalue())
    # return tokens, spacing
    spaces_ = spaces.findall(s)
    tokens = spaces.split(s)
    if len(tokens) != len(spaces_):
        if len(tokens) == len(spaces_) + 1:
            spaces_.append("")
        else:
            raise ValueError("Number of tokens and spaces do not match")
    return tokens, spaces_


def join_tokens(tokens):
    """Join a list of tokens into a string

    Arguments:
        tokens (list) : a list of tokens

    Returns:
        a string with space-separated tokens
    """
    return " ".join(tokens)

def join_tokens_with_spacing(tokens, spacing):
    """Join a list of tokens with spacing into a string

    Arguments:
        tokens (list) : a list of tokens
        spacing (list) : a list of spacing

    Returns:
        a string with tokens and spacing
    """
    return "".join([f"{token}{space}" for token, space in zip(tokens, spacing)])


def _is_spacing(c):
    """ Determine if the character is ignorable """
    return True if c in END_OF_TOKEN else False


def split_sentences(text, delimiter="\n"):
    """ Split a text into sentences with a delimiter"""
    return re.sub(r"(( /?[.!?])+ )", rf"\1{delimiter}", text)


def is_sentence_separator(token):
    """ Returns true if the token is a sentence splitter """
    return re.match(r"^/?[.!?]$", token) is not None

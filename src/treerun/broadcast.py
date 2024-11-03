#!/usr/bin/python

text_width = 80
tab_width = 4
line_symbol = '\u2014'

def horizontal_line():
    print(text_width*line_symbol)

def header(string):
    """Simple header with lines abive and below (em-dash: U+2014)."""
    horizontal_line()
    print(string)
    horizontal_line()

def whitespace(strings, max_length=None):
    """Returns a dictionary with the same keys as the original dictionary 
    but with a number of spaces as values instead.

    The number of spaces corresponds to the difference between all keys and 
    the longest key (+tab_width).
    """
    if type(strings) == list:
        lengths = [len(string) for s in strings]
        if max_length == None:
            longest_string = max(lengths)
        else:
            longest_string = max_length+tab_width
        spaces = {string:(longest_string-length) for string, length in zip(strings, lengths)}

    elif type(strings) == dict:
        # Get longest name
        name_lengths = {key:len(key) for key in strings}
        if max_length == None:
            longest_string = name_lengths[max(name_lengths, key=name_lengths.get)]+tab_width
        else:
            longest_string = max_length+tab_width

        # Create whitespace map
        spaces = {key:(longest_string-val)*' ' for key,val in name_lengths.items()}

    return spaces, longest_string

def tabulate(data:dict, max_length=None) -> None:
    """Tabulates keys and values of a given dictionary into two columns."""
    assert type(data) == dict, ValueError('The \'tabulate\' method takes a dictionary as input.')
    space, _ = whitespace(data, max_length=max_length)
    for key,val in data.items():
        print(f'{key}{space[key]}{val}')
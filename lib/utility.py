#A place to stick general utility functions.

def prepend_exclamation(input):
    
    output = "!" + input
    
    return output

def append_value(input):

    output = input + "_value"

    return output

def simplify_alias(full_alias):

    return full_alias.split('_')[0]
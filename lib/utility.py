import dearpygui.dearpygui as dpg
import random

#A place to stick general utility functions.

def prepend_exclamation(input):
    
    output = "!" + input
    
    return output

def append_value(input):

    output = input + "_value"

    return output

def simplify_alias(full_alias):

    return full_alias.split('_')[0]

def create_rand_id(node_type):
    
    random_id = random.randint(0, 50000)
    
    while dpg.does_item_exist(str(random_id) + node_type):
            
            random_id = random.randint(0, 50000)

def fancy_class_name(obj):
    name = obj.__class__.__name__
    name = name.replace('node', '').replace('func', '')
    name = name.replace('_', ' ').title()
    return name
# Copyright 2021 LuminousLizard
# Licensed under the MIT-License

import dearpygui.dearpygui as dpg
from .. lib.fusionAddInUtils.general_utils import log
from .. lib.node_functions.node_input import all_node_inputs
from .. lib.node_functions.link import Link
from .. lib.function_node_dict import function_node_dict
from .node_dict_static import node_dict_static
from .utility import *
import orjson

LinkList = []

# Function for updating all interconnected nodes if a link was created or a value has changed
def func_chain_update(sender, app_data):
    # sender = "NodeEditor" for links
    # sender = attribute tag for changed values
    # data = connected node attributes for links as list
    # data = value for changed variable
    
    input_alias_full = dpg.get_item_alias(app_data[0])

    output_alias_full = dpg.get_item_alias(app_data[1])
    
    data = ()

    if type(app_data) == tuple:
        data = (input_alias_full, output_alias_full)
    else:
        data = app_data

    input_alias = simplify_alias(input_alias_full)

    output_alias = simplify_alias(output_alias_full)

    if type(data) == tuple:

        dpg.add_node_link(data[0], data[1], parent=sender)

        LinkList.append(data)

        start = function_node_dict[input_alias]

        if not (output_alias in start.outputs):

            start.outputs.append(output_alias)

        node_input = all_node_inputs[output_alias_full]

        output_alias = dpg.get_item_alias(app_data[1])


        node_input.linked = True

        start.links.append(Link(start=input_alias_full, end=output_alias_full))

        try:

            dpg.disable_item(data[1] + "_value") #disable the input being linked into

        except:

            pass

        log("update started")

        start.update(sender = sender)

        log(f"link finished")

def node_destroyed(alias):
    
    #Run the nodes delete method

    node_func = function_node_dict[alias]

    node_func.delete()

    #Cleanup all references to the node function

    del function_node_dict[alias]

    entries_to_delete = []

    for key in all_node_inputs.keys():

        if alias in key:

            entries_to_delete.append(key)

    for entry in entries_to_delete:

        del all_node_inputs[entry]

def func_link_destroyed(sender, data):

    #get full alias

    input_full_alias = dpg.get_item_alias(dpg.get_item_configuration(data)["attr_1"])

    output_full_alias = dpg.get_item_alias(dpg.get_item_configuration(data)["attr_2"])

    #delete link between node functions
    
    input_alias = simplify_alias(input_full_alias)

    output_alias = simplify_alias(output_full_alias)

    next = function_node_dict[output_alias]

    start = function_node_dict[input_alias]

    start.outputs.remove(output_alias)

    #delete links to node inputs

    link = all_node_inputs[output_full_alias]

    for l in start.links:

        log(f"{l}")

    link.linked = False

    link.parameter = [0] #reinitialize as a zero value object but maybe we ought to change this at some point

    start.links = [link for link in start.links if link.end != output_full_alias] #remove the links being deleted

    try:

        log("trying to update")

        next.update(sender = sender)

    except:

        log("failed update continueing")

    # Enable target slot

    try:

        log("trying to reinable node")

        dpg.enable_item(output_full_alias + "_value")

    except:

        log("failed to reinable node")

    # Removing the old connection from the LinkList

    LinkList.remove((input_full_alias, output_full_alias))

    # Delete link
    dpg.delete_item(data)

def save_state(sender, app_data):
    
    open("C:/temp/gradient.json", "w").close()

    for n in function_node_dict.values():

        n.update_ui_pos()

    with open('C:/temp/gradient.json', 'a') as json_file:

        json_bytes = orjson.dumps(function_node_dict, option=
                                   orjson.OPT_SERIALIZE_NUMPY |
                                   orjson.OPT_APPEND_NEWLINE)

        json_utf = json_bytes.decode()

        json_file.write(json_utf)

def load_state_relink(link, sender):

    #prevent double linking
    if not dpg.does_alias_exist(link.start + link.end):

        dpg.add_node_link(link.start, link.end, parent = sender, tag = link.start + link.end)

        LinkList.append(link.start)

        LinkList.append(link.end)

        if dpg.does_alias_exist(link.end + "_value"):

            try:

                dpg.disable_item(link.end + "_value") #disable the input being linked into

            except:

                log('caught disable error node input error')

def load_state(sender, app_data):

    with open("C:/temp/gradient.json", "r") as file:

        json = orjson.loads(file.read())

        for key in json.keys():

            _node_name = ''.join(char for char in key if char.isalpha())

            node_group = node_dict_static[_node_name]

            node_func = node_group.load_state(json[key])

            node_group.add_from_func(node_func)

            node_func.sync_ui()

            function_node_dict[key] = node_func

        for node_func in list(function_node_dict.values()):

            for _link in node_func.links:

                _sender = "NodeEditor"

                load_state_relink(link = _link, sender =_sender)
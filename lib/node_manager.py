# Copyright 2021 LuminousLizard
# Licensed under the MIT-License

import dearpygui.dearpygui as dpg
from .. lib.fusionAddInUtils.general_utils import log
from .. lib.node_functions.node_input import all_node_inputs
from .. lib.node_functions.node_output import NodeOutput, all_node_outputs
from .. lib.function_node_dict import function_node_dict
from .node_dict_static import node_dict_static
from .utility import *
import json
import orjson

LinkList = []

# Function for updating all interconnected nodes if a link was created or a value has changed
def func_chain_update(sender, app_data):
    # sender = "NodeEditor" for links
    # sender = attribute tag for changed values
    # data = connected node attributes for links as list
    # data = value for changed variable

    input_alias_full = dpg.get_item_alias(app_data[1])

    output_alias_full = dpg.get_item_alias(app_data[0])
    
    data = ()

    if type(app_data) == tuple:
        data = (input_alias_full, output_alias_full)
    else:
        data = app_data

    output_alias = simplify_alias(output_alias_full)

    if type(data) == tuple:

        dpg.add_node_link(data[0], data[1], parent=sender)

        LinkList.append(data)

        start = function_node_dict[output_alias]

        node_input = all_node_inputs[input_alias_full]

        node_output = all_node_outputs[output_alias_full]

        node_input.linked = True

        node_output.links.append(input_alias_full)

        try:

            dpg.disable_item(data[0] + "_value") #disable the input being linked into

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

    del function_node_dict[alias] #remove the node from the function node dict

    entries_to_delete_inputs = []

    for key in all_node_inputs.keys():

        if alias in key:

            entries_to_delete_inputs.append(key)

    entries_to_delete_outputs = []

    for key in all_node_outputs.keys():

        if alias in key:

            entries_to_delete_outputs.append(key)

    for entry in entries_to_delete_inputs:

        del all_node_inputs[entry]

    for entry in entries_to_delete_outputs:

        del all_node_outputs[entry]

def func_link_destroyed(sender, data):

    #get full alias

    input_full_alias = dpg.get_item_alias(dpg.get_item_configuration(data)["attr_1"])

    output_full_alias = dpg.get_item_alias(dpg.get_item_configuration(data)["attr_2"])

    #delete link between node functions
    
    input_alias = simplify_alias(input_full_alias)

    # output_alias = simplify_alias(output_full_alias)

    next = function_node_dict[input_alias]

    output = all_node_outputs[output_full_alias]

    output.links.remove(input_full_alias)

    # next = function_node_dict[output_alias]

    # output = all_node_outputs[input_full_alias]

    # output.links.remove(output_full_alias)

    #delete links to node inputs

    node_input = all_node_inputs[input_full_alias]

    node_input.linked = False

    node_input.parameter = [0] #reinitialize as a zero value object but maybe we ought to change this at some point

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
        
        #serialize to json. Use orjson to get numpy constructs saved

        json_intermediate = orjson.loads(json_bytes)

        #now remove inputs and outputs.

        for node_func in json_intermediate.values():

            del node_func['inputs']

            del node_func['outputs']

        #now actually save

        json_bytes = orjson.dumps(json_intermediate, option=
                            orjson.OPT_SERIALIZE_NUMPY |
                            orjson.OPT_APPEND_NEWLINE)
        
        json_str = json_bytes.decode()

        json_file.write(json_str)

def load_state_relink(output: NodeOutput, sender):

    for link in output.links:

        #prevent double linking
        if not dpg.does_alias_exist(output.full_id + link):

            dpg.add_node_link(output.full_id, link, parent = sender, tag = output.full_id + link)

            LinkList.append(output.full_id)

            LinkList.append(link)

            if dpg.does_alias_exist(link + "_value"):

                try:

                    dpg.disable_item(link + "_value") #disable the input being linked into

                except:

                    log('caught disable error node input error')

def load_state(sender, app_data):

    with open("C:/temp/gradient.json", "r") as file:

        json_file = json.load(file)

        for key in json_file.keys():

            _node_name = ''.join(char for char in key if char.isalpha())

            node_group = node_dict_static[_node_name]

            node_func = node_group.load_state(json_file[key])

            node_group.add_from_func(node_func)

            node_func.sync_ui()

            function_node_dict[key] = node_func

        _sender = "NodeEditor"

        for node_func in list(function_node_dict.values()):

            for output in node_func.outputs:

                load_state_relink(output = output, sender = _sender)
import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ...lib.function_node_dict import function_node_dict
from ... lib.node_functions.node_readout_func import *
from ... lib.fusionAddInUtils.general_utils import log

def add_node_readout(app_data, user_data):

    add_node_gui()

def add_node_gui(input_node = None):

    node_template = NodeTemplate(node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = ReadoutNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    val = """ah...., 
    the french"""

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "Readout",
                  pos = input_node.ui_pos):
            
        with dpg.node_attribute(tag = input_node.gui_id + node_input):

            dpg.add_spacer(tag = input_node.gui_id + "_space0",
                width=300)

            dpg.add_input_text(tag = input_node.gui_id + node_input + "_value",
                               default_value = val,
                               multiline = True,
                               readonly = True,
                               width = 300,
                               height = 275,
                               callback = input_node.update)
            
        with dpg.node_attribute(tag = input_node.gui_id + node_output,
            attribute_type=dpg.mvNode_Attr_Output):
               
            dpg.add_spacer(tag = input_node.gui_id + "__space1",
                width=300)
import dearpygui.dearpygui as dpg
from .node_template import NodeTemplate
from ..function_node_dict import function_node_dict
from ..node_functions.node_stack_data_func import *
from ..fusionAddInUtils.general_utils import log

def add_node_stack_data(app_data, user_data):

    add_node_gui()

def add_node_gui(input_node = None):

    node_template = NodeTemplate(node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = StackDataNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "Stack Data",
                  pos = input_node.ui_pos):

        with dpg.node_attribute(tag = input_node.gui_id + node_a_data):
            dpg.add_text(default_value = "Data A",
                            tag = input_node.gui_id + node_a_data + "_value")
            
            dpg.add_spacer(tag = input_node.gui_id + "_space2",
                width=150)
            
        with dpg.node_attribute(tag = input_node.gui_id + node_b_data):
            dpg.add_text(default_value = "Data B",
                            tag = input_node.gui_id + node_b_data + "_value")
            
            dpg.add_spacer(tag = input_node.gui_id + "_space3",
                width=150)
            
        node_template.add_input_int_gui_id(name = node_stack_type_name,
                                           input_label = "Stack Type",
                                           _callback = input_node.update,
                                           gui_id = input_node.gui_id,
                                           default_val = input_node.stack_type.parameter[0])

        with dpg.node_attribute(tag = input_node.gui_id + node_output,
                        attribute_type=dpg.mvNode_Attr_Output):
               
            dpg.add_spacer(tag = input_node.gui_id + "__space4",
                width=150)
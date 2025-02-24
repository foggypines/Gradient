import dearpygui.dearpygui as dpg
from .node_template import NodeTemplate
from ... lib.function_node_dict import function_node_dict
from ... lib.node_functions.node_array_func import *
from ... lib.node_functions.node_base_func import node_output

def add_node_input_array(app_data, user_data):

    add_node_gui()

def add_node_gui(input_node = None):

    node_template = NodeTemplate(node_name = node_name)

    if input_node is None:

            node_template.create_rand_id()

            _tag = (str(node_template.random_id) + node_template.node_type)

            input_node = ArrayNodeFunction(gui_id=_tag)

            function_node_dict[_tag] = input_node

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "Input Array",
                  pos = input_node.ui_pos):
        with dpg.node_attribute(tag = input_node.gui_id + node_output,
                                 attribute_type=dpg.mvNode_Attr_Output):
            dpg.add_spacer(tag = input_node.gui_id + "_value",
                            width=150)

        node_template.add_input_float_gui_id(name = node_increment,
                                            input_label = "Increment",
                                            _callback = input_node.update,
                                            gui_id = input_node.gui_id,
                                            default_val = input_node.increment.parameter[0])

        node_template.add_input_int_gui_id(name = node_count,
                                           input_label = "Count",
                                           _callback = input_node.update,
                                           gui_id = input_node.gui_id,
                                           default_val = input_node.count.parameter[0])
        
        node_template.add_input_float_gui_id(name = node_start,
                                            input_label = "Start",
                                            _callback = input_node.update,
                                            gui_id = input_node.gui_id,
                                            default_val = input_node.start.parameter[0])
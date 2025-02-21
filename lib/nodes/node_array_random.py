import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ...lib.function_node_dict import function_node_dict
from ... lib.node_functions.node_array_random_func import *
from ... lib.fusionAddInUtils.general_utils import log

def add_node_rand_array(app_data, user_data):

    add_node_gui()

def add_node_gui(input_node = None):

    node_template = NodeTemplate(node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = ArrayRandomNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    log("hello from the add node rand array def")

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "Random Array",
                  pos = input_node.ui_pos):
        with dpg.node_attribute(tag = input_node.gui_id + node_output,
                                 attribute_type=dpg.mvNode_Attr_Output):
            
            dpg.add_spacer(tag = input_node.gui_id + "_value",
                            width=150)
            
            dpg.add_button(tag = input_node.gui_id + "_recalc"+ "_value",
                                label="Recalculate",
                                width=150,
                                callback=input_node.update)
            
            dpg.add_spacer(tag = input_node.gui_id + "__value",
                width=150)

        node_template.add_input_float_gui_id(name = node_min,
                                             input_label = "Minimum",
                                             _callback = input_node.update,
                                             gui_id = input_node.gui_id,
                                             default_val = input_node.min.parameter[0])
        
        node_template.add_input_float_gui_id(name = node_max,
                                             input_label = "Maximum",
                                             _callback = input_node.update,
                                             gui_id = input_node.gui_id,
                                             default_val = input_node.max.parameter[0])
        
        node_template.add_input_int_gui_id(name = node_count,
                                           input_label = "Count",
                                           _callback = input_node.update,
                                           gui_id = input_node.gui_id,
                                           default_val = input_node.count.parameter[0])
        
        node_template.add_input_int_gui_id(name = node_set,
                                            input_label = "Set Count",
                                            _callback = input_node.update,
                                            gui_id = input_node.gui_id,
                                            default_val = input_node.set.parameter[0])
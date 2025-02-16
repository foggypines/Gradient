import dearpygui.dearpygui as dpg
from .node_template import NodeTemplate
from ..function_node_dict import function_node_dict
from ..node_functions.node_delete_index_func import *
from ..fusionAddInUtils.general_utils import log

def add_node_delete_index_data(app_data, user_data):

    add_node_gui()

def add_node_gui(input_node = None):

    node_template = NodeTemplate(node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = DeleteIndexNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "Delete Index Data",
                  pos = input_node.ui_pos):

        with dpg.node_attribute(tag = input_node.gui_id + set_name):
            dpg.add_text(default_value = "Set",
                            tag = input_node.gui_id + set_name + "_value")
            
            dpg.add_spacer(tag = input_node.gui_id + "_space2",
                width=150)
            
        with dpg.node_attribute(tag = input_node.gui_id + indices_name):
            node_template.add_input_int_gui_id(name = indices_name,
                                               input_label = "Indices",
                                               _callback = input_node.compute,
                                               gui_id = input_node.gui_id,
                                               default_val = input_node.indices.parameter[0])
            
            dpg.add_spacer(tag = input_node.gui_id + "_space3",
                width=150)
            
        with dpg.node_attribute(tag = input_node.gui_id + node_output_name,
                        attribute_type=dpg.mvNode_Attr_Output):
               
            dpg.add_spacer(tag = input_node.gui_id + "__space4",
                width=150)
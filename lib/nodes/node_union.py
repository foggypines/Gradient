import dearpygui.dearpygui as dpg
from .node_template import NodeTemplate
from ..function_node_dict import function_node_dict
from ..node_functions.node_union_func import *

def add_node_union_data(app_data, user_data):

    add_node_gui()

def add_node_gui(input_node = None):

    node_template = NodeTemplate(node_type)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = UnionNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "BReP Union",
                  pos = input_node.ui_pos):

        with dpg.node_attribute(tag = input_node.gui_id + node_a_input):
            dpg.add_text(default_value = "Target",
                            tag = input_node.gui_id + node_a_input + "_value")
            
            dpg.add_spacer(tag = input_node.gui_id + "_space2",
                width=150)
            
        with dpg.node_attribute(tag = input_node.gui_id + node_b_input):
            dpg.add_text(default_value = "Tool",
                            tag = input_node.gui_id + node_b_input + "_value")
            
            dpg.add_spacer(tag = input_node.gui_id + "_space3",
                width=150)
            

        with dpg.node_attribute(tag = input_node.gui_id + node_output,
                        attribute_type=dpg.mvNode_Attr_Output):
               
            dpg.add_spacer(tag = input_node.gui_id + "__space4",
                width=150)
import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ... lib.function_node_dict import function_node_dict
from ... lib.node_functions import node_bounding_box_func as bound_box_func
from ... lib.node_functions import node_brep_box_func as brep_box_func
from ... lib.node_functions.node_base_func import *

def add_node_bounding_box(app_data, user_data):
    
    add_node_bounding_box_gui(input_node = None)

def add_node_bounding_box_gui(input_node = None):

    node_template = NodeTemplate(bound_box_func.node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = bound_box_func.BoundingBoxNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "Bounding Box",
                  pos = input_node.ui_pos):

        for node_input in input_node.inputs:

            node_template.add_from_node_input(node_input = node_input,
                                              _callback = input_node.compute)
            
        with dpg.node_attribute(tag = input_node.output.full_id,
                                 attribute_type = dpg.mvNode_Attr_Output):
            dpg.add_spacer(tag = input_node.gui_id + "_value",
                    width=150)
        
def add_node_brep_box(app_data, user_data):

    add_node_brep_box_gui(input_node = None)

def add_node_brep_box_gui(input_node = None):

    node_template = NodeTemplate(bound_box_func.node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = brep_box_func.BRePBoxNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "BReP Box",
                  pos = input_node.ui_pos):

        for node_input in input_node.inputs:

            node_template.add_from_node_input(node_input = node_input,
                                              _callback = input_node.compute)
            
        with dpg.node_attribute(tag = input_node.output.full_id,
                                 attribute_type = dpg.mvNode_Attr_Output):
            dpg.add_spacer(tag = input_node.gui_id + "_value",
                            width=150)
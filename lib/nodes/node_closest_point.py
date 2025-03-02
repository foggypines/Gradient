import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ... lib.node_functions.node_base_func import node_output
from ... lib.function_node_dict import function_node_dict
from ... lib.node_functions.node_closest_point_func import *
from ... lib.fusionAddInUtils.general_utils import log

def add_node_closest_point(app_data, user_data):

    add_node_gui()

def add_node_gui(input_node = None):

    node_template = NodeTemplate(node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = ClosestPointNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "Closest Point",
                  pos = input_node.ui_pos):

        with dpg.node_attribute(tag = input_node.gui_id + point_name):
            dpg.add_text(default_value = "Point",
                            tag = input_node.gui_id + point_name + "_value")
            
            dpg.add_spacer(tag = input_node.gui_id + "_space",
                width=150)
            
        with dpg.node_attribute(tag = input_node.gui_id + point_set_name):
            dpg.add_text(default_value = "Point Set",
                            tag = input_node.gui_id + point_set_name + "_value")
            
            dpg.add_spacer(tag = input_node.gui_id + "_space1",
                width=150)

        # for node_output in input_node.outputs: 
            
        #     node_template.add_from_node_output(node_output=node_output)
            
        with dpg.node_attribute(tag = input_node.gui_id + node_output,
                        attribute_type=dpg.mvNode_Attr_Output):
            dpg.add_text(default_value = "Closest", indent = 100)
               
            dpg.add_spacer(tag = input_node.gui_id + "__space2",
                width=150)
            
        with dpg.node_attribute(tag = input_node.gui_id + node_output_distance,
                        attribute_type=dpg.mvNode_Attr_Output):
            dpg.add_text(default_value = "Distance", indent = 100)
               
            dpg.add_spacer(tag = input_node.gui_id + "__space3",
                width=150)
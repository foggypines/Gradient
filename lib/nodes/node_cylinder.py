import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ... lib.function_node_dict import function_node_dict
from ... lib.node_functions.node_cylinder_func import CylinderNodeFunction, node_name, node_point_input, node_vector_input, node_radius_input, node_output
from ... lib.fusionAddInUtils.general_utils import log

def add_node_cylinder(app_data, user_data):
      
    add_node_gui()

def add_node_gui(input_node = None):

    node_template = NodeTemplate(node_name = node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = CylinderNodeFunction(gui_id =_tag)

        function_node_dict[_tag] = input_node

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = node_template.label,
                  pos = input_node.ui_pos):
        
        with dpg.node_attribute(tag=input_node.gui_id + node_point_input):
                dpg.add_text(default_value = "point",
                              tag = input_node.gui_id + node_point_input + "_value")
                
        with dpg.node_attribute(tag = input_node.gui_id + node_vector_input):
                dpg.add_text(default_value = "vector",
                                tag = input_node.gui_id + node_vector_input + "_value")

        node_template.add_input_float_gui_id(name = node_radius_input,
                                             input_label = "Radius",
                                             _callback = input_node.compute,
                                             gui_id = input_node.gui_id,
                                             default_val = input_node.rad.parameter[0])
        
        node_template.add_out_obj(gui_id = input_node.gui_id)

    log("Cylinder node creation complete")
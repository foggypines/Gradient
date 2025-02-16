import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ... lib.node_functions.node_sphere_func import node_name, node_point_input, node_rad_input, node_out_put, SphereNodeFunction
from ... lib.function_node_dict import function_node_dict
from ...lib.node_functions.node_input import all_node_inputs
from ... lib.fusionAddInUtils.general_utils import log

class node_sphere(NodeTemplate):

    def __init__(self, node_name):
        NodeTemplate.__init__(self, node_name)
        
    def add_node(self):

        self.add_node_gui()

    def add_node_gui(self, input_node = None):

        if input_node is None:

            self.create_rand_id()

            _tag = (str(self.random_id) + self.node_type)

            input_node = SphereNodeFunction(gui_id=_tag)

            function_node_dict[_tag] = input_node

        log(f'we are now here the gui id is {input_node.gui_id}')

        with dpg.node(tag = input_node.gui_id,
                      parent="NodeEditor",
                      label=self.label,
                      pos=input_node.ui_pos):

            with dpg.node_attribute(tag = input_node.gui_id + node_point_input):
                dpg.add_text(default_value = "point",
                            tag = input_node.gui_id + node_point_input + "_value")

            self.add_input_float_gui_id(name = node_rad_input,
                                input_label = "Radius",
                                _callback = input_node.compute,
                                gui_id = input_node.gui_id,
                                default_val = input_node.rad.parameter[0])
            
            self.add_out_obj(gui_id=input_node.gui_id)

        log("sphere creation complete")

node_sphere_instance = node_sphere(node_name)
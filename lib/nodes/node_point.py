import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ... lib.node_functions.node_point_func import PointNodeFunction, node_x_input, node_y_input, node_z_input, node_out_put
from ... lib.function_node_dict import function_node_dict
from ... lib.fusionAddInUtils.general_utils import log

class node_point(NodeTemplate):

    def __init__(self, node_name):
        NodeTemplate.__init__(self, node_name)
        
    def add_node(self, user_data):

        self.create_rand_id()

        _pos = [200,200]

        _tag = (str(self.random_id) + self.node_type)

        try:

            point_node_func = PointNodeFunction(gui_id=_tag)

            log("initialized point func object")

        except Exception as ex:
            
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)

            log(f'{message}')

        with dpg.node(tag=_tag,
                      parent="NodeEditor",
                      label=self.label,
                      pos=_pos):
            self.add_input_float_(node_x_input, "X value", point_node_func.compute)
            self.add_input_float_(node_y_input, "Y value", point_node_func.compute)
            self.add_input_float_(node_z_input, "Z value", point_node_func.compute)
            with dpg.node_attribute(tag=str(self.random_id) + self.node_type + "_Output", attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_spacer(tag=str(self.random_id) + self.node_type + "_value",
                                width=150)

        log('about to add {point_node_func} to funct dictionary')

        function_node_dict[_tag] = point_node_func

        log('added function to dictionary')

node_point_instance = node_point('Point')

def add_from_func(input_func: PointNodeFunction):

    node_point = NodeTemplate('Point')

    with dpg.node(tag=input_func.gui_id,
                    parent="NodeEditor",
                    label=node_point.label,
                    pos=input_func.ui_pos): 

        with dpg.node_attribute(tag=input_func.gui_id + node_x_input):
            dpg.add_input_float(tag=input_func.gui_id + node_x_input + "_value",
                                label="X value",
                                width=150,
                                default_value=0,
                                callback=input_func.compute)
        
        with dpg.node_attribute(tag=input_func.gui_id + node_y_input):
            dpg.add_input_float(tag=input_func.gui_id + node_y_input + "_value",
                        label="Y value",
                        width=150,
                        default_value=0,
                        callback=input_func.compute)
            
        with dpg.node_attribute(tag=input_func.gui_id + node_z_input):
            dpg.add_input_float(tag=input_func.gui_id + node_z_input + "_value",
                                label="Z value",
                                width=150,
                                default_value=0,
                                callback=input_func.compute)

        with dpg.node_attribute(tag=input_func.gui_id + "_Output", attribute_type=dpg.mvNode_Attr_Output):
            dpg.add_spacer(tag=input_func.gui_id + "_value",
                            width=150)
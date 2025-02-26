import random
import dearpygui.dearpygui as dpg
from ..node_functions.node_input import NodeInput
from ..node_functions.node_output import NodeOutput

class NodeTemplate:

    def __init__(self, node_name):
        self.tag = "Menu_AddNode_" + node_name
        self.label = node_name
        self.user_data = node_name
        self.node_type = "!" + node_name

    def add_menu_item(self):
        dpg.add_menu_item(tag = self.tag,
                          label = self.label,
                          callback = self.add_node,
                          user_data = self.user_data)
        
    def create_rand_id(self):
        self.random_id = random.randint(0, 50000)
        while dpg.does_item_exist(str(self.random_id) + self.node_type):
            self.random_id = random.randint(0, 50000)

    def add_from_node_input(self, node_input: NodeInput, _callback):
        with dpg.node_attribute(tag = node_input.full_id):

            if node_input.ui_element == True:

                dpg.add_input_float(tag = node_input.full_id + "_value",
                                    label = node_input.ui_label,
                                    width = 150,
                                    default_value = node_input.parameter[0],
                                    callback = _callback)
                
            else:
                dpg.add_text(default_value= node_input.ui_label, indent=150)
            
    def add_input_float_(self, name, input_label, _callback, default_val = 0):
        with dpg.node_attribute(tag=str(self.random_id) + self.node_type + name):
            dpg.add_input_float(tag=str(self.random_id) + self.node_type + name + "_value",
                                label=input_label,
                                width=150,
                                default_value=default_val,
                                callback=_callback)
            
    def add_input_float_gui_id(self, name, input_label, _callback, gui_id, default_val = 0):
        with dpg.node_attribute(tag=gui_id + name):
            dpg.add_input_float(tag=gui_id + name + "_value",
                                label=input_label,
                                width=150,
                                default_value=default_val,
                                callback=_callback)
            
    def add_input_int(self, name, input_label, _callback, default_val = 0):
        with dpg.node_attribute(tag=str(self.random_id) + self.node_type + name):
            dpg.add_input_int(tag=str(self.random_id) + self.node_type + name + "_value",
                                label=input_label,
                                width=150,
                                default_value=default_val,
                                callback=_callback)  
            
    def add_input_int_gui_id(self, name, input_label, _callback, gui_id, default_val = 0):
        with dpg.node_attribute(tag = gui_id + name):
            dpg.add_input_int(tag = gui_id + name + "_value",
                                label = input_label,
                                width = 150,
                                default_value = default_val,
                                callback = _callback)

    def add_from_node_output(self, node_output: NodeOutput):
        with dpg.node_attribute(tag = node_output.full_id,
                attribute_type=dpg.mvNode_Attr_Output):

            dpg.add_spacer(tag = node_output.full_id + "__space0",
                width=150)

    def add_out_float(self, name, input_label):
        with dpg.node_attribute(tag=str(self.random_id) + self.node_type + name, attribute_type=dpg.mvNode_Attr_Output):
            dpg.add_input_float(tag=str(self.random_id) + self.node_type + name + "_value",
                                label=input_label,
                                width=150,
                                default_value=0,
                                readonly=True)
            
    def add_out_obj(self, gui_id):
        with dpg.node_attribute(tag = gui_id + "_Output", attribute_type=dpg.mvNode_Attr_Output):
            dpg.add_spacer(tag = gui_id + "_value", width = 150, height = 10)
            dpg.add_text(default_value="Body", indent=150)
            
    def add_node(self, user_data):
        pass

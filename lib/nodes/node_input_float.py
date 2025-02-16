import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from random import randint
from ... lib.node_manager import function_node_dict
from ... lib.node_functions.node_input_float_func import InputFloatNodeFunction, node_name
from ... lib.fusionAddInUtils.general_utils import log

def add_node_input_float(app_data, user_data):

    add_node_gui()

# Add simple input node
def add_node_gui(input_node = None):

    log('adding gui')

    #check if the input_node is a None type
    if input_node is None:

        # Create random ID and check that the ID does not exist yet for this node type
        random_id = randint(0, 50000)
        while dpg.does_item_exist(str(random_id) + "!NodeInput"):
            random_id = randint(0, 50000)

        tag = str(random_id) + "!" + node_name

        input_node = InputFloatNodeFunction(gui_id=tag)

        function_node_dict[tag] = input_node

    with dpg.node(tag=input_node.gui_id,
                  parent="NodeEditor",
                  label="Input float",
                  pos=input_node.ui_pos):
        with dpg.node_attribute(tag=input_node.gui_id + "_Output", attribute_type=dpg.mvNode_Attr_Output):
            dpg.add_input_float(tag=input_node.gui_id + "_Output_value",
                                label="Float value",
                                width=150,
                                default_value=input_node.value,
                                callback=input_node.compute)
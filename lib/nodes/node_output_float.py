# Copyright 2021 LuminousLizard
# Licensed under the MIT-License

import dearpygui.dearpygui as dpg
from random import randint


# Add simple input node for an int value with hard coded ID "1"
def add_node_output_float(user_data):
    # Create random ID and check that the ID does not exist yet for this node type
    random_id = randint(0, 50000)
    while dpg.does_item_exist(str(random_id) + "!Node_Output"):
        random_id = randint(0, 50000)

    # Simple result node for an int value with hard coded ID "3"
    with dpg.node(tag=str(random_id) + "!Node_Result",
                  parent="NodeEditor",
                  label="Result",
                  pos=user_data):
        with dpg.node_attribute(tag=str(random_id) + "!Node_Result_Input"):
            dpg.add_input_text(tag=str(random_id) + "!Node_Result_Input_value",
                               width=150,
                               default_value="None",
                               enabled=False,
                               label="Result")

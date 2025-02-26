import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ... lib.node_functions.node_base_func import node_output
from ... lib.node_functions.node_transform_func import TransformNodeFunction, node_type
from ... lib.function_node_dict import function_node_dict
from ... lib.fusionAddInUtils.general_utils import log

def add_node_transform(app_data, user_data):

    add_node_gui()

def add_node_gui(node = None):

    node_template = NodeTemplate(node_type)

    if node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        node = TransformNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = node

    with dpg.node(tag = node.gui_id,
                  parent = "NodeEditor",
                  label = "BReP Transform",
                  pos = node.ui_pos):

        for node_input in node.inputs:

            node_template.add_from_node_input(node_input = node_input, _callback = node.update)

        node_template.add_from_node_output(node.output)
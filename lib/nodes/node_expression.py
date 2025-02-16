import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ...lib.function_node_dict import function_node_dict
from ... lib.node_functions.node_expression_func import *
from ... lib.fusionAddInUtils.general_utils import log

def add_node_expr(app_data, user_data):

    add_node_gui()

def add_node_gui(input_node = None):

    node_template = NodeTemplate(node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = ExpressionNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    with dpg.node(tag = input_node.gui_id,
                  parent = "NodeEditor",
                  label = "Expression",
                  pos = input_node.ui_pos):
            
        with dpg.node_attribute(tag = input_node.gui_id + node_expression):
            dpg.add_input_text(tag = input_node.gui_id + node_expression + "_value",
                                label = "Expression",
                                width = 150,
                                default_value = input_node.expression.parameter,
                                callback = input_node.compute)
            
            dpg.add_spacer(tag = input_node.gui_id + "_space1",
                width=150)

        with dpg.node_attribute(tag = input_node.gui_id + node_a_var):
            dpg.add_text(default_value = "a Variable",
                            tag = input_node.gui_id + node_a_var + "_value")
            
            dpg.add_spacer(tag = input_node.gui_id + "_space2",
                width=150)
            
        with dpg.node_attribute(tag = input_node.gui_id + node_b_var):
            dpg.add_text(default_value = "b Variable",
                            tag = input_node.gui_id + node_b_var + "_value")
            
            dpg.add_spacer(tag = input_node.gui_id + "_space3",
                width=150)
            
        with dpg.node_attribute(tag = input_node.gui_id + node_output,
                        attribute_type=dpg.mvNode_Attr_Output):
               
            dpg.add_spacer(tag = input_node.gui_id + "__space4",
                width=150)
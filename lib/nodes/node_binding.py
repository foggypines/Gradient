import dearpygui.dearpygui as dpg
from . node_template import NodeTemplate
from ... lib.function_node_dict import function_node_dict
from ... lib.node_functions import node_bounding_box_func as bound_box_func
from ... lib.node_functions import node_brep_box_func as brep_box_func
from ... lib.node_functions import node_cross_product_func as cross_product_func
from ... lib.node_functions import node_get_BReP_func as get_brep_func
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

    node_template.generate_gui(input_node = input_node, label="Bounding Box")
        
def add_node_brep_box(app_data, user_data):

    add_node_brep_box_gui(input_node = None)

def add_node_brep_box_gui(input_node = None):

    node_template = NodeTemplate(bound_box_func.node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = brep_box_func.BRePBoxNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    node_template.generate_gui(input_node = input_node, label="BReP Box")

def add_node_cross_product(app_data, user_data):

    add_node_cross_product_gui(input_node = None)

def add_node_cross_product_gui(input_node = None):

    node_template = NodeTemplate(cross_product_func.node_name)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = cross_product_func.CrossProductNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    node_template.generate_gui(input_node = input_node, label="Cross Product")

def add_node_get_brep(app_data, user_data):

    add_node_get_brep_gui(input_node = None)

def add_node_get_brep_gui(input_node = None):

    node_template = NodeTemplate(get_brep_func.node_type)

    if input_node is None:

        node_template.create_rand_id()

        _tag = (str(node_template.random_id) + node_template.node_type)

        input_node = get_brep_func.GetBRepNodeFunction(gui_id = _tag)

        function_node_dict[_tag] = input_node

    node_template.generate_gui(input_node = input_node, label="Get BRep")
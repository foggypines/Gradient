from .node_functions import *
from .nodes import *

class NodeDictGroup:

    def __init__(self, load_state, add_from_func):

        self.load_state = load_state
        
        self.add_from_func = add_from_func

node_dict_static = {
    
    #Input Output

    node_input_float.node_name: NodeDictGroup(node_input_float_func.InputFloatNodeFunction.from_dict,
                                              node_input_float.add_node_gui),

    node_array_func.node_name: NodeDictGroup(node_array_func.ArrayNodeFunction.from_dict,
                                             node_array.add_node_gui),

    node_array_random_func.node_name: NodeDictGroup(node_array_random_func.ArrayRandomNodeFunction.from_dict,
                                                    node_array_random.add_node_gui),

    # node_readout_func.node_name: NodeDictGroup(node_readout_func.ReadoutNodeFunction.from_dict,
    #                                            node_readout.add_node_gui),

    #Math

    node_expression.node_name: NodeDictGroup(node_expression_func.ExpressionNodeFunction.from_dict,
                                              node_expression.add_node_gui),

    #Premitive Geometry

    node_point_func.node_name: NodeDictGroup(node_point_func.PointNodeFunction.from_dict,
                                             node_point.add_from_func),

    #Evaluate

    node_closest_point_func.node_name: NodeDictGroup(node_closest_point_func.ClosestPointNodeFunction.from_dict,
                                                     node_closest_point.add_node_gui),

    #Solid Geometry

    node_sphere_func.node_name: NodeDictGroup(node_sphere_func.SphereNodeFunction.from_dict,
                                              node_sphere.node_sphere_instance.add_node_gui),


    node_cylinder_func.node_name: NodeDictGroup(node_cylinder_func.CylinderNodeFunction.from_dict,
                                                node_cylinder.add_node_gui),
    }